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

    # Supabase Cloud Database & Auth
    SUPABASE_PROJECT_ID: str = "foghkrwrxqoqrkvdipnn"
    SUPABASE_URL: str = "https://foghkrwrxqoqrkvdipnn.supabase.co"
    SUPABASE_ANON_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZvZ2hrcndyeHFvcXJrdmRpcG5uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI4MDAxMDMsImV4cCI6MjEwODM3NjEwM30.gJgjTMIAGIsZjlnBhIKyQ9C16oprjwiyShJhND37YSM"
    SUPABASE_DB_URL: str = "postgresql://postgres.foghkrwrxqoqrkvdipnn:1569957772Db!@aws-0-us-east-1.pooler.supabase.com:5432/postgres?sslmode=require"
    JWT_SECRET: str = "baddgroup_master_jwt_key_2026_vision_ai_sec"

    # Vision & AI
    YOLO_MODEL_NAME: str = "yolo11n.pt"
    DETECTION_FPS: int = 5
    CONFIDENCE_THRESHOLD: float = 0.40
    TRACKING_BUFFER_SECONDS: float = 3.0  # Seconds without seeing object before closing event
    MIN_EVENT_DURATION_SECONDS: float = 0.5

    # Production Cloud AI (Google Gemini Multimodal Vision)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Storage paths & 24/7 Retention Policies
    STORAGE_DIR: Path = BASE_DIR / "storage"
    THUMBNAILS_DIR: Path = BASE_DIR / "storage" / "thumbnails"
    CLIPS_DIR: Path = BASE_DIR / "storage" / "clips"
    RETENTION_DAYS: int = 14
    MAX_STORAGE_GB: float = 40.0
    AUTO_CLEANUP_INTERVAL_MINUTES: int = 60

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
