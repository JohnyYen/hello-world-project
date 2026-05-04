from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings
from src.shared.infrastructure.base import Base

# DATABASE_URL de Render (n8n-db)
SUPABASE_URL = "postgresql+asyncpg://n8n_db_02sc_user:2EjX0QpGas8rNTH9dCp0bZp1nfFU3Gch@dpg-d7roq5n7f7vs73d5gnm0-a.oregon-postgres.render.com/n8n_db_02sc"
print(f"[DEBUG] Using hardcoded DATABASE_URL: {SUPABASE_URL.replace('n8n_db_02sc_user:2EjX0QpGas8rNTH9dCp0bZp1nfFU3Gch', '***')}")

engine = create_async_engine(SUPABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        yield session
