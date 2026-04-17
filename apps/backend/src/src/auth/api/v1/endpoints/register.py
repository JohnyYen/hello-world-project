from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.application.usecase.register_user_usecase import RegisterUserUseCase
from src.users.api.v1.schemas.user import UserLoginResponse, UserCreate
from src.shared.domain.exceptions import DuplicateEntryException


router = APIRouter(prefix="/register", dependencies=[])


@router.post(
    "",
    response_model=UserLoginResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreate,
    register_uc: RegisterUserUseCase = Depends(),
):
    """
    Registra un nuevo usuario y retorna el token de acceso JWT.

    - **username**: Nombre de usuario (debe ser único)
    - **email**: Email del usuario (debe ser único)
    - **name**: Nombre del usuario (requerido)
    - **lastname**: Apellido del usuario (opcional)
    - **password**: Contraseña del usuario (será hasheada)

    Retorna el token JWT y los datos del usuario creado.
    """
    try:
        return await register_uc.execute(user_data)
    except DuplicateEntryException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
