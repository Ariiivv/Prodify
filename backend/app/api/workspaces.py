from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.ownership import require_user
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.post("", response_model=WorkspaceResponse, status_code=201)
def create_workspace(data: WorkspaceCreate, db: Session = Depends(get_db)):
    require_user(db, data.user_id)

    obj = Workspace(name=data.name, user_id=data.user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
