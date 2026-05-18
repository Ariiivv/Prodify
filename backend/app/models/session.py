import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class FocusSession(Base):
    # Adopted the more descriptive table name from the second version
    __tablename__ = "focus_sessions"

    # Retains your UUID string format for the primary key
    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    # Keeps your String/UUID foreign key to match your app's user setup
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    # Kept as Integer for total tracking duration
    duration_minutes = Column(Integer, nullable=False)
    # Adds the timestamp tracker from the second version
    created_at = Column(DateTime, default=datetime.utcnow)

    # Establishes the relationship mapping back to the User
    user = relationship("User", back_populates="sessions")