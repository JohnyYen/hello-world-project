from fastapi import APIRouter, Depends, HTTPException, status

from src.users.application.usecase.delete_user_usecase import DeleteUserUseCase
from src.users.api.v1.schemas.user import SingleUserResponse


router = APIRouter(prefix="")


@router.delete(
    "/{user_id}", response_model=SingleUserResponse, summary="Eliminar un usuario"
)
async def delete_user(user_id: int, delete_user_uc: DeleteUserUseCase = Depends()):
    """
    Realiza un "soft delete" de un usuario, marcándolo como eliminado en la base de datos.
    Devuelve el usuario eliminado.
    """
    return await delete_user_uc.execute(user_id=user_id)
