from fastapi import APIRouter, Depends

from src.users.application.usecase.get_user_usecase import GetUserUseCase
from src.users.api.v1.schemas.user import SingleUserResponse


router = APIRouter()


@router.get(
    "/{user_id}", response_model=SingleUserResponse, summary="Obtener un usuario por ID"
)
async def get_user(user_id: int, get_user_uc: GetUserUseCase = Depends()):
    """
    Busca y devuelve un usuario por su ID único.
    """
    return await get_user_uc.execute(user_id)
