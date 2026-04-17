from typing import List, Optional, Dict
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

    async def get_all_student_ids_batch(
        self,
        course_ids: Optional[List[int]] = None,
    ) -> Dict[int, List[int]]:
        """
        Obtiene IDs de estudiantes para múltiples cursos en una sola query.

        Args:
            course_ids: Si se proporciona, filtra solo estos cursos.
                        Si None, retorna todos los cursos.

        Returns:
            Dict mapeando course_id -> lista de student_ids.
        """
        query = select(CourseEnrollment.course_id, CourseEnrollment.student_id)
        if course_ids:
            query = query.where(CourseEnrollment.course_id.in_(course_ids))

        result = await self.db.execute(query)
        rows = result.all()

        mapping: Dict[int, List[int]] = {}
        for course_id, student_id in rows:
            if course_id not in mapping:
                mapping[course_id] = []
            mapping[course_id].append(student_id)

        return mapping

    async def get_courses_by_ids(self, course_ids: List[int]) -> List[Course]:
        """
        Obtiene múltiples objetos Course por ID en una sola query.
        """
        query = select(Course).where(
            Course.id.in_(course_ids),
            Course.is_deleted == False,
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
