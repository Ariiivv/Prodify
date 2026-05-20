from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_or_404

from app.schemas.user import UserCreate, UserResponse
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from app.schemas.work_item import WorkItemCreate, WorkItemResponse
from app.schemas.task import TaskCreate, TaskResponse
from app.schemas.session import SessionCreate, SessionResponse
from app.schemas.behavioral_state import AnalyticsResponse

from app.models.user import User
from app.models.workspace import Workspace
from app.models.work_item import WorkItem
from app.models.task import Task
from app.models.session import Session as SessionModel

from app.services.behavioral_engine import BehavioralEngine

router = APIRouter()


# ---------------- HEALTH ----------------
@router.get("/health")
def health():
    return {"status": "healthy", "service": "prodify-backend"}


# ---------------- USERS ----------------
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    obj = User(email=user.email, name=user.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------- WORKSPACE ----------------
@router.post("/workspaces", response_model=WorkspaceResponse)
def create_workspace(data: WorkspaceCreate, db: Session = Depends(get_db)):
    get_or_404(db, User, data.user_id, "user_id")

    obj = Workspace(name=data.name, user_id=data.user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------- WORK ITEM ----------------
@router.post("/work-items", response_model=WorkItemResponse)
def create_work_item(data: WorkItemCreate, db: Session = Depends(get_db)):
    get_or_404(db, User, data.user_id, "user_id")
    workspace = get_or_404(db, Workspace, data.workspace_id, "workspace_id")

    if workspace.user_id != data.user_id:
        raise HTTPException(
            status_code=400,
            detail="workspace_id does not belong to user_id",
        )

    obj = WorkItem(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------- TASK ----------------
@router.post("/tasks", response_model=TaskResponse)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    get_or_404(db, WorkItem, data.work_item_id, "work_item_id")

    obj = Task(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------- SESSION ----------------
@router.post("/sessions", response_model=SessionResponse)
def create_session(data: SessionCreate, db: Session = Depends(get_db)):
    get_or_404(db, User, data.user_id, "user_id")
    get_or_404(db, Task, data.task_id, "task_id")

    obj = SessionModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    BehavioralEngine.compute_and_update(data.user_id, db)

    return obj


# ---------------- ANALYTICS ----------------
@router.get("/users/{user_id}/analytics", response_model=AnalyticsResponse)
def analytics(user_id: str, db: Session = Depends(get_db)):
    get_or_404(db, User, user_id, "user_id")
    state = BehavioralEngine.get_analytics(user_id, db)
    return state
