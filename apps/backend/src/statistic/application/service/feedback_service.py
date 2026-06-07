from typing import Optional
from uuid import UUID

from src.statistic.infrastructure.feedback_repository import FeedbackRepository
from src.statistic.domain.feedback import Feedback
from src.shared.application.usecase.base_service import BaseService


class FeedbackService(BaseService):
    def __init__(self, repository: FeedbackRepository, model: type[Feedback]):
        super().__init__(repository, model)

    async def get_by_student_id(
        self,
        student_id: UUID,
        include_deleted: bool = False,
    ):
        return await self.repository.get_by_student_id(
            student_id=student_id, include_deleted=include_deleted
        )

    async def get_feedback_for_student(
        self,
        student_id: UUID,
        course_ids: list[UUID],
        skip: int = 0,
        limit: int = 100,
    ):
        return await self.repository.get_by_student_and_courses(
            student_id=student_id,
            course_ids=course_ids,
            skip=skip,
            limit=limit,
        )

    async def get_feedback_for_student_with_null_courses(
        self,
        student_id: UUID,
        course_ids: list[UUID],
        skip: int = 0,
        limit: int = 100,
    ):
        """
        History view helper: returns feedback for a student whose course is
        either NULL (unscoped advice) or one of the professor's courses.
        See FeedbackRepository.get_by_student_with_null_or_courses.
        """
        return await self.repository.get_by_student_with_null_or_courses(
            student_id=student_id,
            course_ids=course_ids,
            skip=skip,
            limit=limit,
        )

    async def count_feedback_for_student_with_null_courses(
        self,
        student_id: UUID,
        course_ids: list[UUID],
    ) -> int:
        """Count counterpart of `get_feedback_for_student_with_null_courses`."""
        return await self.repository.count_by_student_with_null_or_courses(
            student_id=student_id,
            course_ids=course_ids,
        )

    async def get_feedback_for_course(
        self,
        course_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ):
        return await self.repository.get_by_course_id(
            course_id=course_id,
            skip=skip,
            limit=limit,
        )
