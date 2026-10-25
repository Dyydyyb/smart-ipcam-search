import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger
from core.config import settings

CAMERAS_FILE = settings.STORAGE_DIR / "cameras.json"

DEFAULT_CAMERAS = []

class CameraManager:
    """Administra el registro dinámico de cámaras IP para despliegue distribuido."""
    def __init__(self, file_path: Path = CAMERAS_FILE):
        self.file_path = file_path
        self._load()

    def _load(self):
        if not self.file_path.exists():
            self._save(DEFAULT_CAMERAS)
            self.cameras = list(DEFAULT_CAMERAS)
        else:
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.cameras = json.load(f)
            except Exception as e:
                logger.error(f"Error cargando cameras.json: {e}")
                self.cameras = list(DEFAULT_CAMERAS)

    def _save(self, data: List[Dict[str, Any]]):
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando cameras.json: {e}")

    def get_all(self) -> List[Dict[str, Any]]:
        self._load()
        return self.cameras

    def get(self, camera_id: str) -> Optional[Dict[str, Any]]:
        self._load()
        for c in self.cameras:
            if c.get("id") == camera_id:
                return c
        return None

    def add(self, name: str, location: str, ip: str, port: int, user: str, password: str, rtsp_sub: Optional[str] = None, rtsp_main: Optional[str] = None) -> Dict[str, Any]:
        self._load()
        cam_id = f"cam_{uuid.uuid4().hex[:6]}"
        sub_url = rtsp_sub or f"rtsp://{user}:{password}@{ip}:{port}/cam/realmonitor?channel=1&subtype=1"
        main_url = rtsp_main or f"rtsp://{user}:{password}@{ip}:{port}/cam/realmonitor?channel=1&subtype=0"

        new_cam = {
            "id": cam_id,
            "name": name.strip(),
            "location": location.strip() if location else "General",
            "ip": ip.strip(),
            "port": port,
            "user": user.strip(),
            "rtsp_sub": sub_url,
            "rtsp_main": main_url,
            "is_active": True
        }
        self.cameras.append(new_cam)
        self._save(self.cameras)
        logger.info(f"Nueva cámara registrada: {name} ({cam_id})")
        return new_cam

    def delete(self, camera_id: str) -> bool:
        self._load()
        initial_len = len(self.cameras)
        self.cameras = [c for c in self.cameras if c.get("id") != camera_id]
        if len(self.cameras) < initial_len:
            self._save(self.cameras)
            logger.info(f"Cámara eliminada: {camera_id}")
            return True
        return False

camera_manager = CameraManager()
