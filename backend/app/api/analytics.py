from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.ownership import require_user
from app.schemas.behavioral_state import AnalyticsResponse
from app.services.behavioral_engine import BehavioralEngine

router = APIRouter(tags=["analytics"])


@router.get(
    "/users/{user_id}/analytics",
    response_model=AnalyticsResponse,
)
def get_user_analytics(user_id: str, db: Session = Depends(get_db)):
    require_user(db, user_id)
    return BehavioralEngine.get_analytics(user_id, db)
