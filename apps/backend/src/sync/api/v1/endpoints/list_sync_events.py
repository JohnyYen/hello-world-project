from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

from src.sync.api.v1.schemas.sync_event import SyncEventSchema
from src.sync.application.service.sync_event_service import SyncEventService
from src.sync.api.v1.dependencies import get_sync_event_service


router = APIRouter(prefix="/sync-events")


@router.get("/{session_id}", response_model=List[SyncEventSchema])
async def list_sync_events(
    session_id: UUID,
    service: SyncEventService = Depends(get_sync_event_service),
):
    """
    Lista eventos asociados a una sesión.
    """
    events = await service.get_events_by_session(session_id=session_id)

    return [
        SyncEventSchema(
            id=str(event.id),
            sync_session_id=str(event.sync_session_id),
            event_type=str(event.event_type),
            payload=event.payload,
            timestamp=event.timestamp,
            status=str(event.status),
        )
        for event in events
    ]
