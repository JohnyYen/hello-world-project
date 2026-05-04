from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings
from src.shared.infrastructure.base import Base

# FORZAR LA URL DE SUPABASE PARA RENDER - USAR POOLER (puerto 6543)
SUPABASE_URL = "postgresql+asyncpg://postgres:3wtDUvT3h69bj6@db.icpzmepwjvigyazpcldq.supabase.co:6543/postgres"
print(f"[DEBUG] Using hardcoded DATABASE_URL: {SUPABASE_URL.replace('postgres:3wtDUvT3h69bj6', '***')}")

engine = create_async_engine(SUPABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        yield session
