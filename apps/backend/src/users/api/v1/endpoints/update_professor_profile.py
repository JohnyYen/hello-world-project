from fastapi import APIRouter, Depends

from src.users.application.usecase.update_professor_profile_usecase import (
    UpdateProfessorProfileUseCase,
)
from src.users.api.v1.schemas.teacher import (
    TeacherProfileUpdate,
    TeacherUpdateResponseSchema,
)


router = APIRouter(prefix="/professors")


@router.put("/me", response_model=TeacherUpdateResponseSchema)
async def update_teacher_profile(
    profile_data: TeacherProfileUpdate,
    update_profile_uc: UpdateProfessorProfileUseCase = Depends(),
):
    """
    Actualizar perfil del profesor autenticado.

    Requiere autenticación mediante token JWT.
    """
    return await update_profile_uc.execute(profile_data)
