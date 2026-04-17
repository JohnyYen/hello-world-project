from fastapi import APIRouter, Depends

from src.users.application.usecase.update_student_usecase import UpdateStudentUseCase
from src.users.api.v1.schemas.student import StudentUpdate, StudentResponse


router = APIRouter(prefix="/students")


@router.put("/{id}", response_model=StudentResponse)
async def update_student(
    id: int,
    student_data: StudentUpdate,
    update_student_uc: UpdateStudentUseCase = Depends(),
):
    """
    Actualizar información del estudiante.

    Requiere autenticación y rol de professor o admin.
    """
    return await update_student_uc.execute(student_id=id, student_data=student_data)
