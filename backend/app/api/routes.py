from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

# Schemas
from app.schemas.user import UserCreate
from app.schemas.workspace import WorkspaceCreate
from app.schemas.work_item import WorkItemCreate
from app.schemas.task import TaskCreate
from app.schemas.session import FocusSessionCreate

# Models
from app.models.user import User
from app.models.workspace import Workspace
from app.models.work_item import WorkItem
from app.models.task import Task
from app.models.session import Session as FocusSession

router = APIRouter()


# -------------------- DB Dependency --------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- Health --------------------

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "prodify-backend"
    }


# -------------------- User --------------------

@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# -------------------- Workspace --------------------

@router.post("/workspaces")
def create_workspace(workspace: WorkspaceCreate, db: Session = Depends(get_db)):
    db_workspace = Workspace(
        name=workspace.name,
        user_id=workspace.user_id
    )
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace


# -------------------- Work Item --------------------

@router.post("/work-items")
def create_work_item(
    work_item: WorkItemCreate,
    db: Session = Depends(get_db)
):
    db_item = WorkItem(
        title=work_item.title,
        description=work_item.description,
        type=work_item.type,
        total_estimated_minutes=work_item.total_estimated_minutes,
        due_date=work_item.due_date,
        workspace_id=work_item.workspace_id,
        user_id=work_item.user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# -------------------- Task --------------------

@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        work_item_id=task.work_item_id,
        title=task.title
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# -------------------- Session --------------------

@router.post("/sessions")
def log_session(session_data: FocusSessionCreate, db: Session = Depends(get_db)):
    db_session = FocusSession(
        user_id=session_data.user_id,
        task_id=session_data.task_id,
        duration_minutes=session_data.duration_minutes,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


# -------------------- Analytics --------------------

@router.get("/users/{user_id}/analytics")
def get_user_analytics(user_id: str, db: Session = Depends(get_db)):
    sessions = db.query(FocusSession).filter(
        FocusSession.user_id == user_id
    ).all()

    total_sessions = len(sessions)
    total_minutes = sum(s.duration_minutes for s in sessions)

    avg_session_length = (
        total_minutes / total_sessions if total_sessions > 0 else 0
    )

    productivity_score = 0
    if total_sessions > 0:
        productivity_score = min(
            (avg_session_length / 45) * 100,
            100
        )

    return {
        "user_id": user_id,
        "total_sessions": total_sessions,
        "total_focus_minutes": total_minutes,
        "average_session_length": avg_session_length,
        "productivity_score": round(productivity_score, 2)
    }