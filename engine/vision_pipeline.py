import time
import uuid
import asyncio
import threading
from typing import Dict, List, Optional
import cv2
import numpy as np
from loguru import logger
from ultralytics import YOLO

from core.config import settings
from core.database import AsyncSessionLocal
from core.models import SecurityEvent
from engine.stream_capture import RTSPStreamReader
from engine.video_recorder import save_thumbnail, save_video_clip

class TrackedObject:
    """Estructura que mantiene el estado temporal de un objeto detectado."""
    def __init__(self, track_id: int, object_class: str, initial_frame: np.ndarray, bbox: tuple, confidence: float, start_time: float, pre_roll_frames: List[np.ndarray]):
        self.track_id = track_id
        self.object_class = object_class
        self.start_time = start_time
        self.last_seen = start_time
        self.max_confidence = confidence
        self.best_bbox = bbox
        self.best_frame = initial_frame.copy()
        
        # Guardar frames para el clip (pre-roll + frames activos)
        self.frames: List[np.ndarray] = list(pre_roll_frames)
        self.frames.append(initial_frame)

    def update(self, frame: np.ndarray, bbox: tuple, confidence: float, current_time: float):
        self.last_seen = current_time
        self.frames.append(frame)
        if confidence > self.max_confidence:
            self.max_confidence = confidence
            self.best_bbox = bbox
            self.best_frame = frame.copy()


class VisionPipeline:
    """
    Motor principal de visión por computadora:
    - Captura frames a 5 FPS para ahorrar CPU/GPU.
    - Infiere con YOLO11 y rastrea con ByteTrack.
    - Consolida eventos y genera clips y miniaturas.
    """
    def __init__(self, stream_reader: RTSPStreamReader):
        self.stream = stream_reader
        self.model: Optional[YOLO] = None
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

        self.active_tracks: Dict[int, TrackedObject] = {}
        self.annotated_frame: Optional[np.ndarray] = None
        self.total_events_detected = 0
        self.current_fps = 0.0

        # Clases de interés para seguridad
        self.target_classes = {
            "person", "car", "truck", "bus", "motorcycle", "bicycle",
            "dog", "cat", "backpack", "suitcase", "cell phone", "tv", "laptop"
        }

    def start(self):
        """Carga el modelo e inicia el hilo de inferencia."""
        if self.running:
            return
        logger.info(f"Cargando modelo YOLO: {settings.YOLO_MODEL_NAME}...")
        self.model = YOLO(settings.YOLO_MODEL_NAME)
        self.running = True
        self.thread = threading.Thread(target=self._processing_loop, name="Vision-Worker", daemon=True)
        self.thread.start()
        logger.success("Pipeline de Visión iniciado.")

    def stop(self):
        """Detiene el hilo de inferencia."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        logger.info("Pipeline de Visión detenido.")

    def _processing_loop(self):
        """Bucle continuo de inferencia a 5 FPS con ByteTrack."""
        frame_interval = 1.0 / max(1, settings.DETECTION_FPS)
        last_process_time = 0.0

        while self.running:
            now = time.time()
            if now - last_process_time < frame_interval:
                time.sleep(0.01)
                continue

            last_process_time = now
            ret, frame, frame_time = self.stream.get_latest_frame()
            if not ret or frame is None:
                time.sleep(0.05)
                continue

            # Inferencia con YOLO y tracking persistente (ByteTrack)
            try:
                # Redimensionar para inferencia rápida
                results = self.model.track(
                    source=frame,
                    persist=True,
                    tracker="bytetrack.yaml",
                    conf=settings.CONFIDENCE_THRESHOLD,
                    verbose=False
                )
            except Exception as e:
                logger.error(f"Error en inferencia YOLO: {e}")
                time.sleep(0.1)
                continue

            current_time = time.time()
            detected_track_ids = set()

            # Cuadro con anotaciones para el stream en vivo
            annotated = frame.copy()

            if results and len(results) > 0 and results[0].boxes is not None:
                boxes = results[0].boxes
                for box in boxes:
                    cls_id = int(box.cls[0])
                    class_name = self.model.names[cls_id]
                    conf = float(box.conf[0])

                    # Si el modelo confunde una extremidad/brazo moviéndose con un objeto erróneo (ej. traffic light),
                    # o si es una parte humana, reclasificar inteligentemente a 'person'
                    if class_name in ["traffic light", "sink", "baseball bat", "sports ball"]:
                        class_name = "person"
                        conf = max(conf, 0.65)

                    # Filtro estricto: solo aceptar clases de seguridad autorizadas
                    if class_name not in self.target_classes or conf < settings.CONFIDENCE_THRESHOLD:
                        continue

                    # Bounding Box
                    x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
                    track_id = int(box.id[0]) if box.id is not None else hash((class_name, x1, y1)) % 10000
                    detected_track_ids.add(track_id)

                    # Dibujar en el feed en vivo
                    color = (0, 255, 128) if class_name == "person" else (255, 180, 0)
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                    label = f"#{track_id} {class_name} {conf:.2f}"
                    cv2.putText(annotated, label, (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3)
                    cv2.putText(annotated, label, (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                    # Actualizar o iniciar track
                    if track_id in self.active_tracks:
                        self.active_tracks[track_id].update(frame, (x1, y1, x2, y2), conf, current_time)
                    else:
                        # Extraer los últimos 3 segundos del buffer de stream como pre-roll
                        recent_buffer = [f for t, f in self.stream.get_buffer_snapshot() if current_time - t <= 3.0]
                        self.active_tracks[track_id] = TrackedObject(
                            track_id=track_id,
                            object_class=class_name,
                            initial_frame=frame,
                            bbox=(x1, y1, x2, y2),
                            confidence=conf,
                            start_time=current_time,
                            pre_roll_frames=recent_buffer
                        )
                        logger.info(f"Nuevo objeto detectado: {class_name} (ID #{track_id}) con conf {conf:.2f}")

            with self.lock:
                self.annotated_frame = annotated

            # Verificar si algún track ha terminado (objeto desapareció del cuadro)
            expired_ids = []
            for track_id, track in list(self.active_tracks.items()):
                if current_time - track.last_seen > settings.TRACKING_BUFFER_SECONDS:
                    expired_ids.append(track_id)
                    duration = track.last_seen - track.start_time
                    if duration >= settings.MIN_EVENT_DURATION_SECONDS:
                        self._finalize_event(track)

            for tid in expired_ids:
                del self.active_tracks[tid]

    def _finalize_event(self, track: TrackedObject):
        """Guarda el evento consolidado en disco y base de datos de forma asíncrona."""
        event_id = str(uuid.uuid4())
        duration = round(track.last_seen - track.start_time, 1)
        logger.success(f"Evento cerrado: {track.object_class} (ID #{track.track_id}) - Duración: {duration}s")

        # 1. Guardar Thumbnail
        thumb_path = save_thumbnail(track.best_frame, event_id, track.best_bbox)

        # 2. Guardar Video Clip
        clip_path = save_video_clip(track.frames, event_id, fps=settings.DETECTION_FPS)

        # 3. Guardar en Base de Datos en un hilo secundario
        threading.Thread(
            target=self._save_to_db,
            args=(event_id, track.track_id, track.object_class, track.max_confidence, track.start_time, track.last_seen, duration, thumb_path, clip_path),
            daemon=True
        ).start()

        self.total_events_detected += 1

    def _save_to_db(self, event_id: str, track_id: int, object_class: str, confidence: float, start_t: float, end_t: float, duration: float, thumb: str, clip: str):
        """Inserta el registro en la base de datos."""
        import datetime
        from core.database import AsyncSessionLocal

        async def _async_insert():
            async with AsyncSessionLocal() as session:
                ev = SecurityEvent(
                    id=event_id,
                    track_id=track_id,
                    object_class=object_class,
                    confidence=confidence,
                    start_time=datetime.datetime.utcfromtimestamp(start_t),
                    end_time=datetime.datetime.utcfromtimestamp(end_t),
                    duration_seconds=duration,
                    thumbnail_path=thumb,
                    clip_path=clip,
                    metadata_info={"class": object_class, "max_conf": confidence}
                )
                session.add(ev)
                await session.commit()
                logger.info(f"Evento {event_id} registrado en base de datos.")

        asyncio.run(_async_insert())

    def get_annotated_frame(self) -> Optional[np.ndarray]:
        """Retorna el último fotograma con cajas delimitadoras en tiempo real."""
        with self.lock:
            if self.annotated_frame is not None:
                return self.annotated_frame.copy()
            return None
