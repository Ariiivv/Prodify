from pydantic import BaseModel

class TaskCreate(BaseModel):
    course_id: int
    title: str