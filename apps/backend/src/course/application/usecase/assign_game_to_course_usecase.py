"""
UseCase: AssignGameToCourseUseCase

Asigna un juego a un curso. Solo accesible por administradores.
 Valida: el juego exista, el curso no tenga juego previamente asignado.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.course.infrastructure.course_repository import CourseRepository
from src.game.infrastructure.game_repository import GameRepository
from src.course.api.v1.schemas.course_management import (
    CourseDetailResponse,
    CourseResponse,
    StudentEnrollmentResponse,
    ProfessorAssignmentResponse,
    AssignedGameResponse,
)
from src.course.domain.game_assignment_exceptions import (
    GameAlreadyAssignedException,
    GameNotFoundException,
)
from src.shared.domain.exceptions import NotFoundException


class AssignGameToCourseUseCase:
    """
    Caso de uso para asignar un juego a un curso.

    Flujo:
    1. Verifica que el juego exista y no esté eliminado.
    2. Verifica que el curso no tenga ya un juego asignado.
    3. Actualiza `courses.game_id`.
    4. Retorna el detalle del curso actualizado.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repo = CourseRepository(db)
        self.game_repo = GameRepository(db)

    async def execute(
        self, course_id: UUID, game_id: UUID
    ) -> CourseDetailResponse:
        """
        Asigna un juego a un curso.

        Args:
            course_id: UUID del curso destino.
            game_id: UUID del juego a asignar.

        Returns:
            CourseDetailResponse con el curso actualizado.

        Raises:
            NotFoundException: Si el curso o el juego no existen.
            GameAlreadyAssignedException: Si el curso ya tiene un juego asignado.
        """
        # 1. Obtener curso
        course = await self.course_repo.get_by_id_with_relations(course_id)
        if not course:
            raise NotFoundException(f"Curso con ID {course_id} no encontrado.")

        # 2. Verificar que no tenga juego ya asignado
        if course.game_id is not None:
            raise GameAlreadyAssignedException(course.name)

        # 3. Obtener juego
        game = await self.game_repo.get_by_id(game_id, include_deleted=False)
        if not game:
            raise GameNotFoundException(str(game_id))

        # 4. Asignar
        course.game_id = game_id
        await self.db.commit()
        await self.db.refresh(course)

        # 5. Obtener datos para respuesta
        students_data = await self.course_repo.get_students_for_course(course_id)
        professors_data = await self.course_repo.get_professors_for_course(course_id)

        course_resp = CourseResponse.model_validate(course)
        course_resp.student_count = len(students_data)
        course_resp.professor_count = len(professors_data)

        game_data = AssignedGameResponse.model_validate(game)

        return CourseDetailResponse(
            **course_resp.model_dump(by_alias=True),
            students=[
                StudentEnrollmentResponse.model_validate(s) for s in students_data
            ],
            professors=[
                ProfessorAssignmentResponse.model_validate(p) for p in professors_data
            ],
            game=game_data,
        )
