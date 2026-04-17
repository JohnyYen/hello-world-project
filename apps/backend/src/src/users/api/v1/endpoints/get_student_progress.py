from fastapi import APIRouter, Depends

from src.users.application.usecase.get_student_progress_usecase import (
    GetStudentProgressUseCase,
)
from src.users.api.v1.schemas.student import StudentProgressResponse


router = APIRouter(prefix="/students")


@router.get("/{id}/progress", response_model=StudentProgressResponse)
async def get_student_progress(
    id: int,
    get_progress_uc: GetStudentProgressUseCase = Depends(),
):
    """
    Obtener progreso del estudiante.

    Requiere autenticación. Professor/Admin pueden ver cualquier estudiante.
    El propio estudiante puede ver su propio progreso.
    """
    return await get_progress_uc.execute(student_id=id)
