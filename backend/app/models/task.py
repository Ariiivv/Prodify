import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    work_item_id = Column(String, ForeignKey("work_items.id"), nullable=False)

    title = Column(String, nullable=False)

    work_item = relationship("WorkItem", back_populates="tasks")
    sessions = relationship(
        "Session",
        back_populates="task",
        cascade="all, delete-orphan"
    )