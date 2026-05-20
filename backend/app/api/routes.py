from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.schemas.user import UserCreate
from app.schemas.workspace import WorkspaceCreate
from app.schemas.work_item import WorkItemCreate
from app.schemas.task import TaskCreate, TaskResponse
from app.schemas.session import SessionCreate, SessionResponse

from app.models.user import User
from app.models.workspace import Workspace
from app.models.work_item import WorkItem
from app.models.task import Task
from app.models.session import Session as SessionModel

router = APIRouter()


# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- HELPERS ----------------
def get_or_404(db: Session, model, model_id: str, name: str):
    obj = db.query(model).filter(model.id == model_id).first()
    if not obj:
        raise HTTPException(status_code=400, detail=f"Invalid {name}")
    return obj


# ---------------- HEALTH ----------------
@router.get("/health")
def health():
    return {"status": "healthy", "service": "prodify-backend"}


# ---------------- USERS ----------------
@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    obj = User(email=user.email, name=user.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------- WORKSPACE ----------------
@router.post("/workspaces")
def create_workspace(data: WorkspaceCreate, db: Session = Depends(get_db)):
    get_or_404(db, User, data.user_id, "user_id")

    obj = Workspace(name=data.name, user_id=data.user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------- WORK ITEM ----------------
@router.post("/work-items")
def create_work_item(data: WorkItemCreate, db: Session = Depends(get_db)):
    obj = WorkItem(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------- TASK ----------------
@router.post("/tasks", response_model=TaskResponse)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):

    get_or_404(db, WorkItem, data.work_item_id, "work_item_id")

    obj = Task(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------------- SESSION ----------------
@router.post("/sessions", response_model=SessionResponse)
def create_session(data: SessionCreate, db: Session = Depends(get_db)):

    get_or_404(db, User, data.user_id, "user_id")
    get_or_404(db, Task, data.task_id, "task_id")

    obj = SessionModel(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ---------------- ANALYTICS (UPGRADED FOUNDATION) ----------------
@router.get("/users/{user_id}/analytics")
def analytics(user_id: str, db: Session = Depends(get_db)):

    sessions = db.query(SessionModel).filter(
        SessionModel.user_id == user_id
    ).all()

    if not sessions:
        return {
            "user_id": user_id,
            "total_sessions": 0,
            "total_minutes": 0,
            "avg_session_length": 0,
            "productivity_score": 0,
            "consistency_score": 0,
            "burnout_risk": 0
        }

    total_sessions = len(sessions)
    total_minutes = sum(s.duration_minutes for s in sessions)
    avg = total_minutes / total_sessions

    # variance proxy (basic stability signal)
    variance = sum((s.duration_minutes - avg) ** 2 for s in sessions) / total_sessions

    # upgraded scoring baseline (still simple but more meaningful)
    productivity_score = min((avg / 45) * 100, 100)
    consistency_score = max(0, 100 - (variance / 20))

    burnout_risk = min(
        100,
        (avg / 90) * 50 + (variance / 50) * 50
    )

    return {
        "user_id": user_id,
        "total_sessions": total_sessions,
        "total_minutes": total_minutes,
        "avg_session_length": round(avg, 2),
        "productivity_score": round(productivity_score, 2),
        "consistency_score": round(consistency_score, 2),
        "burnout_risk": round(burnout_risk, 2)
    }