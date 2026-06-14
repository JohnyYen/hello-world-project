from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.statistic.api.v1.schemas.student_games import (
    StudentGamesResponse,
    StudentGameItem,
)
from src.users.domain.student import Student


class GetStudentGamesUseCase:
    """
    Caso de uso para obtener los juegos disponibles de un estudiante
    en el contexto del profesor logueado.

    La lógica es:
    1. El profesor está asociado a cursos via CourseProfessor
    2. El estudiante está inscrito a cursos via CourseEnrollment
    3. Los cursos pueden tener un juego asociado (course.game_id)
    4. Retornamos los juegos de los cursos donde coinciden profesor y estudiante

    Esto asegura que el profesor SOLO vea juegos a los que tiene acceso
    a través de sus propios cursos.
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(self, student_id: str) -> StudentGamesResponse:
        """
        Obtiene los juegos disponibles para un estudiante.

        Args:
            student_id: UUID del estudiante (puede ser user_id o student_id)

        Returns:
            StudentGamesResponse: Lista de juegos disponibles
        """
        try:
            student_uuid = UUID(student_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de estudiante inválido",
            )

        # Validar rol
        if self.current_user.role.role_name not in ["admin", "professor"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para ver juegos del estudiante",
            )

        # Resolver student_id (el frontend puede enviar user_id)
        resolved_student_id = await self._resolve_student_id(student_uuid)

        # Si es admin, traer todos los juegos del estudiante
        if self.current_user.role.role_name == "admin":
            games = await self._get_all_student_games(resolved_student_id)
        else:
            # Si es profesor, filtrar por sus cursos
            games = await self._get_professor_student_games(resolved_student_id)

        return StudentGamesResponse(games=games)

    async def _resolve_student_id(self, given_id: UUID) -> UUID:
        """
        Resuelve un user_id a student_id si corresponde.
        Misma lógica que en GetStudentProgressUseCase.
        """
        stmt = select(Student.id).where(Student.user_id == given_id)
        result = await self.db.execute(stmt)
        student_row = result.scalar_one_or_none()
        return student_row if student_row is not None else given_id

    async def _get_all_student_games(
        self, student_id: UUID
    ) -> list[StudentGameItem]:
        """
        Para admin: obtiene todos los juegos donde el estudiante
        tiene progreso registrado (via progresses table).

        Usamos progresses como fuente de verdad porque un estudiante
        puede tener progreso en juegos sin estar inscrito en un curso
        que los contenga (ej: xAPI statements directos).
        """
        from src.statistic.domain.progress import Progress
        from src.game.domain.segment_level import SegmentLevel
        from src.game.domain.level import Level
        from src.game.domain.game import Game

        stmt = (
            select(Game.id, Game.title, Game.description)
            .distinct()
            .select_from(Progress)
            .join(SegmentLevel, Progress.segment_level_id == SegmentLevel.id)
            .join(Level, SegmentLevel.level_number_id == Level.id)
            .join(Game, Level.game_id == Game.id)
            .where(Progress.student_id == student_id)
            .where(Progress.deleted_at.is_(None))
            .where(Game.deleted_at.is_(None))
            .order_by(Game.title)
        )

        result = await self.db.execute(stmt)
        rows = result.fetchall()

        return [
            StudentGameItem(
                id=str(row.id),
                title=row.title,
                description=row.description,
            )
            for row in rows
        ]

    async def _get_professor_student_games(
        self, student_id: UUID
    ) -> list[StudentGameItem]:
        """
        Para profesor: obtiene juegos donde el estudiante tiene progreso
        Y el profesor dicta al menos un curso que tiene ese juego.

        Esto mantiene la seguridad (el profesor solo ve juegos de sus cursos)
        pero usa progresses como fuente de verdad en lugar de course_enrollments,
        cubriendo el caso donde hay progreso sin inscripción a curso.
        """
        from src.statistic.domain.progress import Progress
        from src.game.domain.segment_level import SegmentLevel
        from src.game.domain.level import Level
        from src.game.domain.game import Game
        from src.course.domain.course import Course
        from src.course.domain.course_professor import CourseProfessor
        from src.users.domain.professor import Professor

        # Obtener el professor_id a partir del current_user
        professor_subq = (
            select(Professor.id)
            .where(Professor.user_id == self.current_user.id)
            .where(Professor.deleted_at.is_(None))
        )

        stmt = (
            select(Game.id, Game.title, Game.description)
            .distinct()
            .select_from(Progress)
            .join(SegmentLevel, Progress.segment_level_id == SegmentLevel.id)
            .join(Level, SegmentLevel.level_number_id == Level.id)
            .join(Game, Level.game_id == Game.id)
            # Filtrar solo juegos que están en cursos del profesor
            .join(Course, Course.game_id == Game.id)
            .join(CourseProfessor, CourseProfessor.course_id == Course.id)
            .where(Progress.student_id == student_id)
            .where(CourseProfessor.professor_id.in_(professor_subq))
            .where(Progress.deleted_at.is_(None))
            .where(Game.deleted_at.is_(None))
            .where(Course.deleted_at.is_(None))
            .order_by(Game.title)
        )

        result = await self.db.execute(stmt)
        rows = result.fetchall()

        return [
            StudentGameItem(
                id=str(row.id),
                title=row.title,
                description=row.description,
            )
            for row in rows
        ]
