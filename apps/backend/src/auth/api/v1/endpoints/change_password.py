from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from uuid import UUID

from src.auth.application.usecase.change_password_usecase import (
    ChangePasswordUseCase,
    InvalidPasswordException,
)
from src.users.api.v1.schemas.user import UserChangePassword, SingleUserResponse
from src.shared.domain.exceptions import InvalidCredentialsException, NotFoundException


router = APIRouter(
    prefix="/change-password",
    dependencies=[Depends(HTTPBearer())],
)


@router.post("", response_model=SingleUserResponse)
async def change_password(
    password_data: UserChangePassword,
    user_id: UUID = Query(..., description="ID del usuario"),
    change_password_uc: ChangePasswordUseCase = Depends(),
):
    """
    Cambia la contraseña de un usuario.

    - **user_id**: ID del usuario (en query parameter o body)
    - **current_password**: Contraseña actual para verificación
    - **new_password**: Nueva contraseña (mínimo 8 caracteres)
    """
    try:
        await change_password_uc.execute(
            user_id=user_id,
            current_password=password_data.current_password,
            new_password=password_data.new_password,
        )
        return SingleUserResponse(message="Contraseña cambiada exitosamente", data=None)
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
