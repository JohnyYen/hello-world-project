from fastapi import APIRouter, Depends, Query

from src.users.application.usecase.list_users_usecase import ListUsersUseCase
from src.users.api.v1.schemas.user import UserListResponse


router = APIRouter()


@router.get("/", response_model=UserListResponse, summary="Obtener todos los usuarios")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    include_deleted: bool = False,
    list_users_uc: ListUsersUseCase = Depends(),
):
    """
    Obtiene una lista paginada de todos los usuarios registrados en el sistema.

    - **include_deleted**: Si es True, incluye usuarios eliminados (soft deleted).
      Por defecto es False para solo mostrar usuarios activos.
    """
    return await list_users_uc.execute(
        skip=skip, limit=limit, include_deleted=include_deleted
    )
