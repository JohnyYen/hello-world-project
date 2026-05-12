from fastapi import APIRouter, Depends, HTTPException, status

from src.sync.api.v1.schemas.sync_session import SyncSessionCreate, SyncSessionSchema
from src.sync.application.service.sync_session_service import SyncSessionService
from src.sync.api.v1.dependencies import get_sync_session_service


router = APIRouter(prefix="/sync-sessions")


@router.post("", response_model=SyncSessionSchema, status_code=status.HTTP_201_CREATED)
async def start_sync_session(
    sync_session: SyncSessionCreate,
    service: SyncSessionService = Depends(get_sync_session_service),
):
    """
    Inicia una sesión de sincronización.
    """
    session = await service.create(instance_id=sync_session.instance_id)

    return SyncSessionSchema(
        id=str(session.id),
        instance_id=str(session.instance_id),
        is_active=session.status == "active",
        start_time=session.start_time,
        end_time=session.end_time,
    )
