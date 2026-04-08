"""
Central API Router - Aggregates all domain routers.

This module provides a central router that includes all API routers from:
<<<<<<< HEAD
- Authentication (auth)
- Users (users)
- Games (game)
- Sync (sync)
- Statistics (statistic)
- Course Reports (course)
=======
- Authentication (auth) - PUBLIC (no auth required)
- Users (users) - PROTECTED (JWT required)
- Games (game) - PROTECTED (JWT required)
- Sync (sync) - PROTECTED (JWT required)
- Statistics (statistic) - PROTECTED (JWT required)
>>>>>>> develop
"""

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

# Import routers from all domains
from src.auth.api.router import router as auth_router
from src.users.api.router import router as users_router
from src.game.api.router import router as game_router
from src.sync.api.v1.router import router as sync_router
from src.statistic.api.v1.router import router as statistic_router
from src.course.api.v1.router import router as course_router

# Create the central API router
router = APIRouter(prefix="/api/v1")

# Create a protected router with HTTPBearer dependency
# This applies JWT auth to all endpoints included in this router
protected_router = APIRouter(dependencies=[Depends(HTTPBearer())])

# Include auth router WITHOUT authentication (login, register, etc.)
router.include_router(auth_router)
<<<<<<< HEAD
router.include_router(users_router)
router.include_router(game_router)
router.include_router(sync_router)
router.include_router(statistic_router)
router.include_router(course_router)
=======

# Include protected routers WITH authentication
protected_router.include_router(users_router)
protected_router.include_router(game_router)
protected_router.include_router(sync_router)
protected_router.include_router(statistic_router)

# Include the protected router in the main router
router.include_router(protected_router)
>>>>>>> develop
