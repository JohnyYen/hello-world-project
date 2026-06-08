from typing import List
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.statistic.domain.feedback import Feedback


class FeedbackRepository(BaseRepository[Feedback]):
    """
    Repositorio específico para el modelo Feedback.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Feedback)

    async def get_by_student_id(
        self, student_id: UUID, include_deleted: bool = False
    ) -> List[Feedback]:
        filters = {"student_id": student_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_course_id(
        self,
        course_id: UUID,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[Feedback]:
        filters = {"course_id": course_id}
        return await self.get_all(
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
            filters=filters,
        )

    async def get_by_student_and_courses(
        self,
        student_id: UUID,
        course_ids: list[UUID],
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[Feedback]:
        filters = {"student_id": student_id, "course_id": course_ids}
        return await self.get_all(
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
            filters=filters,
        )

    async def get_by_student_with_null_or_courses(
        self,
        student_id: UUID,
        course_ids: list[UUID],
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[Feedback]:
        """
        Return feedback for `student_id` whose course is either NULL or one
        of the given `course_ids`. SQL's `NULL IN (...)` is always UNKNOWN,
        so the regular `get_by_student_and_courses` (which builds a plain
        IN clause) silently drops NULL-course rows. The submit form allows
        `course_id=NULL`, so we need this OR variant.
        """
        query = select(Feedback).where(
            and_(
                Feedback.student_id == student_id,
                or_(
                    Feedback.course_id.is_(None),
                    Feedback.course_id.in_(course_ids),
                ),
            )
        )
        if not include_deleted:
            query = query.where(Feedback.deleted_at.is_(None))
        query = (
            query.order_by(Feedback.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_by_student_with_null_or_courses(
        self,
        student_id: UUID,
        course_ids: list[UUID],
        include_deleted: bool = False,
    ) -> int:
        """Count counterpart of `get_by_student_with_null_or_courses`."""
        query = select(func.count(Feedback.id)).where(
            and_(
                Feedback.student_id == student_id,
                or_(
                    Feedback.course_id.is_(None),
                    Feedback.course_id.in_(course_ids),
                ),
            )
        )
        if not include_deleted:
            query = query.where(Feedback.deleted_at.is_(None))
        result = await self.db.execute(query)
        return int(result.scalar() or 0)

    async def get_by_rating(
        self, rating: int, include_deleted: bool = False
    ) -> List[Feedback]:
        filters = {"rating": rating}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_all_with_student(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
        order_by: str = "created_at",
        descending: bool = True,
    ) -> List[Feedback]:
        return await self.get_all(
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
            order_by=order_by,
            descending=descending,
        )
