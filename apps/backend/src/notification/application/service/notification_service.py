"""
Notification service for CRUD operations and auto-generation
of system notifications for professors.
"""

import logging
from datetime import datetime, timezone, timedelta
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.notification.domain import Notification
from src.notification.infrastructure.notification_repository import (
    NotificationRepository,
)
from src.users.domain.user import User
from src.users.domain.student import Student
from src.course.domain.course_enrollment import CourseEnrollment

logger = logging.getLogger(__name__)

# ─── Auto-notification config ───────────────────────────────────────────────

SYSTEM_NOTIFICATION_TYPES = {
    "inactive_students": {
        "title": "Estudiantes inactivos",
        "message_template": "{count} estudiante(s) no han accedido a la plataforma en más de 7 días.",
    },
    "unassigned_students": {
        "title": "Estudiantes sin curso",
        "message_template": "{count} estudiante(s) aún no están asignados a ningún curso.",
    },
    "new_registrations": {
        "title": "Nuevos registros",
        "message_template": "{count} nuevo(s) estudiante(s) se registraron en la última semana.",
    },
    "weekly_summary": {
        "title": "Resumen semanal",
        "message_template": "Esta semana hay {total} estudiante(s) activos en la plataforma.",
    },
}

ACTIVITY_THRESHOLD_DAYS = 7


class NotificationService:
    """Service for notification operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = NotificationRepository(db)

    async def list_notifications(
        self, user: User, skip: int = 0, limit: int = 50, unread_only: bool = False
    ) -> tuple[list[Notification], int, int]:
        """List notifications for a user, auto-generating system notifications.

        Returns:
            Tuple of (notifications list, unread count, total count)
        """
        # Auto-generate system notifications for professors
        if user.role and user.role.role_name == "professor":
            await self._generate_system_notifications(user)

        # Now fetch from DB
        notifications = await self.repository.get_by_user_id(
            user.id, skip=skip, limit=limit, unread_only=unread_only
        )
        unread_count = await self.repository.count_unread(user.id)
        total_count = len(notifications)

        return notifications, unread_count, total_count

    async def _generate_system_notifications(self, user: User) -> None:
        """Generate system notifications based on platform state."""
        try:
            # 1. Inactive students
            inactive_count = await self._count_inactive_students()
            if inactive_count > 0:
                await self._create_if_not_exists(
                    user_id=user.id,
                    notification_type="inactive_students",
                    message=SYSTEM_NOTIFICATION_TYPES["inactive_students"][
                        "message_template"
                    ].format(count=inactive_count),
                    title=SYSTEM_NOTIFICATION_TYPES["inactive_students"]["title"],
                )

            # 2. Unassigned students
            unassigned_count = await self._count_unassigned_students()
            if unassigned_count > 0:
                await self._create_if_not_exists(
                    user_id=user.id,
                    notification_type="unassigned_students",
                    message=SYSTEM_NOTIFICATION_TYPES["unassigned_students"][
                        "message_template"
                    ].format(count=unassigned_count),
                    title=SYSTEM_NOTIFICATION_TYPES["unassigned_students"]["title"],
                )

            # 3. New registrations
            new_count = await self._count_new_registrations()
            if new_count > 0:
                await self._create_if_not_exists(
                    user_id=user.id,
                    notification_type="new_registrations",
                    message=SYSTEM_NOTIFICATION_TYPES["new_registrations"][
                        "message_template"
                    ].format(count=new_count),
                    title=SYSTEM_NOTIFICATION_TYPES["new_registrations"]["title"],
                )

            # 4. Weekly summary
            active_count = await self._count_active_students()
            await self._create_if_not_exists(
                user_id=user.id,
                notification_type="weekly_summary",
                message=SYSTEM_NOTIFICATION_TYPES["weekly_summary"][
                    "message_template"
                ].format(total=active_count),
                title=SYSTEM_NOTIFICATION_TYPES["weekly_summary"]["title"],
            )

        except Exception as e:
            logger.error(f"Error generating system notifications: {e}", exc_info=True)

    async def _count_inactive_students(self) -> int:
        """Count students with no activity in ACTIVITY_THRESHOLD_DAYS days."""
        from src.users.infrastructure.role_repository import RoleRepository

        role_repo = RoleRepository(self.db)
        student_role = await role_repo.get_student_role()

        cutoff = datetime.now(timezone.utc) - timedelta(days=ACTIVITY_THRESHOLD_DAYS)

        query = (
            select(func.count(User.id))
            .outerjoin(Student, Student.user_id == User.id)
            .where(
                and_(
                    User.role_id == student_role.id,
                    User.deleted_at.is_(None),
                    User.is_active == True,
                    (
                        Student.last_active_at.is_(None)
                        | (Student.last_active_at < cutoff)
                    ),
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def _count_unassigned_students(self) -> int:
        """Count students not enrolled in any course."""
        from src.users.infrastructure.role_repository import RoleRepository

        role_repo = RoleRepository(self.db)
        student_role = await role_repo.get_student_role()

        enrolled_ids = select(CourseEnrollment.student_id).distinct()

        query = (
            select(func.count(User.id))
            .join(Student, Student.user_id == User.id)
            .where(
                and_(
                    User.role_id == student_role.id,
                    User.deleted_at.is_(None),
                    User.is_active == True,
                    Student.id.notin_(enrolled_ids),
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def _count_new_registrations(self) -> int:
        """Count students registered in the last 7 days."""
        from src.users.infrastructure.role_repository import RoleRepository

        role_repo = RoleRepository(self.db)
        student_role = await role_repo.get_student_role()

        cutoff = datetime.now(timezone.utc) - timedelta(days=7)

        query = (
            select(func.count(User.id))
            .where(
                and_(
                    User.role_id == student_role.id,
                    User.deleted_at.is_(None),
                    User.created_at >= cutoff,
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def _count_active_students(self) -> int:
        """Count active students (any activity in the last 7 days)."""
        from src.users.infrastructure.role_repository import RoleRepository

        role_repo = RoleRepository(self.db)
        student_role = await role_repo.get_student_role()

        cutoff = datetime.now(timezone.utc) - timedelta(days=7)

        query = (
            select(func.count(User.id))
            .join(Student, Student.user_id == User.id)
            .where(
                and_(
                    User.role_id == student_role.id,
                    User.deleted_at.is_(None),
                    User.is_active == True,
                    Student.last_active_at >= cutoff,
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def _create_if_not_exists(
        self,
        user_id: UUID,
        notification_type: str,
        title: str,
        message: str,
    ) -> None:
        """Create a notification if one of the same type doesn't exist today."""
        exists = await self.repository.notification_exists(
            user_id=user_id,
            notification_type=notification_type,
            days=1,
        )
        if not exists:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                is_read=False,
                notification_type=notification_type,
                entity_type="system",
                entity_id=None,
            )
            self.db.add(notification)
            await self.db.commit()
            logger.info(
                f"Created system notification '{notification_type}' for user {user.id}"
            )

    async def mark_as_read(self, notification_id: UUID, user: User) -> bool:
        """Mark a notification as read."""
        return await self.repository.mark_as_read(notification_id, user.id)

    async def mark_all_as_read(self, user: User) -> int:
        """Mark all notifications as read for the user."""
        return await self.repository.mark_all_as_read(user.id)

    async def delete_notification(self, notification_id: UUID, user: User) -> bool:
        """Soft-delete a notification."""
        return await self.repository.delete(notification_id)
