from fastapi import APIRouter

from src.auth.api.v1.endpoints.login import router as login_router
from src.auth.api.v1.endpoints.register import router as register_router
from src.auth.api.v1.endpoints.change_password import router as change_password_router


router = APIRouter(prefix="/auth", tags=["Authentication"], security=[])

# Incluir todos los routers de endpoints
router.include_router(login_router)
router.include_router(register_router)
router.include_router(change_password_router)
