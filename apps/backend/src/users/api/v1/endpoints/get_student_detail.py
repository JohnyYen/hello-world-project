from fastapi import APIRouter, Depends

from src.users.application.usecase.get_student_detail_usecase import (
    GetStudentDetailUseCase,
)
from src.users.api.v1.schemas.student import StudentResponse


router = APIRouter(prefix="/students")


@router.get("/{id}", response_model=StudentResponse)
async def get_student(
    id: int,
    get_student_uc: GetStudentDetailUseCase = Depends(),
):
    """
    Obtener detalle de un estudiante.

    Requiere autenticación. Professor/Admin pueden ver cualquier estudiante.
    El propio estudiante puede ver su propio perfil.
    """
    return await get_student_uc.execute(student_id=id)
