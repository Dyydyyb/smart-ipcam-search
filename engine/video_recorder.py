import os
import cv2
import subprocess
import numpy as np
from pathlib import Path
from typing import List, Tuple
from loguru import logger
from core.config import settings

def save_thumbnail(frame: np.ndarray, event_id: str, bbox: tuple = None) -> str:
    """
    Guarda una imagen en miniatura para el evento.
    Si se proporciona bbox (x1, y1, x2, y2), dibuja el cuadro de detección
    o resalta el objeto.
    """
    thumb_path = settings.THUMBNAILS_DIR / f"{event_id}.jpg"
    display_frame = frame.copy()

    if bbox is not None:
        x1, y1, x2, y2 = [int(v) for v in bbox]
        # Dibujar cuadro delimitador estético (verde / cian)
        cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 180), 2)

    cv2.imwrite(str(thumb_path), display_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return str(thumb_path)

def save_video_clip(frames: List[np.ndarray], event_id: str, fps: float = 15.0) -> str:
    """
    Guarda una lista de frames como video .mp4 compatible con navegadores web
    usando FFmpeg con codec H.264 (yuv420p) y flag faststart para streaming fluido.
    """
    if not frames:
        return ""

    raw_path = settings.CLIPS_DIR / f"{event_id}_raw.mp4"
    final_path = settings.CLIPS_DIR / f"{event_id}.mp4"

    height, width, _ = frames[0].shape
    effective_fps = max(5.0, min(float(fps), 30.0))

    # 1. Escribir archivo temporal con OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(raw_path), fourcc, effective_fps, (width, height))
    for f in frames:
        out.write(f)
    out.release()

    # 2. Transcodificar a H.264 web-standard usando FFmpeg
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_path),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "24",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(final_path)
        ]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
        if result.returncode == 0 and final_path.exists():
            if raw_path.exists():
                raw_path.unlink()
            logger.info(f"Clip de video guardado y optimizado en: {final_path.name}")
            return str(final_path)
    except Exception as e:
        logger.warning(f"Error al transcodificar con FFmpeg: {e}. Usando video directo.")

    # Fallback si falla FFmpeg
    if raw_path.exists():
        raw_path.rename(final_path)
    return str(final_path)
