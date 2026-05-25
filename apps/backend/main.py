from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router
from src.shared.infrastructure.config import settings
from src.shared.seed.run_seed import run_all_seeds
from src.shared.domain.exceptions import AppException
from src.admin.admin import setup_admin
from alembic import command
from alembic.config import Config as AlembicConfig
import os
import traceback


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
    openapi_extra={
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        }
    },
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup SQLAdmin - registers all models with authentication
# SQLAdmin 0.20.0 maneja su propia autenticación via AuthenticationBackend
setup_admin(app)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Manejador global para excepciones de aplicación - mejora debugging"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "detail": exc.detail,
            "path": str(request.url.path),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global para excepciones no manejadas - para debugging en desarrollo"""
    return JSONResponse(
        status_code=500,
        content={
            "error": exc.__class__.__name__,
            "detail": str(exc),
            "path": str(request.url.path),
            "traceback": traceback.format_exc() if settings.DEBUG else None,
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


@app.get("/health")
def verify_health():
    return {"message": "Health!!!"}


@app.get("/openapi")
def get_openapi():
    return app.openapi()
