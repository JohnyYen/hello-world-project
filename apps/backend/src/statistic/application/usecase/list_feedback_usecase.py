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
from src.users.domain.student import Student
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

    async def _resolve_student_id(self, submitted_id: UUID) -> UUID:
        """
        Map the `student_id` the client sent to the real `students.id` row.

        Mirrors CreateFeedbackUseCase._resolve_student_id: the dashboard
        URL `/dashboard/students/{id}` is keyed by `User.id`, while
        `feedbacks.student_id` FK points to `students.id`. We accept
        either form and return the canonical `students.id`. If neither
        exists we 404.
        """
        direct = await self.db.execute(
            select(Student).where(Student.id == submitted_id)
        )
        if direct.scalar_one_or_none():
            return submitted_id

        by_user = await self.db.execute(
            select(Student).where(Student.user_id == submitted_id)
        )
        student = by_user.scalar_one_or_none()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found",
            )
        return student.id

    async def execute(
        self,
        student_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> FeedbackListResponse:
        # --- Professor flow: view feedback for any student in their courses ---
        professor = self.current_user.professor
        if professor:
            result = await self.db.execute(
                select(CourseProfessor.course_id).where(
                    CourseProfessor.professor_id == professor.id
                )
            )
            course_ids = list(result.scalars().all())

            if not course_ids:
                return FeedbackListResponse(items=[], total=0, skip=skip, limit=limit)

            canonical_student_id = await self._resolve_student_id(student_id)

            feedbacks = await self.feedback_service.get_feedback_for_student_with_null_courses(
                student_id=canonical_student_id,
                course_ids=course_ids,
                skip=skip,
                limit=limit,
            )

            total = await self.feedback_service.count_feedback_for_student_with_null_courses(
                student_id=canonical_student_id,
                course_ids=course_ids,
            )

            return FeedbackListResponse(
                items=[FeedbackSchema.model_validate(f) for f in feedbacks],
                total=total,
                skip=skip,
                limit=limit,
            )

        # --- Student flow: only their own feedback, no course filtering ---
        # Query student separately to avoid async lazy-loading (MissingGreenlet)
        student_result = await self.db.execute(
            select(Student).where(Student.user_id == self.current_user.id)
        )
        student = student_result.scalar_one_or_none()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have a professor or student profile",
            )

        canonical_student_id = await self._resolve_student_id(student_id)

        # Students can only see their own feedback
        if canonical_student_id != student.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only view their own feedback",
            )

        feedbacks = await self.feedback_service.get_all(
            skip=skip,
            limit=limit,
            filters={"student_id": canonical_student_id},
        )
        total = await self.feedback_service.count(
            filters={"student_id": canonical_student_id},
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
