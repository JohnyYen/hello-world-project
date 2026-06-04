from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.course.domain.course_professor import CourseProfessor
from src.shared.deps import get_current_user
from src.shared.infrastructure.session import get_db
from src.shared.application.providers.statistic_providers import get_feedback_service
from src.statistic.api.v1.schemas.feedback import (
    FeedbackListResponse,
    FeedbackSchema,
)
from src.statistic.application.service.feedback_service import FeedbackService
from src.users.domain.user import User


class ListFeedbackUseCase:
    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
        feedback_service: Annotated[FeedbackService, Depends(get_feedback_service)],
        current_user: Annotated[User, Depends(get_current_user)],
    ):
        self.db = db
        self.feedback_service = feedback_service
        self.current_user = current_user

    async def execute(
        self,
        student_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> FeedbackListResponse:
        professor = self.current_user.professor
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have a professor profile",
            )

        result = await self.db.execute(
            select(CourseProfessor.course_id).where(
                CourseProfessor.professor_id == professor.id
            )
        )
        course_ids = list(result.scalars().all())

        if not course_ids:
            return FeedbackListResponse(items=[], total=0, skip=skip, limit=limit)

        feedbacks = await self.feedback_service.get_feedback_for_student(
            student_id=student_id,
            course_ids=course_ids,
            skip=skip,
            limit=limit,
        )

        total = await self.feedback_service.count(
            filters={"student_id": student_id, "course_id": course_ids},
        )

        return FeedbackListResponse(
            items=[FeedbackSchema.model_validate(f) for f in feedbacks],
            total=total,
            skip=skip,
            limit=limit,
        )

    async def execute_by_course(
        self,
        course_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> FeedbackListResponse:
        professor = self.current_user.professor
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have a professor profile",
            )

        course_prof = await self.db.execute(
            select(CourseProfessor).where(
                CourseProfessor.professor_id == professor.id,
                CourseProfessor.course_id == course_id,
            )
        )
        if not course_prof.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Professor does not teach this course",
            )

        feedbacks = await self.feedback_service.get_feedback_for_course(
            course_id=course_id,
            skip=skip,
            limit=limit,
        )

        total = await self.feedback_service.count(
            filters={"course_id": course_id},
        )

        return FeedbackListResponse(
            items=[FeedbackSchema.model_validate(f) for f in feedbacks],
            total=total,
            skip=skip,
            limit=limit,
        )
