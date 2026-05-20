from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    work_item_id: str
    title: str


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    work_item_id: str
    title: str
