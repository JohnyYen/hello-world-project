import os

from pydantic_settings import BaseSettings

# Always prefer environment variable over .env files
# This ensures Docker's DATABASE_URL takes precedence


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hello World Backend"
    DATABASE_URL: str = (
        "postgresql+asyncpg://value:password@localhost:5432/hello-world-db"
    )
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600  # 1 hour for practical testing
    DEBUG: bool = True  # Enable detailed error traces in development

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
