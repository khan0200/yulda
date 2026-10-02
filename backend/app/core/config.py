from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    APP_NAME: str = "Yulda"
    API_V1_PREFIX: str = "/api/v1"
    ENV: str = "development"
    DEBUG: bool = True

    # Mongo
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "yulda"

    # Redis
    REDIS_URL: str = "redis://127.0.0.1:6379/0"

    # JWT
    JWT_SECRET: str = "change-me-dev-secret"
    JWT_REFRESH_SECRET: str = "change-me-dev-refresh-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"

    # Storage (S3-compatible)
    STORAGE_ENDPOINT: str = "http://localhost:9000"
    STORAGE_ACCESS_KEY: str = "minioadmin"
    STORAGE_SECRET_KEY: str = "minioadmin"
    STORAGE_BUCKET: str = "yulda-dev"
    STORAGE_REGION: str = "us-east-1"
    STORAGE_PUBLIC_BASE_URL: str = "http://localhost:9000/yulda-dev"

    # Maps
    MAPS_API_KEY: str = ""

    # Rate limiting
    RATE_LIMIT_DEFAULT: str = "100/minute"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
