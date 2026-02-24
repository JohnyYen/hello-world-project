from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.shared.infrastructure.session import get_db
from src.users.infrastructure.lms_credential_repository import LMSCredentialRepository
from src.users.infrastructure.user_repository import UserRepository
from src.shared.domain.exceptions import NotFoundException


router = APIRouter(prefix="/lms", tags=["LMS Integration"])


class SyncResultResponse(BaseModel):
    """Response schema for LMS sync operation."""

    status: str = "success"  # success, partial, failed
    message: str
    records_synced: dict[str, int]
    sync_time: datetime
    next_sync_scheduled: Optional[datetime] = None


@router.post("/sync/{user_id}", response_model=SyncResultResponse)
async def sync_lms_data(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Sincronizar datos entre LMS y la plataforma.

    Importa usuarios, cursos y calificaciones desde el LMS
    o exporta progreso de estudiantes al LMS.
    """
    # Verificar que el usuario existe
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise NotFoundException(f"Usuario con id={user_id} no encontrado")

    # Verificar que tiene credenciales LMS
    lms_repo = LMSCredentialRepository(db)
    credentials = await lms_repo.get_by_user_id(user_id)
    if not credentials:
        raise NotFoundException(
            f"El usuario {user_id} no tiene credenciales LMS configuradas"
        )

    # TODO: Implementar sincronización real con el LMS
    # Por ahora, retornamos un resultado mock

    sync_time = datetime.utcnow()
    result = SyncResultResponse(
        status="success",
        message="Sincronización completada exitosamente",
        records_synced={
            "users": 0,
            "courses": 0,
            "grades": 0,
        },
        sync_time=sync_time,
        next_sync_scheduled=sync_time + timedelta(hours=24),
    )

    return result
