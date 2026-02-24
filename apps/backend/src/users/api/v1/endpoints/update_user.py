from fastapi import APIRouter, Depends

from src.users.application.usecase.update_user_usecase import UpdateUserUseCase
from src.users.api.v1.schemas.user import UserUpdate, SingleUserResponse


router = APIRouter(prefix="")


@router.put(
    "/{user_id}", response_model=SingleUserResponse, summary="Actualizar un usuario"
)
async def update_user(
    user_id: int, user_data: UserUpdate, update_user_uc: UpdateUserUseCase = Depends()
):
    """
    Actualiza la información de un usuario existente, identificado por su ID.
    """
    return await update_user_uc.execute(user_id=user_id, user_data=user_data)
