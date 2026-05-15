# Location: app/schemas/session.py
from pydantic import BaseModel

class FocusSessionCreate(BaseModel):
    user_id: str  # 👈 Change this from int to str
    duration_minutes: int

    class Config:
        from_attributes = True