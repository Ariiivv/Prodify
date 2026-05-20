from typing import Type, TypeVar

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

T = TypeVar("T")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_or_404(
    db: Session,
    model: Type[T],
    model_id: str,
    *,
    name: str | None = None,
) -> T:
    """Return entity by primary key or raise HTTP 404."""
    obj = db.query(model).filter(model.id == model_id).first()
    if not obj:
        label = name or model.__tablename__
        raise HTTPException(
            status_code=404,
            detail=f"{label} not found",
        )
    return obj
