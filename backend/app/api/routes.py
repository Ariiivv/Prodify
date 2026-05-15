from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.user import UserCreate
from app.schemas.course import CourseCreate
from app.schemas.task import TaskCreate
from app.schemas.session import FocusSessionCreate
from app.models.user import User
from app.models.session import FocusSession
from app.models.course import Course
from app.models.task import Task

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "prodify-backend"
    }

@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/courses")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        title=course.title,
        total_hours=course.total_hours,
        deadline_days=course.deadline_days,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(course_id=task.course_id, title=task.title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.post("/sessions")
def log_session(session_data: FocusSessionCreate, db: Session = Depends(get_db)):
    db_session = FocusSession(
        user_id=session_data.user_id,
        duration_minutes=session_data.duration_minutes,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session
