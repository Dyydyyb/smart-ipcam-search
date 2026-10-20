import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    track_id = Column(Integer, nullable=False, index=True)
    object_class = Column(String(50), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    
    start_time = Column(DateTime, nullable=False, index=True, default=datetime.now)
    end_time = Column(DateTime, nullable=False, default=datetime.now)
    duration_seconds = Column(Float, nullable=False, default=0.0)

    thumbnail_path = Column(String(255), nullable=True)
    clip_path = Column(String(255), nullable=True)
    
    # Detalle adicional: bounding box final, color aproximado, etc.
    metadata_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "track_id": self.track_id,
            "object_class": self.object_class,
            "confidence": round(self.confidence, 2),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": round(self.duration_seconds, 1),
            "thumbnail_url": f"/api/thumbnail/{self.id}" if self.thumbnail_path else None,
            "video_url": f"/api/video/{self.id}" if self.clip_path else None,
            "metadata": self.metadata_info or {}
        }
