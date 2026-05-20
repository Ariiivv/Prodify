from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.ownership import validate_work_item_ownership
from app.models.work_item import WorkItem
from app.schemas.work_item import WorkItemCreate, WorkItemResponse

router = APIRouter(prefix="/work-items", tags=["work-items"])


@router.post("", response_model=WorkItemResponse, status_code=201)
def create_work_item(data: WorkItemCreate, db: Session = Depends(get_db)):
    validate_work_item_ownership(
        db, user_id=data.user_id, workspace_id=data.workspace_id
    )

    obj = WorkItem(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
