from fastapi import APIRouter
from src.sync.api.v1.schemas.sync_event import SyncEventCreate, SyncEventSchema
import datetime


router = APIRouter(prefix="/sync-events")


@router.post("", response_model=SyncEventSchema)
async def register_sync_event(sync_event: SyncEventCreate):
    """
    Registra un evento (acción del jugador).
    """
    # Datos de prueba
    mock_new_event = {
        "id": 1001,
        "session_id": sync_event.session_id,
        "event_type": sync_event.event_type,
        "event_data": sync_event.event_data,
        "timestamp": datetime.datetime.now(),
    }

    return mock_new_event
