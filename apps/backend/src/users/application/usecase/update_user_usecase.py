from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status

from src.shared.application.providers.users_providers import get_user_service
from src.users.application.service.user_service import UserService
from src.users.api.v1.schemas.user import UserUpdate, SingleUserResponse
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


class UpdateUserUseCase:
    """
    Caso de uso para actualizar un usuario existente.

    Responsabilidades:
    - Actualizar datos del usuario
    - Hashear contraseña si se proporciona
    - Devolver respuesta con el usuario actualizado y su relación role cargada

    Este UseCase NO maneja:
    - Validación de unicidad (delegado a UserService)
    """

    def __init__(
        self,
        user_service: UserService = Depends(get_user_service),
    ):
        self.user_service = user_service

    async def execute(self, user_id: UUID, user_data: UserUpdate) -> SingleUserResponse:
        """
        Actualiza un usuario existente.

        Args:
            user_id: ID del usuario a actualizar
            user_data: Datos validados para la actualización

        Returns:
            SingleUserResponse: Respuesta con el usuario actualizado

        Raises:
            HTTPException 404: Si el usuario no existe
            HTTPException 409: Si hay valores duplicados
        """
        try:
            user = await self.user_service.update_user(user_id, user_data)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                )

            # Siempre cargar user con role para evitar lazy loading issues
            user_with_role = await self.user_service.get_user_by_id_with_role(user.id)

            return SingleUserResponse(
                message="Usuario actualizado con éxito", data=user_with_role
            )
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario no encontrado: {str(e)}",
            )
        except DuplicateEntryException as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
