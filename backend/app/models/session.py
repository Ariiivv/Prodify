import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Float, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class Session(Base):
    __tablename__ = "sessions"
    __table_args__ = (
        Index("ix_sessions_user_id_started_at", "user_id", "started_at"),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # core tracking
    duration_minutes = Column(Integer, nullable=False)

    # NEW: behavioral tracking (safe additive fields)
    focus_score = Column(Float, default=0.0)          # 0–100
    interruption_count = Column(Integer, default=0)    # simple signal
    pause_minutes = Column(Float, default=0.0)        # total paused time

    # timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)

    user = relationship("User", back_populates="sessions")
    task = relationship("Task", back_populates="sessions")