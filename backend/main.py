import os
import io
import time
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

import cv2
from fastapi import FastAPI, Depends, Query, HTTPException, Response, status
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from loguru import logger

from core.config import settings
from core.database import init_db, get_db, AsyncSessionLocal
from core.models import SecurityEvent
from engine.stream_capture import RTSPStreamReader
from engine.vision_pipeline import VisionPipeline
from backend.nlp_search import execute_smart_search

# Instancias globales de los motores
stream_reader = RTSPStreamReader(settings.CAMERA_RTSP_SUB, name="Substream-AI", target_fps=settings.DETECTION_FPS)
vision_pipeline = VisionPipeline(stream_reader)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación: inicializa DB y workers en segundo plano."""
    logger.info("Iniciando Smart IP Cam Search Platform...")
    await init_db()
    
    # Iniciar captura de stream y visión artificial
    stream_reader.start()
    vision_pipeline.start()
    
    yield
    
    # Detener workers al apagar
    logger.info("Deteniendo workers de captura y visión...")
    vision_pipeline.stop()
    stream_reader.stop()

app = FastAPI(
    title="Smart IP Camera AI Search",
    description="Plataforma de búsqueda inteligente para cámaras IP mediante IA local y visión por computadora.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos del frontend
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

class SearchRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Sirve la interfaz web principal."""
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Smart IP Camera AI Search</h1><p>Frontend no encontrado en frontend/index.html</p>")

@app.get("/api/status")
async def get_system_status(db: AsyncSession = Depends(get_db)):
    """Retorna el estado de la cámara, FPS de detección y conteo de eventos."""
    total_events_query = await db.execute(select(SecurityEvent))
    events_count = len(total_events_query.scalars().all())

    return {
        "camera": {
            "ip": settings.CAMERA_IP,
            "connected": stream_reader.connected,
            "width": stream_reader.width,
            "height": stream_reader.height,
            "fps": round(stream_reader.fps, 1),
            "detection_fps": settings.DETECTION_FPS
        },
        "vision": {
            "model": settings.YOLO_MODEL_NAME,
            "active_tracks": len(vision_pipeline.active_tracks),
            "total_detected_runtime": vision_pipeline.total_events_detected
        },
        "database": {
            "total_events_saved": events_count
        }
    }

@app.get("/api/events")
async def get_events(
    limit: int = 50,
    offset: int = 0,
    object_class: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Lista los eventos registrados con filtros opcionales."""
    stmt = select(SecurityEvent).order_by(desc(SecurityEvent.start_time)).limit(limit).offset(offset)
    if object_class:
        stmt = stmt.where(SecurityEvent.object_class == object_class)
    
    result = await db.execute(stmt)
    events = result.scalars().all()
    return [e.to_dict() for e in events]

@app.post("/api/search")
async def search_events(req: SearchRequest, db: AsyncSession = Depends(get_db)):
    """Ejecuta una búsqueda en lenguaje natural interpretada por el LLM."""
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="La consulta no puede estar vacía")
    
    results = await execute_smart_search(db, query)
    return results

@app.get("/api/live")
def live_stream():
    """Genera un stream MJPEG con las cajas delimitadoras de detección en tiempo real."""
    def generate_mjpeg():
        while True:
            frame = vision_pipeline.get_annotated_frame()
            if frame is None:
                ret, raw, _ = stream_reader.get_latest_frame()
                frame = raw if ret and raw is not None else None

            if frame is not None:
                # Codificar a JPEG
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(1.0 / max(1, settings.DETECTION_FPS))

    return StreamingResponse(generate_mjpeg(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/api/thumbnail/{event_id}")
async def get_thumbnail(event_id: str, db: AsyncSession = Depends(get_db)):
    """Sirve la imagen miniatura del evento."""
    stmt = select(SecurityEvent).where(SecurityEvent.id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    
    if not event or not event.thumbnail_path or not os.path.exists(event.thumbnail_path):
        raise HTTPException(status_code=404, detail="Thumbnail no encontrado")
        
    return FileResponse(event.thumbnail_path, media_type="image/jpeg")

@app.get("/api/video/{event_id}")
async def get_video(event_id: str, db: AsyncSession = Depends(get_db)):
    """Sirve el clip de video .mp4 del evento."""
    stmt = select(SecurityEvent).where(SecurityEvent.id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    
    if not event or not event.clip_path or not os.path.exists(event.clip_path):
        raise HTTPException(status_code=404, detail="Clip de video no encontrado")
        
    return FileResponse(event.clip_path, media_type="video/mp4")

@app.post("/api/create_demo_event")
async def create_demo_event(db: AsyncSession = Depends(get_db)):
    """Crea un evento de demostración inmediato usando el snapshot capturado para probar la UI."""
    import uuid
    import datetime
    from engine.video_recorder import save_thumbnail, save_video_clip

    event_id = str(uuid.uuid4())
    snapshot_path = Path("snapshots/camera_test.jpg")
    
    if snapshot_path.exists():
        frame = cv2.imread(str(snapshot_path))
    else:
        ret, frame, _ = stream_reader.get_latest_frame()
        if not ret or frame is None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)

    # Crear thumbnail y clip simulado de 30 frames
    thumb_path = save_thumbnail(frame, event_id, bbox=(120, 80, 520, 400))
    clip_frames = [frame.copy() for _ in range(30)]
    clip_path = save_video_clip(clip_frames, event_id, fps=15.0)

    now = datetime.datetime.utcnow()
    ev = SecurityEvent(
        id=event_id,
        track_id=101,
        object_class="person",
        confidence=0.92,
        start_time=now - datetime.timedelta(seconds=12),
        end_time=now,
        duration_seconds=12.0,
        thumbnail_path=thumb_path,
        clip_path=clip_path,
        metadata_info={"class": "person", "max_conf": 0.92, "demo": True}
    )
    db.add(ev)
    await db.commit()
    return {"status": "ok", "event_id": event_id, "event": ev.to_dict()}

