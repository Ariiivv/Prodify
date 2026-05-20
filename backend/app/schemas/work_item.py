from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
from datetime import datetime


WorkItemType = Literal["one_time", "recurring", "long_term"]


class WorkItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: WorkItemType
    total_estimated_minutes: Optional[int] = None
    due_date: Optional[datetime] = None
    workspace_id: str
    user_id: str


class WorkItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
