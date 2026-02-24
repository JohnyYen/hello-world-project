from fastapi import APIRouter, Depends

from src.users.application.usecase.delete_student_usecase import DeleteStudentUseCase


router = APIRouter(prefix="/students")


@router.delete("/{id}")
async def delete_student(
    id: int,
    delete_student_uc: DeleteStudentUseCase = Depends(),
):
    """
    Eliminar estudiante (soft delete).

    Requiere autenticación y rol de professor o admin.
    """
    return await delete_student_uc.execute(student_id=id)
