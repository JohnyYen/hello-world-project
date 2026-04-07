from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment


class CourseRepository(BaseRepository[Course]):
    """
    Repositorio para el modelo Course con soporte de enrollments.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Course)

    async def get_all_with_enrollment_counts(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[tuple[Course, int]]:
        """
        Obtiene todos los cursos con la cantidad de estudiantes inscritos.

        Returns:
            Lista de tuplas (Course, student_count)
        """
        query = (
            select(Course, func.count(CourseEnrollment.student_id).label("student_count"))
            .outerjoin(CourseEnrollment, Course.id == CourseEnrollment.course_id)
            .where(Course.is_deleted == False)
            .group_by(Course.id)
            .order_by(Course.school_year.desc(), Course.period_label)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.all()

    async def get_student_ids_for_course(self, course_id: int) -> List[int]:
        """
        Obtiene los IDs de estudiantes inscritos en un curso.
        """
        query = (
            select(CourseEnrollment.student_id)
            .where(CourseEnrollment.course_id == course_id)
        )
        result = await self.db.execute(query)
        return [row[0] for row in result.all()]
