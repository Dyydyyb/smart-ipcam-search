import os
import io
import time
import datetime
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

import cv2
import numpy as np
from fastapi import FastAPI, Depends, Query, HTTPException, Response, status, Request, WebSocket, WebSocketDisconnect
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
from core.camera_manager import camera_manager
from core.crm_manager import crm_manager
from core import supabase_db
from engine.stream_capture import RTSPStreamReader
from engine.vision_pipeline import VisionPipeline
from engine.storage_manager import storage_manager
from backend.nlp_search import execute_smart_search

# Instancias globales de los motores
stream_reader = RTSPStreamReader(settings.CAMERA_RTSP_SUB, name="Substream-AI", target_fps=settings.DETECTION_FPS)
vision_pipeline = VisionPipeline(stream_reader)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación: inicializa DB y workers en segundo plano."""
    logger.info("Iniciando Smart IP Cam Search Platform...")
    await init_db()
    
    # Iniciar captura de stream, visión artificial y retención de disco 24/7
    stream_reader.start()
    vision_pipeline.start()
    storage_manager.start()
    
    yield
    
    # Detener workers al apagar
    logger.info("Deteniendo workers de captura, visión y retención...")
    storage_manager.stop()
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
    camera_id: Optional[str] = None

class BatchDeleteRequest(BaseModel):
    event_ids: List[str]

class AddCameraRequest(BaseModel):
    name: str
    location: Optional[str] = "General"
    ip: str
    port: int = 554
    user: str = "admin"
    password: str = ""
    rtsp_sub: Optional[str] = None
    rtsp_main: Optional[str] = None

class CreateClientRequest(BaseModel):
    name: str
    business_type: Optional[str] = "Comercio / Local"
    phone: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""
    notes: Optional[str] = ""
    installation_cost: float = 0.0
    installation_paid: float = 0.0
    monthly_fee: float = 0.0
    billing_day: int = 10
    payment_method: Optional[str] = "Efectivo"
    service_status: Optional[str] = "activo"
    client_user: Optional[str] = ""
    client_pass: Optional[str] = ""
    cameras: Optional[List[Dict[str, Any]]] = []

class UpdateClientRequest(BaseModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    installation_cost: Optional[float] = None
    installation_paid: Optional[float] = None
    monthly_fee: Optional[float] = None
    billing_day: Optional[int] = None
    service_status: Optional[str] = None
    client_user: Optional[str] = None
    client_pass: Optional[str] = None
    cameras: Optional[List[Dict[str, Any]]] = None

class LoginRequest(BaseModel):
    username: str
    password: str
    expected_role: Optional[str] = None

class RecordPaymentRequest(BaseModel):
    payment_type: str  # 'cuota' o 'instalacion'
    amount: float
    method: Optional[str] = "Transferencia"
    period: Optional[str] = None
    notes: Optional[str] = ""

class CreateSoftwareSaleRequest(BaseModel):
    buyer_name: str
    buyer_company: Optional[str] = ""
    buyer_contact: Optional[str] = ""
    buyer_email: Optional[str] = ""
    license_plan: Optional[str] = "Licencia Servidor Pro (On-Premise)"
    licenses_count: Optional[int] = 1
    price: float
    amount_paid: Optional[float] = 0.0
    currency: Optional[str] = "ARS"
    payment_model: Optional[str] = "Pago Único Perpetuo"
    payment_method: Optional[str] = "Transferencia Bancaria"
    payment_status: Optional[str] = "pagado"
    license_key: Optional[str] = ""
    date: Optional[str] = None
    notes: Optional[str] = ""

class UpdateSoftwareSaleRequest(BaseModel):
    buyer_name: Optional[str] = None
    buyer_company: Optional[str] = None
    buyer_contact: Optional[str] = None
    buyer_email: Optional[str] = None
    license_plan: Optional[str] = None
    licenses_count: Optional[int] = None
    price: Optional[float] = None
    amount_paid: Optional[float] = None
    currency: Optional[str] = None
    payment_model: Optional[str] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    license_key: Optional[str] = None
    notes: Optional[str] = None

class RecordSoftwarePaymentRequest(BaseModel):
    amount: float
    method: Optional[str] = "Transferencia Bancaria"
    notes: Optional[str] = ""

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Sirve la interfaz web principal."""
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Smart IP Camera AI Search</h1><p>Frontend no encontrado en frontend/index.html</p>")

@app.get("/login", response_class=HTMLResponse)
async def serve_login():
    """Sirve la página de inicio de sesión de Baddgroup."""
    login_file = frontend_dir / "login.html"
    if login_file.exists():
        return HTMLResponse(content=login_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Baddgroup Login</h1><p>Archivo no encontrado en frontend/login.html</p>", status_code=404)

def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    """Extrae y verifica el usuario autenticado desde header Authorization o cookie."""
    auth_header = request.headers.get("Authorization")
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    if not token:
        token = request.cookies.get("baddgroup_token")
    if not token:
        return None
    return supabase_db.verify_token(token)

def require_admin(request: Request) -> Dict[str, Any]:
    user = get_current_user(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acceso denegado. Se requiere cuenta de Administrador.")
    return user

@app.post("/api/auth/login")
async def auth_login(req: LoginRequest, response: Response):
    """Autentica credenciales en Supabase y emite token JWT firmado."""
    user = supabase_db.authenticate_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    if req.expected_role and req.expected_role == "admin" and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Esta cuenta no posee privilegios de Administrador del CRM")

    token = supabase_db.generate_token(user)
    
    response.set_cookie(
        key="baddgroup_token",
        value=token,
        max_age=86400 * 7,
        httponly=False,
        samesite="lax",
        secure=False
    )
    
    return {
        "status": "ok",
        "token": token,
        "user": user,
        "redirect": "/crm" if user.get("role") == "admin" else "/"
    }

@app.get("/api/auth/me")
async def auth_me(request: Request):
    """Retorna los datos del usuario logueado actualmente."""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Sesión no iniciada o token expirado")
    return {"status": "ok", "user": user}

@app.post("/api/auth/logout")
async def auth_logout(response: Response):
    """Cierra la sesión activa borrando la cookie de autenticación."""
    response.delete_cookie("baddgroup_token")
    return {"status": "ok", "message": "Sesión cerrada correctamente"}

@app.get("/api/status")
async def get_system_status(request: Request, db: AsyncSession = Depends(get_db)):
    """Retorna el estado de la cámara, motor de IA y conteo de eventos."""
    total_events_query = await db.execute(select(SecurityEvent))
    events_count = len(total_events_query.scalars().all())

    user = get_current_user(request)
    primary_cam = None
    cameras_count = 0
    if user:
        try:
            supabase_cams = supabase_db.get_cameras_for_user(user)
            if supabase_cams:
                primary_cam = supabase_cams[0]
                cameras_count = len(supabase_cams)
        except Exception:
            pass

    if not primary_cam:
        cameras = camera_manager.get_all()
        primary_cam = cameras[0] if cameras else {}
        cameras_count = len(cameras)

    cam_id = primary_cam.get("id", "")
    cam_name = primary_cam.get("name", "Cámara de Seguridad")

    ai_mode = "Gemini 1.5 Flash (Visión Multimodal)" if bool(settings.GEMINI_API_KEY) else f"Qwen 2.5 ({settings.OLLAMA_MODEL} Local)"
    is_connected = stream_reader.connected if (stream_reader.connected and cam_id) else False

    return {
        "camera": {
            "id": cam_id,
            "name": cam_name,
            "ip": primary_cam.get("ip", ""),
            "safety_code": primary_cam.get("safety_code", ""),
            "connected": is_connected,
            "width": stream_reader.width if is_connected else 640,
            "height": stream_reader.height if is_connected else 480,
            "fps": round(stream_reader.fps, 1) if is_connected else 15.0,
            "detection_fps": settings.DETECTION_FPS
        },
        "ai_engine": {
            "name": ai_mode,
            "provider": "gemini" if bool(settings.GEMINI_API_KEY) else "ollama",
            "model": settings.GEMINI_MODEL if bool(settings.GEMINI_API_KEY) else settings.OLLAMA_MODEL,
            "multimodal": bool(settings.GEMINI_API_KEY)
        },
        "cameras_count": cameras_count,
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
    request: Request,
    limit: int = 50,
    offset: int = 0,
    object_class: Optional[str] = None,
    camera_id: Optional[str] = None,
    all: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """Lista los eventos registrados con filtros opcionales de clase y cámara."""
    user = get_current_user(request)
    allowed_cam_ids = None
    if user and user.get("role") == "client":
        try:
            cams = supabase_db.get_cameras_for_user(user)
            allowed_cam_ids = [c["id"] for c in cams]
        except Exception:
            pass

    stmt = select(SecurityEvent).order_by(desc(SecurityEvent.start_time))
    if object_class:
        stmt = stmt.where(SecurityEvent.object_class == object_class)
        
    if camera_id and camera_id != "all":
        stmt = stmt.where(SecurityEvent.camera_id == camera_id)
    elif allowed_cam_ids is not None:
        if allowed_cam_ids:
            stmt = stmt.where(SecurityEvent.camera_id.in_(allowed_cam_ids))
        else:
            return []
            
    if not all:
        stmt = stmt.limit(limit).offset(offset)
    
    result = await db.execute(stmt)
    events = result.scalars().all()
    return [e.to_dict() for e in events]

@app.delete("/api/events/{event_id}")
async def delete_single_event(event_id: str, db: AsyncSession = Depends(get_db)):
    """Elimina una grabación individual por su ID, removiendo también sus archivos en disco."""
    stmt = select(SecurityEvent).where(SecurityEvent.id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Grabación no encontrada")
        
    # Borrar archivos físicos
    if event.thumbnail_path and os.path.exists(event.thumbnail_path):
        try:
            os.remove(event.thumbnail_path)
        except Exception as e:
            logger.warning(f"No se pudo borrar thumbnail {event.thumbnail_path}: {e}")
            
    if event.clip_path and os.path.exists(event.clip_path):
        try:
            os.remove(event.clip_path)
        except Exception as e:
            logger.warning(f"No se pudo borrar clip {event.clip_path}: {e}")
            
    await db.delete(event)
    await db.commit()
    return {"status": "ok", "deleted_id": event_id}

@app.post("/api/events/batch-delete")
async def delete_events_batch(req: BatchDeleteRequest, db: AsyncSession = Depends(get_db)):
    """Elimina un conjunto de grabaciones seleccionadas por sus IDs."""
    if not req.event_ids:
        return {"status": "ok", "deleted_count": 0}
        
    stmt = select(SecurityEvent).where(SecurityEvent.id.in_(req.event_ids))
    result = await db.execute(stmt)
    events = result.scalars().all()
    
    deleted_count = 0
    for ev in events:
        if ev.thumbnail_path and os.path.exists(ev.thumbnail_path):
            try:
                os.remove(ev.thumbnail_path)
            except Exception:
                pass
        if ev.clip_path and os.path.exists(ev.clip_path):
            try:
                os.remove(ev.clip_path)
            except Exception:
                pass
        await db.delete(ev)
        deleted_count += 1
        
    await db.commit()
    return {"status": "ok", "deleted_count": deleted_count}

@app.delete("/api/events")
async def delete_events_filtered_or_all(
    object_class: Optional[str] = None,
    delete_all: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """Elimina grabaciones por filtro de clase o todo el historial completo."""
    if not delete_all and not object_class:
        raise HTTPException(status_code=400, detail="Especifique un filtro de clase o delete_all=true")
        
    stmt = select(SecurityEvent)
    if object_class:
        stmt = stmt.where(SecurityEvent.object_class == object_class)
        
    result = await db.execute(stmt)
    events = result.scalars().all()
    
    deleted_count = 0
    for ev in events:
        if ev.thumbnail_path and os.path.exists(ev.thumbnail_path):
            try:
                os.remove(ev.thumbnail_path)
            except Exception:
                pass
        if ev.clip_path and os.path.exists(ev.clip_path):
            try:
                os.remove(ev.clip_path)
            except Exception:
                pass
        await db.delete(ev)
        deleted_count += 1
        
    await db.commit()
    return {"status": "ok", "deleted_count": deleted_count, "filter": object_class or "all"}

@app.post("/api/search")
async def search_events(req: SearchRequest, db: AsyncSession = Depends(get_db)):
    """Ejecuta una búsqueda en lenguaje natural interpretada por el LLM para una cámara específica."""
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="La consulta no puede estar vacía")
    
    if not req.camera_id or req.camera_id.strip().lower() in ("all", "todas", "null", "none", ""):
        raise HTTPException(
            status_code=400,
            detail="Debes seleccionar una cámara en específico para buscar el evento con IA. La búsqueda simultánea en todas las cámaras no está permitida."
        )
    
    results = await execute_smart_search(db, query, camera_id=req.camera_id.strip())
    return results

@app.post("/api/stream/push")
async def push_stream_frame(request: Request):
    """Recibe fotogramas de cámaras remotas a través del canal encriptado HTTPS."""
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="Empty frame")
    
    nparr = np.frombuffer(body, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is not None:
        stream_reader.push_frame(frame)
        return {"status": "ok", "received": True}
    raise HTTPException(status_code=400, detail="Invalid image frame")

@app.websocket("/api/stream/ws")
async def stream_ws_ingest(websocket: WebSocket):
    """Canal WebSocket de ultra-baja latencia (15ms) para ingesta de video desde cámaras remotas."""
    await websocket.accept()
    logger.info("Cámara remota conectada vía WebSocket Bridge.")
    try:
        while True:
            data = await websocket.receive_bytes()
            if data:
                nparr = np.frombuffer(data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is not None:
                    stream_reader.push_frame(frame)
    except WebSocketDisconnect:
        logger.warning("Cámara remota desconectada del WebSocket Bridge.")
    except Exception as e:
        logger.error(f"Error en WebSocket Bridge: {e}")

def to_ascii_banner(text: str) -> str:
    import unicodedata
    if not text:
        return ""
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii').upper()

@app.get("/api/live")
def live_stream(request: Request, camera_id: Optional[str] = None):
    """Genera un stream MJPEG con detección en tiempo real para la cámara solicitada."""
    target_cam_id = camera_id

    def generate_mjpeg():
        while True:
            frame = None
            cam_info = None

            if target_cam_id and target_cam_id != "all":
                try:
                    cam_info = supabase_db.get_camera_by_id(target_cam_id)
                except Exception:
                    pass
                if not cam_info:
                    cam_info = camera_manager.get(target_cam_id)
            else:
                user = get_current_user(request)
                if user:
                    try:
                        user_cams = supabase_db.get_cameras_for_user(user)
                        if user_cams:
                            cam_info = user_cams[0]
                    except Exception:
                        pass
                if not cam_info:
                    cams = camera_manager.get_all()
                    if cams:
                        cam_info = cams[0]

            # Si el stream físico está conectado
            if stream_reader.connected:
                frame = vision_pipeline.get_annotated_frame()
                if frame is None:
                    ret, raw, _ = stream_reader.get_latest_frame()
                    frame = raw if ret and raw is not None else None

            # Render de standby Baddgroup si aún no hay flujo directo de video
            if frame is None:
                cam_name = cam_info.get("name", "Cámara de Seguridad") if cam_info else "Cámara de Seguridad"
                cam_code = cam_info.get("safety_code", "") if cam_info else ""
                cam_serial = cam_info.get("serial_number", "") if cam_info else ""
                cam_ip = cam_info.get("ip", "") if cam_info else ""

                canvas = np.zeros((480, 640, 3), dtype=np.uint8)
                canvas[:] = (15, 23, 42) # Slate-900

                banner_text = f"BADDGROUP VISION - {to_ascii_banner(cam_name)}"
                cv2.putText(canvas, banner_text, (25, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (248, 250, 252), 2)
                
                details = f"SAFETY CODE: {cam_code}" if cam_code else (f"IP: {cam_ip}" if cam_ip else "STREAM P2P")
                if cam_serial:
                    details += f" | S/N: {cam_serial}"
                cv2.putText(canvas, details, (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (59, 130, 246), 1)

                cv2.putText(canvas, "ESTADO: ESPERANDO TRANSMISION DE VIDEO", (25, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (245, 158, 11), 1)
                cv2.putText(canvas, "CANAL ENCRIPTADO P2P LISTO PARA RECIBIR", (25, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (148, 163, 184), 1)

                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(canvas, f"MONITOREO BADDGROUP 24/7 | {now_str}", (25, 435), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (16, 185, 129), 1)
                frame = canvas

            if frame is not None:
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

@app.get("/api/events/from_moment/{event_id}")
async def get_events_from_moment(event_id: str, db: AsyncSession = Depends(get_db)):
    """Obtiene el evento indicado y todos los eventos cronológicamente posteriores para reproducción continua."""
    stmt = select(SecurityEvent).where(SecurityEvent.id == event_id)
    result = await db.execute(stmt)
    start_event = result.scalar_one_or_none()
    
    if not start_event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
        
    subsequent_stmt = (
        select(SecurityEvent)
        .where(SecurityEvent.start_time >= start_event.start_time)
        .order_by(SecurityEvent.start_time.asc())
        .limit(30)
    )
    sub_res = await db.execute(subsequent_stmt)
    events = sub_res.scalars().all()
    ordered = [start_event] + [e for e in events if e.id != start_event.id]
    return [e.to_dict() for e in ordered]

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

    now = datetime.datetime.now()
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

@app.get("/api/cameras")
async def get_cameras(request: Request):
    """Retorna la lista de cámaras IP configuradas, filtrando por cliente si corresponde."""
    user = get_current_user(request)
    if user:
        try:
            supabase_cams = supabase_db.get_cameras_for_user(user)
            if user.get("role") == "client":
                for c in supabase_cams:
                    c["connected"] = True if c.get("stream_url") or c.get("rtsp_sub") or c.get("ip") else False
                return supabase_cams

            if supabase_cams:
                for c in supabase_cams:
                    c["connected"] = True if c.get("stream_url") or c.get("rtsp_sub") or c.get("ip") else False
                return supabase_cams
        except Exception as e:
            logger.warning(f"Error cargando cámaras de Supabase: {e}")

    # Fallback local
    cams = camera_manager.get_all()
    for c in cams:
        if c.get("id") == "cam_1":
            c["connected"] = stream_reader.connected
        else:
            c["connected"] = False
    return cams

@app.post("/api/cameras")
async def add_camera(req: AddCameraRequest):
    """Registra una nueva cámara IP en el sistema para distribución."""
    if not req.name or not req.ip:
        raise HTTPException(status_code=400, detail="El nombre y la dirección IP son requeridos")
    new_cam = camera_manager.add(
        name=req.name,
        location=req.location or "General",
        ip=req.ip,
        port=req.port,
        user=req.user,
        password=req.password,
        rtsp_sub=req.rtsp_sub,
        rtsp_main=req.rtsp_main
    )
    # Registrar también en Supabase si está disponible
    try:
        supabase_db.add_camera_supabase({
            "name": req.name,
            "location": req.location,
            "ip": req.ip,
            "port": req.port,
            "user": req.user,
            "rtsp_sub": req.rtsp_sub,
            "rtsp_main": req.rtsp_main
        })
    except Exception as e:
        logger.warning(f"No se pudo sincronizar cámara a Supabase: {e}")
        
    return {"status": "ok", "camera": new_cam}

@app.delete("/api/cameras/{cam_id}")
async def delete_camera(cam_id: str):
    """Elimina una cámara registrada."""
    if cam_id == "cam_1" and len(camera_manager.get_all()) <= 1:
        raise HTTPException(status_code=400, detail="No se puede eliminar la cámara principal predeterminada.")
    success = camera_manager.delete(cam_id)
    try:
        supabase_db.delete_camera_supabase(cam_id)
    except Exception:
        pass
    if not success:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    return {"status": "ok", "deleted_id": cam_id}

@app.get("/api/storage")
async def get_storage_stats():
    """Retorna métricas de uso de disco y políticas de retención 24/7."""
    return storage_manager.get_storage_stats()

@app.post("/api/storage/cleanup")
async def trigger_storage_cleanup():
    """Ejecuta purga manual preventiva de grabaciones vencidas o exceso de GB."""
    result = await storage_manager.run_retention_cleanup()
    return {"status": "ok", "result": result}

# ==========================================
# CRM & DASHBOARD DE FACTURACIÓN BADDGROUP (SUPABASE POSTGRESQL)
# ==========================================
@app.get("/crm", response_class=HTMLResponse)
async def serve_crm():
    """Sirve la interfaz web del CRM y panel de facturación de Baddgroup."""
    crm_file = frontend_dir / "crm.html"
    if crm_file.exists():
        return HTMLResponse(content=crm_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Baddgroup CRM</h1><p>Panel no encontrado en frontend/crm.html</p>", status_code=404)

@app.get("/api/crm/stats")
async def get_crm_stats():
    """Retorna las métricas financieras globales, MRR y conteo de clientes desde Supabase."""
    return supabase_db.get_dashboard_stats()

@app.get("/api/crm/clients")
async def get_crm_clients(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query("all")
):
    """Lista todos los clientes con filtros por búsqueda o estado desde Supabase."""
    return supabase_db.get_clients(search=search, status=status)

@app.get("/api/crm/clients/{client_id}")
async def get_crm_client(client_id: str):
    """Obtiene los detalles completos de un cliente específico desde Supabase."""
    client = supabase_db.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@app.post("/api/crm/clients")
async def create_crm_client(req: CreateClientRequest):
    """Registra un nuevo cliente con sus cámaras, cuotas y credenciales en Supabase."""
    if not req.name or not req.name.strip():
        raise HTTPException(status_code=400, detail="El nombre del cliente es obligatorio")
    data = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    new_client = supabase_db.create_client(data)
    return {"status": "ok", "client": new_client}

@app.put("/api/crm/clients/{client_id}")
async def update_crm_client(client_id: str, req: UpdateClientRequest):
    """Actualiza datos del cliente, cuotas, estado o cámaras en Supabase."""
    raw_data = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    clean_data = {k: v for k, v in raw_data.items() if v is not None}
    updated = supabase_db.update_client(client_id, clean_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"status": "ok", "client": updated}

@app.delete("/api/crm/clients/{client_id}")
async def delete_crm_client(client_id: str):
    """Elimina un cliente del CRM en Supabase."""
    success = supabase_db.delete_client(client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"status": "ok", "deleted_id": client_id}

@app.post("/api/crm/clients/{client_id}/payment")
async def record_client_payment(client_id: str, req: RecordPaymentRequest):
    """Registra un pago de cuota mensual o saldo de instalación en Supabase."""
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="El monto del pago debe ser mayor a 0")
    result = supabase_db.record_client_payment(
        client_id=client_id,
        payment_type=req.payment_type,
        amount=req.amount,
        method=req.method or "Transferencia",
        period=req.period or "",
        notes=req.notes or ""
    )
    if not result:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"status": "ok", "result": result}

@app.post("/api/crm/clients/{client_id}/toggle-status")
async def toggle_client_status(client_id: str):
    """Suspende o activa el servicio de un cliente en Supabase."""
    updated = supabase_db.toggle_client_status(client_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"status": "ok", "client": updated}

# ==========================================
# BALANCE FINANCIERO & GRÁFICOS (SUPABASE)
# ==========================================
@app.get("/api/crm/balance-charts")
async def get_balance_charts():
    """Retorna series históricas y composición porcentual de ingresos para gráficos desde Supabase."""
    return supabase_db.get_balance_charts()

# ==========================================
# VENTAS DE SOFTWARE & LICENCIAS (SUPABASE)
# ==========================================
@app.get("/api/crm/software-sales")
async def get_software_sales(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query("all")
):
    """Lista las ventas de software con filtros por búsqueda o estado de cobro desde Supabase."""
    return supabase_db.get_software_sales(search=search, status=status)

@app.get("/api/crm/software-sales/{sale_id}")
async def get_software_sale(sale_id: str):
    """Obtiene los detalles de una venta de software específica desde Supabase."""
    sale = supabase_db.get_software_sale(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venta de software no encontrada")
    return sale

@app.post("/api/crm/software-sales")
async def create_software_sale(req: CreateSoftwareSaleRequest):
    """Registra una nueva venta de software, emite clave de licencia y asienta el valor en Supabase."""
    if not req.buyer_name or not req.buyer_name.strip():
        raise HTTPException(status_code=400, detail="El nombre del comprador es obligatorio")
    data = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    new_sale = supabase_db.create_software_sale(data)
    return {"status": "ok", "sale": new_sale}

@app.put("/api/crm/software-sales/{sale_id}")
async def update_software_sale(sale_id: str, req: UpdateSoftwareSaleRequest):
    """Actualiza los datos o montos de una venta de software en Supabase."""
    raw_data = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    clean_data = {k: v for k, v in raw_data.items() if v is not None}
    updated = supabase_db.update_software_sale(sale_id, clean_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Venta de software no encontrada")
    return {"status": "ok", "sale": updated}

@app.delete("/api/crm/software-sales/{sale_id}")
async def delete_software_sale(sale_id: str):
    """Elimina una venta de software en Supabase."""
    success = supabase_db.delete_software_sale(sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Venta de software no encontrada")
    return {"status": "ok", "deleted_id": sale_id}

@app.post("/api/crm/software-sales/{sale_id}/payment")
async def record_software_sale_payment(sale_id: str, req: RecordSoftwarePaymentRequest):
    """Asienta un cobro total o parcial (saldo/seña) de una venta de software en Supabase."""
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="El monto del cobro debe ser mayor a 0")
    result = supabase_db.record_software_payment(
        sale_id=sale_id,
        amount=req.amount,
        method=req.method or "Transferencia Bancaria",
        notes=req.notes or ""
    )
    if not result:
        raise HTTPException(status_code=404, detail="Venta de software no encontrada")
    return {"status": "ok", "sale": result}



