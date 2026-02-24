from fastapi import APIRouter, Depends

from src.users.application.usecase.get_teacher_settings_usecase import (
    GetTeacherSettingsUseCase,
)
from src.users.api.v1.schemas.teacher import TeacherSettingsResponseSchema


router = APIRouter(prefix="/professors")


@router.get("/settings", response_model=TeacherSettingsResponseSchema)
async def get_teacher_settings(get_settings_uc: GetTeacherSettingsUseCase = Depends()):
    """
    Obtener configuraciones del dashboard del profesor.

    Requiere autenticación mediante token JWT.
    """
    return await get_settings_uc.execute()
