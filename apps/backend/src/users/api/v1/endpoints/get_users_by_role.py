from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.users.api.v1.schemas.user import UserListResponse
from src.users.application.usecase.list_users_by_role_usecase import (
    ListUsersByRoleUseCase,
)

router = APIRouter()


@router.get(
    "/by-role",
    response_model=UserListResponse,
    summary="Obtener usuarios por rol",
)
async def get_users_by_role(
    role: str = Query(
        ...,
        pattern="^(student|professor)$",
        description="Filtrar por rol: 'student' o 'professor'",
    ),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(
        100, ge=1, le=100, description="Máximo de registros a retornar"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Obtiene una lista de usuarios filtrados por rol.

    - **role**: Obligatorio. 'student' o 'professor'.
    - **skip**: Número de registros a saltar (paginación).
    - **limit**: Máximo de registros a devolver (1-100).
    """
    usecase = ListUsersByRoleUseCase(db)
    return await usecase.execute(role=role, skip=skip, limit=limit)
