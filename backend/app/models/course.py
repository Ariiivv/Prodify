import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    # Keeps your current UUID string ID format
    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    # Adds the nullable=False constraint from the second version
    title = Column(String, nullable=False)
    # Keeps your current Float type for total_hours
    total_hours = Column(Float)
    deadline_days = Column(Integer)
    # Adds the timestamp from the second version
    created_at = Column(DateTime, default=datetime.utcnow)

    # Adds the relationship mapping
    tasks = relationship("Task", back_populates="course")