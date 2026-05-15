from fastapi import FastAPI
from app.api.routes import router
from app.core.database import engine
from app.models import user, course, task, session
from app.core.database import engine, Base
from app.models import user, course, task, session

Base.metadata.create_all(bind=engine)

user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)
session.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Prodify API",
    description="AI Behavioral Intelligence Backend",
    version="0.1.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Prodify Backend Running"}