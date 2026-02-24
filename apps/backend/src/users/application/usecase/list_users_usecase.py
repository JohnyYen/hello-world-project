from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.users.application.service.user_service import UserService
from src.users.api.v1.schemas.user import UserListResponse


class ListUsersUseCase:
    """
    Caso de uso para listar usuarios con paginación.

    Responsabilidades:
    - Obtener lista de usuarios con paginación
    - Cargar relaciones de forma eager (role) para evitar lazy loading
    - Devolver respuesta formateada con lista de usuarios

    Este UseCase NO maneja:
    - Filtrado por criterios específicos (ver otros use cases)
    - Creación, actualización o eliminación de usuarios
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        user_service: UserService = Depends(),
    ):
        self.db = db
        self.user_service = user_service

    async def execute(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> UserListResponse:
        """
        Ejecuta la lista de usuarios.

        Args:
            skip: Número de registros a saltar (paginación)
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye usuarios eliminados (soft deleted)

        Returns:
            UserListResponse: Respuesta con lista de usuarios y metadata
        """
        users = await self.user_service.get_all_users_with_role(
            skip=skip, limit=limit, include_deleted=include_deleted
        )
        return UserListResponse(message="Usuarios obtenidos con éxito", data=users)
