import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # one_time | recurring | long_term
    type = Column(String, nullable=False)

    total_estimated_minutes = Column(Integer, nullable=True)
    due_date = Column(DateTime, nullable=True)

    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id"), nullable=False)

    user = relationship("User")
    workspace = relationship("Workspace", back_populates="work_items")
    tasks = relationship(
        "Task",
        back_populates="work_item",
        cascade="all, delete-orphan"
    )