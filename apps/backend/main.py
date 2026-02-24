from fastapi import FastAPI
from src.api.router import router
from src.shared.infrastructure.config import settings
from src.shared.seed.run_seed import run_all_seeds
from alembic import command
from alembic.config import Config as AlembicConfig
import os


def run_migrations():
    """Run Alembic migrations on startup."""
    alembic_cfg = AlembicConfig("alembic.ini")
    # Ensure we're in the correct directory
    alembic_cfg.set_main_option("script_location", "migrations")
    command.upgrade(alembic_cfg, "head")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Una API moderna y asíncrona para gestionar la plataforma de aprendizaje de programación con videjuegos",
    version="1.0.0",
    contact={
        "name": "Johny A. Pedraza Romero",
        "url": "http://tuwebsite.com",
        "email": "jhonnyantonio892@gmail.com",
    },
)


@app.on_event("startup")
async def on_startup():
    # run_migrations()
    await run_all_seeds()
    pass


app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
