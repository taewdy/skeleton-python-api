from __future__ import annotations

from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version as pkg_version
from typing import List, Literal

from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def _package_version(default: str = "0.1.0") -> str:
    try:
        return pkg_version("photos-api")
    except PackageNotFoundError:
        return default


class ServerSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    reload: bool = True
    log_level: Literal["critical", "error", "warning", "info", "debug", "trace"] = "info"


class CorsSettings(BaseModel):
    allow_origins: str = "*"  # comma-separated or "*"
    allow_methods: str = "GET"  # comma-separated
    allow_headers: str = "*"  # comma-separated or "*"

    def origins(self) -> List[str]:
        value = self.allow_origins.strip()
        if value in ("", "*"):
            return ["*"]
        return [part.strip() for part in value.split(",") if part.strip()]

    def methods(self) -> List[str]:
        value = self.allow_methods.strip()
        return [part.strip().upper() for part in value.split(",") if part.strip()]

    def headers(self) -> List[str]:
        value = self.allow_headers.strip()
        if value in ("", "*"):
            return ["*"]
        return [part.strip() for part in value.split(",") if part.strip()]


class ExternalSettings(BaseModel):
    base_url: HttpUrl = HttpUrl("https://jsonplaceholder.typicode.com")
    http_timeout: float = 30.0
    max_retries: int = 2
    backoff_factor: float = 0.2


class LoggingSettings(BaseModel):
    as_json: bool = False


class Settings(BaseSettings):
    """Application settings loaded from environment (and .env)."""

    # App metadata
    app_name: str = "Photos API"
    app_version: str = Field(default_factory=_package_version)

    # Groups
    server: ServerSettings = ServerSettings()
    cors: CorsSettings = CorsSettings()
    external: ExternalSettings = ExternalSettings()
    logging: LoggingSettings = LoggingSettings()

    model_config = SettingsConfigDict(
        env_prefix="PHOTOS_API_",
        env_nested_delimiter="__",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
