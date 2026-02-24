from fastapi import APIRouter
from typing import List
from src.sync.api.v1.schemas.sync_event import SyncEventSchema
import datetime


router = APIRouter(prefix="/sync-events")


@router.get("/{session_id}", response_model=List[SyncEventSchema])
async def list_sync_events(session_id: int):
    """
    Lista eventos asociados a una sesión.
    """
    # Datos de prueba
    mock_events = [
        {
            "id": 1,
            "session_id": session_id,
            "event_type": "player_move",
            "event_data": {"direction": "up", "x": 10, "y": 20},
            "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=5),
        },
        {
            "id": 2,
            "session_id": session_id,
            "event_type": "level_complete",
            "event_data": {"level_id": 5, "score": 1500},
            "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=3),
        },
        {
            "id": 3,
            "session_id": session_id,
            "event_type": "item_collected",
            "event_data": {"item_id": "power_up", "quantity": 1},
            "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=1),
        },
    ]

    return mock_events
