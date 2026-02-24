from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.users.application.service.user_service import UserService
from src.users.api.v1.schemas.user import SingleUserResponse
from src.shared.domain.exceptions import NotFoundException


class GetUserUseCase:
    """
    Caso de uso para obtener un usuario por ID.

    Responsabilidades:
    - Buscar usuario por ID con la relación role cargada de forma eager
    - Manejar el caso de usuario no encontrado
    - Devolver respuesta formateada con los datos del usuario

    Este UseCase NO maneja:
    - Creación, actualización o eliminación de usuarios
    - Listado de múltiples usuarios (ver ListUsersUseCase)
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        user_service: UserService = Depends(),
    ):
        self.db = db
        self.user_service = user_service

    async def execute(self, user_id: int) -> SingleUserResponse:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario a buscar

        Returns:
            SingleUserResponse: Respuesta con los datos del usuario

        Raises:
            HTTPException 404: Si el usuario no existe
        """
        user = await self.user_service.get_user_by_id_with_role(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        return SingleUserResponse(message="Usuario obtenido con éxito", data=user)
