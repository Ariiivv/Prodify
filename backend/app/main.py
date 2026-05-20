import logging

from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings
from app.core.database import init_db

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

if settings.auto_create_db:
    logger.warning(
        "AUTO_CREATE_DB is enabled — using create_all. "
        "Use Alembic migrations in production."
    )
    init_db()

app = FastAPI(
    title="Prodify API",
    description="AI Behavioral Intelligence Backend",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Prodify Backend Running"}
