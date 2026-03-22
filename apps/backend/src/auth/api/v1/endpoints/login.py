from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.application.usecase.authenticate_usecase import AuthenticateUseCase
from src.users.api.v1.schemas.user import UserLoginResponse, UserLogin
from src.shared.domain.exceptions import InvalidCredentialsException


router = APIRouter(prefix="/login", security=[])


@router.post("", response_model=UserLoginResponse)
async def login_for_access_token(
    form_data: UserLogin,
    authenticate_uc: AuthenticateUseCase = Depends(),
):
    """
    Autentica un usuario y retorna el token de acceso JWT.

    - **username**: Username del usuario (opcional)
    - **email**: Email del usuario (opcional)
    - **password**: Contraseña del usuario

    Nota: Proporcionar username O email, no ambos requeridos.

    Retorna el token JWT y los datos del usuario autenticado.
    """
    try:
        return await authenticate_uc.execute(
            username=form_data.username,
            email=form_data.email,
            password=form_data.password,
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
