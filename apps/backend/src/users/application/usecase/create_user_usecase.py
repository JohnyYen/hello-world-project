from typing import Optional
from fastapi import Depends, HTTPException, status

from src.shared.application.providers.users_providers import get_user_service
from src.users.application.service.user_service import UserService
from src.users.api.v1.schemas.user import UserCreate, SingleUserResponse
from src.shared.domain.exceptions import DuplicateEntryException


class CreateUserUseCase:
    """
    Caso de uso para crear un nuevo usuario.

    Responsabilidades:
    - Crear usuario con contraseña hasheada
    - Asignar rol si se proporciona
    - Devolver respuesta con el usuario creado y su relación role cargada

    Este UseCase NO maneja:
    - Validación de unicidad (delegado a UserService)
    - Generación de tokens (ver RegisterUserUseCase)
    """

    def __init__(
        self,
        user_service: UserService = Depends(get_user_service),
    ):
        self.user_service = user_service

    async def execute(
        self, user_data: UserCreate, role_id: Optional[int] = None
    ) -> SingleUserResponse:
        """
        Crea un nuevo usuario.

        Args:
            user_data: Datos validados para la creación del usuario
            role_id: ID del rol a asignar (opcional)

        Returns:
            SingleUserResponse: Respuesta con el usuario creado

        Raises:
            DuplicateEntryException: Si el email o username ya existen
        """
        try:
            user = await self.user_service.create_user(
                user_data=user_data,
                role_id=role_id,
            )

            user_with_role = await self.user_service.get_user_by_id_with_role(user.id)

            return SingleUserResponse(
                message="Usuario creado con éxito", data=user_with_role
            )
        except DuplicateEntryException as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
