import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Camera Settings
    CAMERA_IP: str = "192.168.100.209"
    CAMERA_PORT: int = 554
    CAMERA_USER: str = "admin"
    CAMERA_PASSWORD: str = "L27EA4F3"
    CAMERA_RTSP_MAIN: str = "rtsp://admin:L27EA4F3@192.168.100.209:554/cam/realmonitor?channel=1&subtype=0"
    CAMERA_RTSP_SUB: str = "rtsp://admin:L27EA4F3@192.168.100.209:554/cam/realmonitor?channel=1&subtype=1"

    # Database
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR / 'storage' / 'smart_cam.db'}"

    # Vision & AI
    YOLO_MODEL_NAME: str = "yolo11n.pt"
    DETECTION_FPS: int = 5
    CONFIDENCE_THRESHOLD: float = 0.40
    TRACKING_BUFFER_SECONDS: float = 3.0  # Seconds without seeing object before closing event
    MIN_EVENT_DURATION_SECONDS: float = 0.5

    # Production Cloud AI (Google Gemini Multimodal Vision)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Storage paths
    STORAGE_DIR: Path = BASE_DIR / "storage"
    THUMBNAILS_DIR: Path = BASE_DIR / "storage" / "thumbnails"
    CLIPS_DIR: Path = BASE_DIR / "storage" / "clips"

    # Ollama Local LLM (Fallback de Respaldo)
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"

    # Web Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
settings.THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)
settings.CLIPS_DIR.mkdir(parents=True, exist_ok=True)
