from pydantic import BaseModel
from datetime import datetime


class WorkspaceCreate(BaseModel):
    name: str
    user_id: str


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True