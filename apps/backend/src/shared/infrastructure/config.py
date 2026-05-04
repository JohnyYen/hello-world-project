import os

from pydantic_settings import BaseSettings


def _convert_to_async_db_url(url: str) -> str:
    """Convert postgresql:// to postgresql+asyncpg:// for async database connection."""
    if url and "postgresql://" in url and "postgresql+asyncpg://" not in url:
        return url.replace("postgresql://", "postgresql+asyncpg://")
    return url


# Always prefer environment variable over .env files
# This ensures Docker's DATABASE_URL takes precedence


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hello World Backend"
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:3wtDUvT3h69bj6@db.icpzmepwjvigyazpcldq.supabase.co:6543/postgres?sslmode=require"
    )
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600  # 1 hour for practical testing
    DEBUG: bool = True  # Enable detailed error traces in development

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Convert database URL to asyncpg dialect
        self.DATABASE_URL = _convert_to_async_db_url(self.DATABASE_URL)
        # Log the database URL (masked) for debugging
        if self.DATABASE_URL:
            masked_url = self.DATABASE_URL.replace(
                self.DATABASE_URL.split("@")[0].split("://")[1]
                if "@" in self.DATABASE_URL
                else "",
                "***",
            )
            print(f"[CONFIG] DATABASE_URL: {masked_url}")


settings = Settings()
