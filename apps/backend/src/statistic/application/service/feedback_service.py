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
