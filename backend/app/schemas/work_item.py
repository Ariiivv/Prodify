from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WorkItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: str  # one_time | recurring | long_term
    total_estimated_minutes: Optional[int] = None
    due_date: Optional[datetime] = None
    workspace_id: str
    user_id: str


class WorkItemResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    type: str
    total_estimated_minutes: Optional[int]
    due_date: Optional[datetime]
    is_completed: bool
    created_at: datetime
    user_id: str
    workspace_id: str

    class Config:
        from_attributes = True