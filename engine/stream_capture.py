import os
import time
import threading
from collections import deque
from typing import Optional, Tuple, List
import cv2
import numpy as np
from loguru import logger

# Configurar transporte TCP y timeout de 5 segundos para reconexión infalible 24/7
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|stimeout;5000000"

class RTSPStreamReader:
    """
    Lector de stream RTSP asíncrono y resiliente en un hilo independiente.
    Mantiene el último cuadro con cero latencia y un buffer circular de los
    últimos N segundos para pre-roll de eventos.
    """
    def __init__(self, rtsp_url: str, name: str = "Stream", buffer_seconds: int = 15, target_fps: int = 15):
        self.rtsp_url = rtsp_url
        self.name = name
        self.buffer_seconds = buffer_seconds
        self.target_fps = target_fps
        self.max_buffer_len = buffer_seconds * target_fps

        self.cap: Optional[cv2.VideoCapture] = None
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

        self.latest_frame: Optional[np.ndarray] = None
        self.latest_timestamp: float = 0.0
        self.frame_buffer: deque = deque(maxlen=self.max_buffer_len)

        self.connected = False
        self.fps = 15.0
        self.width = 640
        self.height = 480

    def start(self):
        """Inicia el hilo de lectura del stream."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, name=f"RTSP-{self.name}", daemon=True)
        self.thread.start()
        logger.info(f"[{self.name}] Hilo de captura RTSP iniciado.")

    def stop(self):
        """Detiene el hilo de lectura."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        if self.cap:
            self.cap.release()
        self.connected = False
        logger.info(f"[{self.name}] Hilo de captura detenido.")

    def _connect(self) -> bool:
        """Intenta abrir la conexión RTSP."""
        logger.info(f"[{self.name}] Conectando a {self.rtsp_url.split('@')[-1]}...")
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass

        self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        if not self.cap.isOpened():
            logger.warning(f"[{self.name}] Falló al abrir el stream RTSP.")
            self.connected = False
            return False

        self.connected = True
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if w > 0 and h > 0:
            self.width = w
            self.height = h
        if fps > 0:
            self.fps = fps
        logger.success(f"[{self.name}] Conectado exitosamente ({self.width}x{self.height} @ {self.fps:.1f} FPS).")
        return True

    def _capture_loop(self):
        """Bucle principal de lectura continua de frames."""
        retry_delay = 2.0
        while self.running:
            if not self.connected:
                if not self._connect():
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 1.5, 30.0)
                    continue
                retry_delay = 2.0

            ret, frame = self.cap.read()
            if not ret or frame is None:
                logger.warning(f"[{self.name}] Pérdida de señal o fin de stream. Reconectando...")
                self.connected = False
                if self.cap:
                    try:
                        self.cap.release()
                    except Exception:
                        pass
                    self.cap = None
                time.sleep(1.0)
                continue

            now = time.time()
            with self.lock:
                self.latest_frame = frame
                self.latest_timestamp = now
                self.frame_buffer.append((now, frame))

    def get_latest_frame(self) -> Tuple[bool, Optional[np.ndarray], float]:
        """Retorna el frame más reciente sin latencia."""
        with self.lock:
            if self.latest_frame is not None:
                return True, self.latest_frame.copy(), self.latest_timestamp
            return False, None, 0.0

    def get_buffer_snapshot(self) -> List[Tuple[float, np.ndarray]]:
        """Retorna una copia de los frames almacenados en el buffer."""
        with self.lock:
            return list(self.frame_buffer)
