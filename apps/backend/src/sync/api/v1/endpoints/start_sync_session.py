from fastapi import APIRouter
from src.sync.api.v1.schemas.sync_session import SyncSessionCreate, SyncSessionSchema
import datetime


router = APIRouter(prefix="/sync-sessions")


@router.post("", response_model=SyncSessionSchema)
async def start_sync_session(sync_session: SyncSessionCreate):
    """
    Inicia una sesión de sincronización.
    """
    # Datos de prueba
    mock_new_session = {
        "id": 101,
        "instance_id": sync_session.instance_id,
        "is_active": True,
        "started_at": datetime.datetime.now(),
        "ended_at": None,
    }

    return mock_new_session
