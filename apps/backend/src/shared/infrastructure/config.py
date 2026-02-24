import os

from pydantic_settings import BaseSettings

# Detectar automáticamente qué archivo .env usar
# Prioridad: .env.local > .env
# Esto permite tener configuración para desarrollo local (localhost) y Docker
_env_file = ".env.local" if os.path.exists(".env.local") else ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hello World Backend"
    DATABASE_URL: str = (
        "postgresql+asyncpg://value:password@localhost:5432/hello-world-db"
    )
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = _env_file
        env_file_encoding = "utf-8"


settings = Settings()
