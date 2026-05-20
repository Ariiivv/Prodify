import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class BehavioralState(Base):
    __tablename__ = "behavioral_states"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)

    # core computed intelligence signals (derived later from sessions)
    focus_consistency_score = Column(Float, default=0.0)  # stability across sessions
    burnout_risk_score = Column(Float, default=0.0)       # fatigue + inconsistency
    efficiency_score = Column(Float, default=0.0)         # output per time
    predicted_daily_capacity_minutes = Column(Float, default=0.0)

    # NEW: behavioral aggregates (still lightweight, no AI required)
    total_sessions = Column(Integer, default=0)
    total_focus_minutes = Column(Integer, default=0)
    avg_session_length = Column(Float, default=0.0)
    interruption_rate = Column(Float, default=0.0)

    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="behavioral_state")