from fastapi import APIRouter, Depends

from src.users.application.usecase.update_teacher_settings_usecase import (
    UpdateTeacherSettingsUseCase,
)
from src.users.api.v1.schemas.teacher import (
    TeacherSettingsUpdate,
    TeacherSettingsResponseSchema,
)


router = APIRouter(prefix="/professors")


@router.put("/settings", response_model=TeacherSettingsResponseSchema)
async def update_teacher_settings(
    settings_data: TeacherSettingsUpdate,
    update_settings_uc: UpdateTeacherSettingsUseCase = Depends(),
):
    """
    Actualizar configuraciones del dashboard del profesor.

    Requiere autenticación mediante token JWT.
    """
    return await update_settings_uc.execute(settings_data)
