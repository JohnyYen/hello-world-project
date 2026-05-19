from datetime import datetime
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.course.domain.course_enrollment import CourseEnrollment
from src.course.infrastructure.course_repository import CourseRepository
from src.course.api.v1.schemas.course_management import StudentEnrollmentResponse
from src.shared.domain.exceptions import NotFoundException


class ManageEnrollmentUseCase:
    """
    Inscribir/desinscribir estudiantes + soft delete cascade de curso.
    """

    def __init__(self, db: AsyncSession, course_repo: CourseRepository):
        self.db = db
        self.course_repo = course_repo

    async def enroll_students(
        self, course_id: UUID, student_ids: list[UUID]
    ) -> list[StudentEnrollmentResponse]:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException("Curso no encontrado")

        existing_ids = await self.course_repo.get_existing_enrollment_ids(course_id)
        new_ids = [sid for sid in student_ids if sid not in existing_ids]

        if new_ids:
            await self.course_repo.bulk_create_enrollments(course_id, new_ids)

        students_data = await self.course_repo.get_students_for_course(course_id)
        return [StudentEnrollmentResponse.model_validate(s) for s in students_data]

    async def unenroll_student(self, course_id: UUID, student_id: UUID) -> bool:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException("Curso no encontrado")

        existing_ids = await self.course_repo.get_existing_enrollment_ids(
            course_id
        )
        if student_id not in existing_ids:
            return False

        now = datetime.utcnow()
        result = await self.db.execute(
            update(CourseEnrollment)
            .where(
                CourseEnrollment.course_id == course_id,
                CourseEnrollment.student_id == student_id,
                CourseEnrollment.deleted_at.is_(None),
            )
            .values(deleted_at=now, is_deleted=True)
        )
        return result.rowcount > 0

    async def delete_course(self, course_id: UUID) -> bool:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException("Curso no encontrado")

        await self.course_repo.soft_delete_enrollments_for_course(course_id)
        await self.course_repo.soft_delete_professors_for_course(course_id)
        result = await self.course_repo.soft_delete_course(course_id)

        return result

    async def get_students(
        self, course_id: UUID
    ) -> list[StudentEnrollmentResponse]:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException("Curso no encontrado")

        students_data = await self.course_repo.get_students_for_course(course_id)
        return [StudentEnrollmentResponse.model_validate(s) for s in students_data]
