from fastapi import APIRouter, Depends, HTTPException, status

from src.users.application.usecase.create_user_usecase import CreateUserUseCase
from src.users.api.v1.schemas.user import UserCreate, SingleUserResponse


router = APIRouter()


@router.post(
    "/",
    response_model=SingleUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
)
async def create_user(
    user_data: UserCreate, create_user_uc: CreateUserUseCase = Depends()
):
    """
    Crea un nuevo usuario en la base de datos con la información proporcionada.
    - **email**: El correo electrónico del usuario (debe ser único).
    - **username**: El nombre de usuario (opcional, debe ser único si se proporciona).
    - **name**: El nombre del usuario (requerido).
    - **password**: La contraseña del usuario.
    """
    return await create_user_uc.execute(user_data=user_data)
