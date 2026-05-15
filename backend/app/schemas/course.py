from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    total_hours: float
    deadline_days: int