from pydantic import BaseModel, ConfigDict
from datetime import datetime


class WorkspaceCreate(BaseModel):
    name: str
    user_id: str


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    user_id: str
    created_at: datetime
