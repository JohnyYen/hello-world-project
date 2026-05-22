import os

from pydantic_settings import BaseSettings


def _convert_to_async_db_url(url: str) -> str:
    """Convert postgresql:// to postgresql+asyncpg:// for async database connection."""
    if url and "postgresql://" in url and "postgresql+asyncpg://" not in url:
        return url.replace("postgresql://", "postgresql+asyncpg://")
    return url


def _get_debug_mode() -> bool:
    """Get DEBUG mode from environment variable, default to False for security."""
    debug_value = os.getenv("DEBUG", "false").lower()
    return debug_value in ("true", "1", "yes")


# Always prefer environment variable over .env files
# This ensures Docker's DATABASE_URL takes precedence


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hello World Backend"
    DATABASE_URL: str = (
        "postgresql+asyncpg://value:password@localhost:5432/hello-world-db"
    )
    SECRET_KEY: str = ""  # Will be validated at startup
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600  # 1 hour for practical testing
    DEBUG: bool = False  # Default to False for security - override with DEBUG=true env var

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Convert database URL to asyncpg dialect
        self.DATABASE_URL = _convert_to_async_db_url(self.DATABASE_URL)
        
        # Override DEBUG from environment variable
        self.DEBUG = _get_debug_mode()
        
        # Validate SECRET_KEY at startup - fail fast if not configured
        if not self.SECRET_KEY:
            raise ValueError(
                "SECRET_KEY is not configured! "
                "Set SECRET_KEY environment variable to a secure value. "
                "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        
        # Validate minimum key strength
        if len(self.SECRET_KEY) < 32:
            raise ValueError(
                f"SECRET_KEY is too short ({len(self.SECRET_KEY)} chars). "
                "Minimum 32 characters required for secure JWT signing."
            )
        
        # Log the database URL (masked) for debugging
        if self.DATABASE_URL:
            masked_url = self.DATABASE_URL.replace(
                self.DATABASE_URL.split("@")[0].split("://")[1]
                if "@" in self.DATABASE_URL
                else "",
                "***",
            )
            print(f"[CONFIG] DATABASE_URL: {masked_url}")
        
        # Warn if debug is enabled (security concern)
        if self.DEBUG:
            print("[SECURITY WARNING] DEBUG mode is enabled! Tracebacks will be exposed.")


settings = Settings()
