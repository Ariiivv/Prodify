from pydantic import BaseModel
from datetime import datetime


class BehavioralStateResponse(BaseModel):
    id: str
    user_id: str
    focus_consistency_score: float
    burnout_risk_score: float
    efficiency_score: float
    predicted_daily_capacity_minutes: float
    updated_at: datetime

    class Config:
        from_attributes = True