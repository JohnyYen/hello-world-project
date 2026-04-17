from fastapi import APIRouter, Depends

from src.users.application.usecase.create_student_usecase import CreateStudentUseCase
from src.users.api.v1.schemas.student import StudentCreate, StudentResponse


router = APIRouter(prefix="/students")


@router.post("", response_model=StudentResponse)
async def create_student(
    student_data: StudentCreate,
    create_student_uc: CreateStudentUseCase = Depends(),
):
    """
    Registrar un nuevo estudiante.

    Requiere autenticación y rol de professor o admin.
    """
    return await create_student_uc.execute(student_data=student_data)
