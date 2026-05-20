import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Configure test environment before any app imports
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("AUTO_CREATE_DB", "true")
os.environ.setdefault("LOG_LEVEL", "WARNING")

from app.core.config import get_settings
from app.core.database import Base, SessionLocal, engine, init_db

get_settings.cache_clear()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_db()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db() -> Session:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client():
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
