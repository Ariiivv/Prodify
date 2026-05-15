# Location: app/schemas/task.py
from pydantic import BaseModel

class TaskCreate(BaseModel):
    course_id: str  # 👈 Change this from int to str
    title: str

    class Config:
        from_attributes = True