from pydantic import BaseModel


class SessionCreate(BaseModel):
    user_id: str
    task_id: str
    duration_minutes: int


class SessionResponse(BaseModel):
    id: str
    user_id: str
    task_id: str
    duration_minutes: int

    class Config:
        from_attributes = True