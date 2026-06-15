"""
Notification repository for CRUD operations on notifications.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.notification.domain import Notification
from src.shared.infrastructure.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """Repository for Notification model operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Notification)

    async def get_by_user_id(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        unread_only: bool = False,
    ) -> list[Notification]:
        """Get notifications for a specific user, newest first."""
        query = (
            select(Notification)
            .where(
                and_(
                    Notification.user_id == user_id,
                    Notification.deleted_at.is_(None),
                )
            )
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        if unread_only:
            query = query.where(Notification.is_read == False)  # noqa: E712

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def mark_as_read(self, notification_id: UUID, user_id: UUID) -> bool:
        """Mark a single notification as read (with ownership check)."""
        result = await self.db.execute(
            update(Notification)
            .where(
                and_(
                    Notification.id == notification_id,
                    Notification.user_id == user_id,
                    Notification.deleted_at.is_(None),
                )
            )
            .values(is_read=True)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def mark_all_as_read(self, user_id: UUID) -> int:
        """Mark all unread notifications as read for a user."""
        result = await self.db.execute(
            update(Notification)
            .where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False,  # noqa: E712
                    Notification.deleted_at.is_(None),
                )
            )
            .values(is_read=True)
        )
        await self.db.commit()
        return result.rowcount

    async def count_unread(self, user_id: UUID) -> int:
        """Count unread notifications for a user."""
        query = select(func.count(Notification.id)).where(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False,  # noqa: E712
                Notification.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def notification_exists(
        self, user_id: UUID, notification_type: str, days: int = 1
    ) -> bool:
        """Check if a notification of a given type exists within recent days."""
        from datetime import datetime, timezone, timedelta

        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        query = select(func.count(Notification.id)).where(
            and_(
                Notification.user_id == user_id,
                Notification.notification_type == notification_type,
                Notification.created_at >= cutoff,
                Notification.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(query)
        return (result.scalar() or 0) > 0
