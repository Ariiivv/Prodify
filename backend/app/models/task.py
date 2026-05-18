import uuid
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    # Retains your UUID string format for the primary key
    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    # Correctly targets the courses.id String/UUID primary key
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    # Adds a non-nullable constraint for safety
    title = Column(String, nullable=False)

    # Establishes the bidirectional relationship back to the Course model
    course = relationship("Course", back_populates="tasks")