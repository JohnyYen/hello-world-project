"""
DELETE /api/v1/notifications/{notification_id} - Delete a notification.
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
from src.notification.api.v1.schemas.notification import NotificationDeleteResponse

router = APIRouter(prefix="/notifications")


@router.delete("/{notification_id}", response_model=NotificationDeleteResponse)
async def delete_notification(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete (soft delete) a notification."""
    service = NotificationService(db)
    success = await service.delete_notification(notification_id, current_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada o no tienes permiso para eliminarla",
        )

    return NotificationDeleteResponse(
        success=True,
        message="Notificación eliminada",
        data=None,
    )
