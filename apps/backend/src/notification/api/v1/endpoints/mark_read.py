"""
PATCH /api/v1/notifications/{notification_id}/read - Mark a notification as read.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.notification.application.service.notification_service import (
    NotificationService,
)
from src.notification.api.v1.schemas.notification import NotificationReadResponse

router = APIRouter(prefix="/notifications")


@router.patch("/{notification_id}/read", response_model=NotificationReadResponse)
async def mark_notification_read(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark a single notification as read."""
    service = NotificationService(db)
    success = await service.mark_as_read(notification_id, current_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada o no tienes permiso para modificarla",
        )

    return NotificationReadResponse(
        success=True,
        message="Notificación marcada como leída",
        data=None,
    )
