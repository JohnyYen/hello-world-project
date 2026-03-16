from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db

from src.sync.application.service.sync_session_service import SyncSessionService
from src.sync.application.service.sync_event_service import SyncEventService


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
