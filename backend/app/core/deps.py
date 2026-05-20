from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_or_404(db: Session, model, model_id: str, name: str):
    obj = db.query(model).filter(model.id == model_id).first()
    if not obj:
        raise HTTPException(status_code=400, detail=f"Invalid {name}")
    return obj
