"""Application configuration loaded from environment variables."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Smart Stadium AI System"
    app_version: str = "1.0.0"
    debug: bool = True
    database_url: str = "sqlite:///./smart_stadium.db"
    admin_api_key: str = "admin-secret-key-change-me"
    log_level: str = "INFO"
    cors_origins: str = "*"

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
