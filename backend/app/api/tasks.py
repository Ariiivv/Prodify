from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_or_404
from app.models.work_item import WorkItem
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    get_or_404(db, WorkItem, data.work_item_id, name="work_item")

    obj = Task(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
