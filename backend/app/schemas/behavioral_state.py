from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BehavioralStateResponse(BaseModel):
    """Canonical analytics contract — field names match BehavioralState model."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str

    focus_consistency_score: float
    burnout_risk_score: float
    efficiency_score: float
    predicted_daily_capacity_minutes: float

    total_sessions: int
    total_focus_minutes: int
    avg_session_length: float
    interruption_rate: float

    updated_at: datetime


class AnalyticsResponse(BehavioralStateResponse):
    """Alias for GET /users/{user_id}/analytics — same contract as persisted state."""

    pass
