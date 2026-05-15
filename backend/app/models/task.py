from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base
import uuid

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("courses.id"))
    title = Column(String)