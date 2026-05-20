from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.ownership import require_user, require_task_for_user
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionResponse
from app.services.behavioral_engine import BehavioralEngine

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse, status_code=201)
def create_session(data: SessionCreate, db: Session = Depends(get_db)):
    require_user(db, data.user_id)
    require_task_for_user(db, data.task_id, data.user_id)

    obj = SessionModel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    BehavioralEngine.compute_and_update(data.user_id, db)

    return obj
