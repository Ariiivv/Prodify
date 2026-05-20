from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./prodify.db"
    environment: Literal["development", "production", "test"] = "development"
    log_level: str = "INFO"

    # Dev-only: create tables on startup without Alembic (disabled in production/test)
    auto_create_db: bool = False

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @model_validator(mode="after")
    def validate_production_safety(self) -> "Settings":
        if self.environment == "production" and self.auto_create_db:
            raise ValueError(
                "AUTO_CREATE_DB must be false when ENVIRONMENT=production. "
                "Use Alembic migrations instead."
            )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
