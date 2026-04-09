from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from src.users.application.usecase.update_user_usecase import UpdateUserUseCase
from src.users.api.v1.schemas.user import UserUpdate, SingleUserResponse


router = APIRouter()


@router.put(
    "/{user_id}",
    response_model=SingleUserResponse,
    summary="Actualizar un usuario",
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    update_user_uc: UpdateUserUseCase = Depends(),
):
    """
    Actualiza los datos de un usuario existente por su ID.
    """
    try:
        return await update_user_uc.execute(user_id=user_id, user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
