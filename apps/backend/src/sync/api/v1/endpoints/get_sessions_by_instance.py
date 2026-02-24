from fastapi import APIRouter
from typing import List
from src.sync.api.v1.schemas.sync_session import SyncSessionSchema
import datetime


router = APIRouter(prefix="/sync-sessions")


@router.get("/{instance_id}", response_model=List[SyncSessionSchema])
async def get_sessions_by_instance(instance_id: int):
    """
    Obtiene sesiones de una instancia.
    """
    # Datos de prueba
    mock_sessions = [
        {
            "id": 1,
            "instance_id": instance_id,
            "is_active": True,
            "started_at": datetime.datetime.now() - datetime.timedelta(minutes=30),
            "ended_at": None,
        },
        {
            "id": 2,
            "instance_id": instance_id,
            "is_active": False,
            "started_at": datetime.datetime.now() - datetime.timedelta(days=1),
            "ended_at": datetime.datetime.now() - datetime.timedelta(days=1, hours=2),
        },
    ]

    return mock_sessions
