from fastapi import APIRouter, Depends, HTTPException, status

from src.sync.api.v1.schemas.sync_event import SyncEventCreate, SyncEventSchema
from src.sync.application.service.sync_event_service import SyncEventService
from src.sync.api.v1.dependencies import get_sync_event_service
from src.shared.domain.exceptions import NotFoundException


router = APIRouter(prefix="/sync-events")


@router.post("", response_model=SyncEventSchema, status_code=status.HTTP_201_CREATED)
async def register_sync_event(
    sync_event: SyncEventCreate,
    service: SyncEventService = Depends(get_sync_event_service),
):
    """
    Registra un evento (acción del jugador).
    """
    try:
        event = await service.create(event_data=sync_event)

        return SyncEventSchema(
            id=event.id,
            sync_session_id=event.sync_session_id,
            event_type=event.event_type,
            payload=event.payload,
            timestamp=event.timestamp,
            status=event.status,
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
