from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class SessionCreate(BaseModel):
    user_id: str
    task_id: str
    duration_minutes: int

    focus_score: float = 0.0
    interruption_count: int = 0
    pause_minutes: float = 0.0

    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    task_id: str
    duration_minutes: int

    focus_score: float
    interruption_count: int
    pause_minutes: float

    started_at: datetime
    ended_at: Optional[datetime] = None
    created_at: datetime
