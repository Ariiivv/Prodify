from pydantic import BaseModel


class TaskCreate(BaseModel):
    work_item_id: str
    title: str


class TaskResponse(BaseModel):
    id: str
    work_item_id: str
    title: str

    class Config:
        from_attributes = True