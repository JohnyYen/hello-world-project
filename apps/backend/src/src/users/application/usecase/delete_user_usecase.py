from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status

from src.shared.application.providers.users_providers import get_user_service
from src.users.application.service.user_service import UserService
from src.users.api.v1.schemas.user import SingleUserResponse
from src.shared.domain.exceptions import NotFoundException


class DeleteUserUseCase:
    """
    Caso de uso para eliminar (soft delete) un usuario.

    Responsabilidades:
    - Realizar soft delete del usuario
    - Devolver el usuario eliminado con la relación role cargada

    Este UseCase NO maneja:
    - Validación de permisos
    - Eliminación permanente (hard delete)
    """

    def __init__(
        self,
        user_service: UserService = Depends(get_user_service),
    ):
        self.user_service = user_service

    async def execute(self, user_id: UUID) -> SingleUserResponse:
        """
        Elimina (soft delete) un usuario.

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            SingleUserResponse: Respuesta con el usuario eliminado

        Raises:
            HTTPException 404: Si el usuario no existe
        """
        # Obtener el usuario antes de eliminar para devolverlo
        user_with_role = await self.user_service.get_user_by_id_with_role(user_id)

        if not user_with_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        # ACCEDER A TODOS LOS CAMPOS MIENTRAS LA SESIÓN ESTÁ ACTIVA
        # Esto evita el error "MissingGreenlet" al acceder a updated_at después del soft delete
        user_dict = {
            "id": user_with_role.id,
            "username": user_with_role.username,
            "email": user_with_role.email,
            "name": user_with_role.name,
            "lastname": user_with_role.lastname,
            "is_active": user_with_role.is_active,
            "created_at": user_with_role.created_at,
            "updated_at": user_with_role.updated_at,
            "role": user_with_role.role,
        }

        # Realizar el soft delete DESPUÉS de acceder a todos los campos
        deleted = await self.user_service.delete_user(user_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo eliminar el usuario",
            )

        return SingleUserResponse(
            message="Usuario eliminado exitosamente", data=user_dict
        )
