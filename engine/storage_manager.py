import os
import time
import shutil
import asyncio
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
from sqlalchemy import select, desc, asc
from core.config import settings
from core.database import AsyncSessionLocal
from core.models import SecurityEvent

class StorageManager:
    """
    Gestor de almacenamiento y retención 24/7.
    Asegura que el servidor nunca se quede sin espacio en disco ni se cuelgue:
    - Purga eventos más antiguos de N días (política de retención configurable).
    - Monitorea el tamaño total en disco y libera espacio si se supera el límite de GB.
    """
    def __init__(self):
        self.running = False
        self.thread: threading.Thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._cleanup_loop, name="Storage-Retention-Worker", daemon=True)
        self.thread.start()
        logger.info(f"[StorageManager] Worker de retención automática 24/7 iniciado (Límite: {settings.MAX_STORAGE_GB} GB / {settings.RETENTION_DAYS} días).")

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        logger.info("[StorageManager] Worker de retención detenido.")

    def get_storage_stats(self) -> Dict[str, Any]:
        """Calcula el uso de almacenamiento en gigabytes y conteo de archivos."""
        total_bytes = 0
        file_count = 0

        for root, _, files in os.walk(settings.STORAGE_DIR):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    total_bytes += os.path.getsize(fp)
                    file_count += 1
                except OSError:
                    pass

        # Espacio en disco del sistema
        try:
            total, used, free = shutil.disk_usage(settings.STORAGE_DIR)
        except Exception:
            total, used, free = (0, 0, 0)

        used_gb = round(total_bytes / (1024 ** 3), 2)
        free_disk_gb = round(free / (1024 ** 3), 2)

        return {
            "app_storage_used_gb": used_gb,
            "app_storage_limit_gb": settings.MAX_STORAGE_GB,
            "system_disk_free_gb": free_disk_gb,
            "total_files": file_count,
            "retention_days": settings.RETENTION_DAYS
        }

    def _cleanup_loop(self):
        """Bucle periódico de verificación y limpieza en segundo plano."""
        # Ejecutar una limpieza inicial a los 30 segundos del arranque
        time.sleep(30)
        while self.running:
            try:
                asyncio.run(self.run_retention_cleanup())
            except Exception as e:
                logger.error(f"[StorageManager] Error durante la limpieza de almacenamiento: {e}")

            # Dormir hasta el siguiente intervalo (ej. 60 minutos)
            for _ in range(settings.AUTO_CLEANUP_INTERVAL_MINUTES * 60):
                if not self.running:
                    break
                time.sleep(1)

    async def run_retention_cleanup(self) -> Dict[str, Any]:
        """Ejecuta la purga de eventos vencidos o exceso de tamaño en disco."""
        logger.info("[StorageManager] Ejecutando análisis de retención en almacenamiento...")
        deleted_count = 0
        freed_bytes = 0

        cutoff_date = datetime.now() - timedelta(days=settings.RETENTION_DAYS)

        async with AsyncSessionLocal() as session:
            # 1. Purga por días de retención
            old_stmt = select(SecurityEvent).where(SecurityEvent.start_time < cutoff_date)
            result = await session.execute(old_stmt)
            expired_events = result.scalars().all()

            for ev in expired_events:
                freed_bytes += self._delete_event_files(ev)
                await session.delete(ev)
                deleted_count += 1

            if expired_events:
                await session.commit()
                logger.info(f"[StorageManager] {deleted_count} eventos anteriores a {settings.RETENTION_DAYS} días eliminados.")

            # 2. Purga por cuota máxima de disco si se supera MAX_STORAGE_GB
            max_bytes = settings.MAX_STORAGE_GB * (1024 ** 3)
            current_bytes = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(settings.STORAGE_DIR) for f in fs if os.path.exists(os.path.join(r, f)))

            if current_bytes > max_bytes:
                logger.warning(f"[StorageManager] Almacenamiento ({round(current_bytes / 1024**3, 2)} GB) supera el límite de {settings.MAX_STORAGE_GB} GB. Purgando eventos más antiguos...")
                excess_stmt = select(SecurityEvent).order_by(asc(SecurityEvent.start_time)).limit(100)
                excess_res = await session.execute(excess_stmt)
                excess_events = excess_res.scalars().all()

                for ev in excess_events:
                    freed_bytes += self._delete_event_files(ev)
                    await session.delete(ev)
                    deleted_count += 1
                    current_bytes -= freed_bytes
                    if current_bytes <= max_bytes * 0.85: # Reducir al 85% del límite
                        break

                await session.commit()

        freed_mb = round(freed_bytes / (1024 ** 2), 2)
        logger.success(f"[StorageManager] Mantenimiento finalizado: {deleted_count} eventos purgados, {freed_mb} MB liberados.")
        return {"deleted_count": deleted_count, "freed_mb": freed_mb}

    def _delete_event_files(self, event: SecurityEvent) -> int:
        """Elimina físicamente el clip de video y thumbnail de un evento."""
        freed = 0
        if event.thumbnail_path and os.path.exists(event.thumbnail_path):
            try:
                freed += os.path.getsize(event.thumbnail_path)
                os.remove(event.thumbnail_path)
            except Exception:
                pass

        if event.clip_path and os.path.exists(event.clip_path):
            try:
                freed += os.path.getsize(event.clip_path)
                os.remove(event.clip_path)
            except Exception:
                pass

        return freed

storage_manager = StorageManager()
