from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment
from src.course.domain.course_professor import CourseProfessor
from src.shared.deps import get_current_user
from src.shared.infrastructure.session import get_db
from src.shared.application.providers.statistic_providers import get_feedback_service
from src.statistic.api.v1.schemas.feedback import FeedbackCreate, FeedbackSchema
from src.statistic.application.service.feedback_service import FeedbackService
from src.users.domain.user import User


class CreateFeedbackUseCase:
    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
        feedback_service: Annotated[FeedbackService, Depends(get_feedback_service)],
        current_user: Annotated[User, Depends(get_current_user)],
    ):
        self.db = db
        self.feedback_service = feedback_service
        self.current_user = current_user

    async def execute(self, request: FeedbackCreate) -> FeedbackSchema:
        professor = self.current_user.professor
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have a professor profile",
            )

        if request.course_id:
            course = await self.db.execute(
                select(Course).where(Course.id == request.course_id)
            )
            if not course.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found",
                )

            enrollment = await self.db.execute(
                select(CourseEnrollment).where(
                    CourseEnrollment.student_id == request.student_id,
                    CourseEnrollment.course_id == request.course_id,
                )
            )
            if not enrollment.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Student is not enrolled in this course",
                )

            course_prof = await self.db.execute(
                select(CourseProfessor).where(
                    CourseProfessor.professor_id == professor.id,
                    CourseProfessor.course_id == request.course_id,
                )
            )
            if not course_prof.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Professor does not teach this course",
                )

        create_data = request.model_dump()
        create_data["professor_id"] = professor.id
        created = await self.feedback_service.create(create_data)
        return FeedbackSchema.model_validate(created)
