from fastapi import APIRouter
from src.sync.api.v1.schemas.sync_session import SyncSessionSchema
import datetime


router = APIRouter(prefix="/sync-sessions")


@router.put("/{session_id}/end", response_model=SyncSessionSchema)
async def end_sync_session(session_id: int):
    """
    Finaliza la sesión.
    """
    # Datos de prueba
    mock_ended_session = {
        "id": session_id,
        "instance_id": 1,  # ID simulado
        "is_active": False,
        "started_at": datetime.datetime.now() - datetime.timedelta(hours=1),
        "ended_at": datetime.datetime.now(),
    }

    return mock_ended_session
