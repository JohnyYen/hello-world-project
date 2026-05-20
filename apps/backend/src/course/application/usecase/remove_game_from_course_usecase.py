"""
UseCase: RemoveGameFromCourseUseCase

Desasigna el juego de un curso (pone game_id en NULL).
Solo accesible por administradores.
Valida que el curso no tenga instancias de juego activas.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.course.infrastructure.course_repository import CourseRepository
from src.course.api.v1.schemas.course_management import (
    CourseDetailResponse,
    CourseResponse,
    StudentEnrollmentResponse,
    ProfessorAssignmentResponse,
)
from src.course.domain.game_assignment_exceptions import (
    GameHasActiveInstancesException,
)
from src.shared.domain.exceptions import NotFoundException


class RemoveGameFromCourseUseCase:
    """
    Caso de uso para desasignar el juego de un curso.

    Flujo:
    1. Obtiene el curso y valida que exista.
    2. Verifica que no haya instancias activas en el curso.
    3. Marca game_id en NULL.
    4. Retorna el detalle del curso.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repo = CourseRepository(db)

    async def execute(self, course_id: UUID) -> CourseDetailResponse:
        """
        Desasigna el juego de un curso.

        Args:
            course_id: UUID del curso.

        Returns:
            CourseDetailResponse con el curso actualizado (game_id en NULL).

        Raises:
            NotFoundException: Si el curso no existe.
            GameHasActiveInstancesException: Si el curso tiene game_instances activas.
        """
        course = await self.course_repo.get_by_id_with_relations(course_id)
        if not course:
            raise NotFoundException(f"Curso con ID {course_id} no encontrado.")

        # Validar que no tenga instancias activas (status en {active, paused})
        has_active = await self.course_repo.has_active_game_instances(course_id)
        if has_active:
            raise GameHasActiveInstancesException(course.name)

        # Obtener estudiantes y profesores (antes de desasignar)
        students_data = await self.course_repo.get_students_for_course(course_id)
        professors_data = await self.course_repo.get_professors_for_course(course_id)

        # Desasignar
        course.game_id = None
        await self.db.commit()
        await self.db.refresh(course)

        # Construir respuesta
        course_resp = CourseResponse.model_validate(course)
        course_resp.student_count = len(students_data)
        course_resp.professor_count = len(professors_data)

        return CourseDetailResponse(
            **course_resp.model_dump(by_alias=True),
            students=[
                StudentEnrollmentResponse.model_validate(s) for s in students_data
            ],
            professors=[
                ProfessorAssignmentResponse.model_validate(p) for p in professors_data
            ],
        )
