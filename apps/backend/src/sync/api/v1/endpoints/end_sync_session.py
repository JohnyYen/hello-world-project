from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from src.sync.api.v1.schemas.sync_session import SyncSessionSchema
from src.sync.application.service.sync_session_service import SyncSessionService
from src.sync.api.v1.dependencies import get_sync_session_service
from src.shared.domain.exceptions import NotFoundException


router = APIRouter(prefix="/sync-sessions")


@router.put("/{session_id}/end", response_model=SyncSessionSchema)
async def end_sync_session(
    session_id: UUID,
    service: SyncSessionService = Depends(get_sync_session_service),
):
    """
    Finaliza la sesión.
    """
    try:
        session = await service.end_session(session_id=session_id)

        return SyncSessionSchema(
            id=str(session.id),
            instance_id=str(session.instance_id),
            is_active=session.status == "active",
            start_time=session.start_time,
            end_time=session.end_time,
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sesión de sincronización no encontrada: {str(e)}",
        )
