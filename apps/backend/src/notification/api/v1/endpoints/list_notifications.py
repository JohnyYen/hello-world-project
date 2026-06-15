"""
GET /api/v1/notifications - List notifications for the authenticated user.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.notification.application.service.notification_service import (
    NotificationService,
)
from src.notification.api.v1.schemas.notification import (
    NotificationListResponse,
    NotificationResponse,
)

router = APIRouter(prefix="/notifications")


@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Máximo de registros"),
    unread_only: bool = Query(False, description="Filtrar solo no leídas"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtener todas las notificaciones del usuario autenticado.

    Genera automáticamente notificaciones del sistema basadas en el estado
    de la plataforma (estudiantes inactivos, sin curso, etc.).
    """
    service = NotificationService(db)
    notifications, unread_count, total_count = await service.list_notifications(
        user=current_user,
        skip=skip,
        limit=limit,
        unread_only=unread_only,
    )

    return NotificationListResponse(
        success=True,
        message="Notificaciones obtenidas exitosamente",
        data=[NotificationResponse.model_validate(n) for n in notifications],
        unread_count=unread_count,
        total_count=total_count,
    )
