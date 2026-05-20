import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)

    user = relationship("User", back_populates="sessions")
    task = relationship("Task", back_populates="sessions")