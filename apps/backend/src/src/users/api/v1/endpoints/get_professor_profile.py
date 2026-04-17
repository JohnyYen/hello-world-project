from fastapi import APIRouter, Depends

from src.users.application.usecase.get_professor_profile_usecase import (
    GetProfessorProfileUseCase,
)
from src.users.api.v1.schemas.teacher import TeacherProfileResponseSchema


router = APIRouter(prefix="/professors")


@router.get("/me", response_model=TeacherProfileResponseSchema)
async def get_teacher_profile(get_profile_uc: GetProfessorProfileUseCase = Depends()):
    """
    Obtener perfil del profesor autenticado.

    Requiere autenticación mediante token JWT.
    """
    return await get_profile_uc.execute()
