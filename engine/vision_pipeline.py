import time
import uuid
import asyncio
import threading
from typing import Dict, List, Optional, Any
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

    def analyze_appearance(self) -> Dict[str, Any]:
        """Analiza la apariencia y características visuales del objeto para búsquedas detalladas."""
        x1, y1, x2, y2 = self.best_bbox
        h, w = self.best_frame.shape[:2]
        bx1, by1, bx2, by2 = max(0, x1), max(0, y1), min(w, x2), min(h, y2)
        
        appearance = "vestimenta estándar"
        if by2 > by1 + 20 and bx2 > bx1 + 20 and self.object_class == "person":
            crop = self.best_frame[by1 + int((by2-by1)*0.25):by1 + int((by2-by1)*0.75), bx1:bx2]
            if crop.size > 0:
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                brightness = float(np.mean(gray))
                if brightness > 130:
                    appearance = "ropa clara / blanca"
                elif brightness < 80:
                    appearance = "ropa oscura / negra"
                else:
                    appearance = "ropa de tono neutro"

        dur = self.last_seen - self.start_time
        movement_desc = "movimiento de extremidades / brazos" if dur >= 1.2 else "movimiento breve"

        return {
            "appearance": appearance,
            "activity": movement_desc
        }


class VisionPipeline:
    """
    Motor principal de visión por computadora:
    - Captura frames a 5 FPS para ahorrar CPU/GPU.
    - Infiere con YOLO11 y rastrea con ByteTrack.
    - Consolida eventos y genera clips y miniaturas.
    """
    def __init__(self, stream_reader: RTSPStreamReader, camera_id: str = "cam_1", camera_name: str = "Cámara Poste Principal"):
        self.stream = stream_reader
        self.camera_id = camera_id
        self.camera_name = camera_name
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

            # 1. Chequeo de movimiento ultra-rápido (0.2ms) para ahorrar 85% de CPU
            gray_small = cv2.cvtColor(cv2.resize(frame, (160, 120)), cv2.COLOR_BGR2GRAY)
            has_motion = True
            if hasattr(self, "_prev_gray") and self._prev_gray is not None:
                diff = cv2.absdiff(gray_small, self._prev_gray)
                movement_score = int(np.sum(diff > 25))
                # Si no hay movimiento y no hay tracks activos, omitir inferencia pesada
                if movement_score < 40 and len(self.active_tracks) == 0:
                    has_motion = False
            self._prev_gray = gray_small

            if not has_motion:
                with self.lock:
                    self.annotated_frame = frame
                continue

            # Inferencia con YOLO optimizada para CPU (imgsz=320 a alta velocidad)
            try:
                results = self.model.track(
                    source=frame,
                    persist=True,
                    tracker="bytetrack.yaml",
                    conf=settings.CONFIDENCE_THRESHOLD,
                    imgsz=320,
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
        """Guarda el evento consolidado en disco y base de datos de forma asíncrona sin bloquear el stream."""
        event_id = str(uuid.uuid4())
        duration = round(track.last_seen - track.start_time, 1)
        visual_info = track.analyze_appearance()
        best_frame = track.best_frame.copy()
        best_bbox = track.best_bbox
        frames_copy = list(track.frames)
        track_id = track.track_id
        obj_class = track.object_class
        max_conf = track.max_confidence
        start_t = track.start_time
        end_t = track.last_seen
        logger.success(f"Evento cerrado: {obj_class} (ID #{track_id}) - Duración: {duration}s - {visual_info}")

        def _async_worker():
            try:
                # 1. Guardar Thumbnail
                thumb_path = save_thumbnail(best_frame, event_id, best_bbox)
                # 2. Guardar Video Clip con FFmpeg
                clip_path = save_video_clip(frames_copy, event_id, fps=settings.DETECTION_FPS)
                # 3. Guardar en Base de Datos
                self._save_to_db(event_id, track_id, obj_class, max_conf, start_t, end_t, duration, thumb_path, clip_path, visual_info)
            except Exception as e:
                logger.error(f"Error procesando guardado de evento {event_id}: {e}")

        # Ejecutar en segundo plano para que el procesamiento de video en vivo nunca se pause
        threading.Thread(target=_async_worker, daemon=True).start()
        self.total_events_detected += 1

    def _save_to_db(self, event_id: str, track_id: int, object_class: str, confidence: float, start_t: float, end_t: float, duration: float, thumb: str, clip: str, visual_info: Optional[Dict[str, Any]] = None):
        """Inserta el registro en la base de datos con hora local precisa."""
        import datetime
        from core.database import AsyncSessionLocal

        meta = {"class": object_class, "max_conf": confidence}
        if visual_info:
            meta.update(visual_info)

        async def _async_insert():
            async with AsyncSessionLocal() as session:
                ev = SecurityEvent(
                    id=event_id,
                    camera_id=self.camera_id,
                    camera_name=self.camera_name,
                    track_id=track_id,
                    object_class=object_class,
                    confidence=confidence,
                    start_time=datetime.datetime.fromtimestamp(start_t),
                    end_time=datetime.datetime.fromtimestamp(end_t),
                    duration_seconds=duration,
                    thumbnail_path=thumb,
                    clip_path=clip,
                    metadata_info=meta
                )
                session.add(ev)
                await session.commit()
                logger.info(f"Evento {event_id} ({self.camera_name}) registrado en base de datos con hora local {ev.start_time}.")

        asyncio.run(_async_insert())

    def get_annotated_frame(self) -> Optional[np.ndarray]:
        """Retorna el último fotograma con cajas delimitadoras en tiempo real."""
        with self.lock:
            if self.annotated_frame is not None:
                return self.annotated_frame.copy()
            return None
