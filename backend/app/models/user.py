import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)

    workspaces = relationship(
        "Workspace",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    sessions = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    work_items = relationship(
        "WorkItem",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    behavioral_state = relationship(
        "BehavioralState",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )