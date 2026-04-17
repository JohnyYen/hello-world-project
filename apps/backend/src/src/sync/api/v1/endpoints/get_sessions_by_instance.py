from fastapi import APIRouter, Depends
from typing import List

from src.sync.api.v1.schemas.sync_session import SyncSessionSchema
from src.sync.application.service.sync_session_service import SyncSessionService
from src.sync.api.v1.dependencies import get_sync_session_service


router = APIRouter(prefix="/sync-sessions")


@router.get("/{instance_id}", response_model=List[SyncSessionSchema])
async def get_sessions_by_instance(
    instance_id: int,
    service: SyncSessionService = Depends(get_sync_session_service),
):
    """
    Obtiene sesiones de una instancia.
    """
    sessions = await service.get_by_instance(instance_id=instance_id)

    return [
        SyncSessionSchema(
            id=session.id,
            instance_id=session.instance_id,
            is_active=session.status == "active",
            start_time=session.start_time,
            end_time=session.end_time,
        )
        for session in sessions
    ]
