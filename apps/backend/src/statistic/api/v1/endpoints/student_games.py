from fastapi import APIRouter, Depends, status

from src.statistic.application.usecase.get_student_games_usecase import (
    GetStudentGamesUseCase,
)
from src.statistic.api.v1.schemas.student_games import StudentGamesResponse

router = APIRouter(tags=["Student Games"])


@router.get(
    "/students/{student_id}/games",
    response_model=StudentGamesResponse,
    summary="Obtener juegos disponibles del estudiante",
    description="Retorna los juegos a los que el estudiante tiene acceso a través de los cursos del profesor logueado",
    status_code=status.HTTP_200_OK,
)
async def get_student_games(
    student_id: str,
    use_case: GetStudentGamesUseCase = Depends(),
) -> StudentGamesResponse:
    """
    Obtiene los juegos disponibles para un estudiante en el contexto del profesor actual.

    Útil para el frontend: muestra al profesor solo los juegos de sus propios cursos
    a los que el estudiante está inscrito.

    Args:
        student_id: UUID del estudiante (user_id enviado por frontend o student_id directo)

    Returns:
        StudentGamesResponse: Lista de juegos disponibles
    """
    return await use_case.execute(student_id)
