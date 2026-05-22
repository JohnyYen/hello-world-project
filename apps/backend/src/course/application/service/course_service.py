from typing import Optional
from uuid import UUID

from src.course.domain.course import Course
from src.course.infrastructure.course_repository import CourseRepository
from src.shared.application.usecase.base_service import BaseService


class CourseService(BaseService[Course]):
    """
    CRUD básico de cursos, validaciones de dominio simples.
    Delega al UseCase operaciones multi-entidad.
    """

    def __init__(self, repository: CourseRepository):
        super().__init__(repository, Course)

    async def get_course_by_id(self, course_id: UUID) -> Optional[Course]:
        return await self.get_by_id(course_id)

    async def get_course_with_relations(self, course_id: UUID) -> Optional[Course]:
        repo: CourseRepository = self.repository
        return await repo.get_by_id_with_relations(course_id)

    async def list_courses(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[Course], int]:
        courses = await self.get_all(
            skip=skip, limit=limit, order_by="school_year", descending=True
        )
        total = await self.count()
        return courses, total

    async def list_courses_with_counts(
        self,
        professor_id: Optional[UUID] = None,
        school_year: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[tuple[Course, int, int]], int]:
        repo: CourseRepository = self.repository
        return await repo.list_with_counts(
            professor_id=professor_id,
            school_year=school_year,
            skip=skip,
            limit=limit,
        )
