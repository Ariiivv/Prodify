from sqlalchemy import Column, String
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    name = Column(String)
    sessions = relationship("FocusSession", back_populates="user")