"""
Provider functions for Sync domain services and repositories.

This module provides FastAPI dependency injection functions for:
- SyncSessionRepository
- SyncEventRepository
- SyncSessionService
- SyncEventService
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db

# Repository imports
from src.sync.infrastructure.repositories.sync_session_repository import (
    SyncSessionRepository,
)
from src.sync.infrastructure.repositories.sync_event_repository import (
    SyncEventRepository,
)

# Service imports
from src.sync.application.service.sync_session_service import SyncSessionService
from src.sync.application.service.sync_event_service import SyncEventService


# ====================
# Repository Providers
# ====================


def get_sync_session_repository(
    db: AsyncSession = Depends(get_db),
) -> SyncSessionRepository:
    """Provider for SyncSessionRepository."""
    return SyncSessionRepository(db)


def get_sync_event_repository(
    db: AsyncSession = Depends(get_db),
) -> SyncEventRepository:
    """Provider for SyncEventRepository."""
    return SyncEventRepository(db)


# ====================
# Service Providers
# ====================


def get_sync_session_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SyncSessionService:
    """Provider for SyncSessionService with injected database session."""
    return SyncSessionService(db)


def get_sync_event_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SyncEventService:
    """Provider for SyncEventService with injected database session."""
    return SyncEventService(db)
