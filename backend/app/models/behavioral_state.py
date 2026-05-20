import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class BehavioralState(Base):
    __tablename__ = "behavioral_states"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)

    focus_consistency_score = Column(Float, default=0.0)
    burnout_risk_score = Column(Float, default=0.0)
    efficiency_score = Column(Float, default=0.0)
    predicted_daily_capacity_minutes = Column(Float, default=0.0)

    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")