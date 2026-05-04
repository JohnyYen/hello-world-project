from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router
from src.shared.infrastructure.config import settings
from src.shared.seed.run_seed import run_all_seeds
from src.shared.domain.exceptions import AppException
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
    try:
        from src.shared.infrastructure.session import SessionLocal
        from sqlalchemy import text
        
        async with SessionLocal() as session:
            # Create roles table
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS roles (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    role_name VARCHAR(255) UNIQUE NOT NULL,
                    description VARCHAR(255),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    deleted_at TIMESTAMP WITH TIME ZONE,
                    is_deleted BOOLEAN DEFAULT false
                )
            """))
            
            # Create users table
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    username VARCHAR(255) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    lastname VARCHAR(255),
                    email VARCHAR(255) UNIQUE NOT NULL,
                    lms_id UUID,
                    avatar_url VARCHAR(255),
                    is_active BOOLEAN DEFAULT true NOT NULL,
                    last_login TIMESTAMP WITH TIME ZONE,
                    role_id UUID,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    deleted_at TIMESTAMP WITH TIME ZONE,
                    is_deleted BOOLEAN DEFAULT false
                )
            """))
            
            # Insert default roles
            await session.execute(text("""
                INSERT INTO roles (role_name, description) VALUES 
                    ('admin', 'System administrator'),
                    ('professor', 'Teacher who creates content'),
                    ('student', 'Learner who plays games')
                ON CONFLICT (role_name) DO NOTHING
            """))
            
            await session.commit()
            print("[STARTUP] Database tables created successfully")
        
        await run_all_seeds()
    except Exception as e:
        print(f"[STARTUP ERROR] {e}")
        import traceback
        traceback.print_exc()


app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/health")
def verify_health():
    return {"message": "Health!!!"}


@app.get("/debug-db")
async def debug_db():
    """Debug endpoint to check database connection"""
    from sqlalchemy import text
    from src.shared.infrastructure.session import SessionLocal
    
    try:
        async with SessionLocal() as session:
            # Get database info
            result = await session.execute(text("SELECT current_database() as db, current_user as user"))
            db_info = result.fetchone()
            
            # Check tables
            result = await session.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]
            
            # Check roles
            result = await session.execute(text("SELECT * FROM roles LIMIT 5"))
            roles = [dict(row._mapping) for row in result.fetchall()]
            
            return {
                "database": db_info[0],
                "user": db_info[1],
                "tables": tables,
                "roles": roles
            }
    except Exception as e:
        return {"error": str(e)}


@app.get("/openapi")
def get_openapi():
    return app.openapi()
