from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    name: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    name: str
