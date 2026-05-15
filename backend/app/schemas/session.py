from pydantic import BaseModel

class FocusSessionCreate(BaseModel):
    user_id: int
    duration_minutes: float