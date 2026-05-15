from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base
import uuid

class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    total_hours = Column(Float)
    deadline_days = Column(Integer)