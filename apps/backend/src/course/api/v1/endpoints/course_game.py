"""
Endpoints de catálogo y gestión de juegos por curso.

- GET /courses/available-games  → Lista juegos NO asignados a ningún curso
- GET /courses/{course_id}/game → Devuelve el juego asignado (si existe)
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps.game_publisher import require_professor_ownership
from src.course.application.usecase.list_available_games_usecase import (
    ListAvailableGamesUseCase,
)
from src.course.infrastructure.course_repository import CourseRepository
from src.course.api.v1.schemas.course_management import (
    AvailableGamesResponse,
    AssignedGameResponse,
)
from src.shared.domain.exceptions import NotFoundException

router = APIRouter()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def get_available_games_usecase(
    db: AsyncSession = Depends(get_db),
) -> ListAvailableGamesUseCase:
    return ListAvailableGamesUseCase(db)


async def get_course_repo(
    db: AsyncSession = Depends(get_db),
) -> CourseRepository:
    return CourseRepository(db)


# ---------------------------------------------------------------------------
# GET /courses/available-games
# Lista todos los juegos publicados NO asignados a ningún curso.
# ---------------------------------------------------------------------------


@router.get(
    "/available-games",
    response_model=AvailableGamesResponse,
    summary="Lista juegos disponibles del catálogo",
)
async def list_available_games(
    usecase: ListAvailableGamesUseCase = Depends(get_available_games_usecase),
):
    """
    Devuelve todos los juegos que aún no están asignados a ningún curso.

    Cualquier usuario autenticado puede consultar el catálogo.
    Requiere token JWT (heredado del router padre).
    """
    return await usecase.execute()


# ---------------------------------------------------------------------------
# GET /courses/{course_id}/game
# Devuelve el juego actualmente asignado al curso.
# ---------------------------------------------------------------------------


@router.get(
    "/{course_id}/game",
    response_model=AssignedGameResponse,
    summary="Devuelve el juego asignado a un curso",
)
async def get_assigned_game(
    course_id: UUID = Path(..., description="UUID del curso"),
    repo: CourseRepository = Depends(get_course_repo),
    current_user=Depends(require_professor_ownership),
):
    """
    Devuelve el juego actualmente asignado a un curso.

    - El profesor debe estar asignado al curso (verificado por `require_professor_ownership`).
    - Si el curso no tiene juego asignado, retorna 204 No Content.
    """
    course = await repo.get_course_with_game(course_id)
    if not course:
        raise NotFoundException(f"Curso con ID {course_id} no encontrado.")

    if course.game_id is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Este curso no tiene un juego asignado.",
        )

    return AssignedGameResponse.model_validate(course.game)
