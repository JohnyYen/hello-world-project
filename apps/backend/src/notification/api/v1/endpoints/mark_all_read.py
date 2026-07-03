"""
PATCH /api/v1/notifications/read-all - Mark all notifications as read.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.notification.application.service.notification_service import (
    NotificationService,
)
from src.notification.api.v1.schemas.notification import NotificationReadResponse

router = APIRouter(prefix="/notifications")


@router.patch("/read-all", response_model=NotificationReadResponse)
async def mark_all_notifications_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark all notifications as read for the current user."""
    service = NotificationService(db)
    updated_count = await service.mark_all_as_read(current_user)

    return NotificationReadResponse(
        success=True,
        message=f"Se marcaron {updated_count} notificaciones como leídas",
        data={"updated_count": updated_count},
    )
