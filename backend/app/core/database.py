from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

if settings.environment == "test":
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    _connect_args = {"check_same_thread": False} if settings.is_sqlite else {}
    engine = create_engine(settings.database_url, connect_args=_connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def _register_models() -> None:
    """Import all ORM modules so metadata is populated (mirrors Alembic env)."""
    from app.models import (  # noqa: F401
        behavioral_state,
        session,
        task,
        user,
        work_item,
        workspace,
    )


def init_db() -> None:
    """Create all tables from ORM metadata (development / test bootstrap only)."""
    _register_models()
    Base.metadata.create_all(bind=engine)
