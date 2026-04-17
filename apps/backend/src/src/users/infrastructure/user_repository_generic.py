from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.users.domain.user import User


class UserRepository(BaseRepository[User]):
    """
    Repositorio específico para el modelo User.

    Hereda todas las operaciones CRUD del BaseRepository y puede sobrescribir
    métodos específicos si es necesario.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(
        self, email: str, include_deleted: bool = False
    ) -> Optional[User]:
        """
        Obtiene un usuario por email.

        Args:
            email: Email del usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados

        Returns:
            User: Instancia del modelo User si se encuentra, None en caso contrario
        """
        filters = {"email": email}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_username(
        self, username: str, include_deleted: bool = False
    ) -> Optional[User]:
        """
        Obtiene un usuario por nombre de usuario.

        Args:
            username: Nombre de usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados

        Returns:
            User: Instancia del modelo User si se encuentra, None en caso contrario
        """
        filters = {"username": username}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def create(self, obj_in: Dict[str, Any]) -> User:
        """
        Método sobrescrito para crear un usuario con lógica específica de validación.
        """
        # Validar unicidad de email y username antes de crear
        existing_email = await self.get_by_email(obj_in.get("email"))
        if existing_email:
            from src.shared.domain.exceptions import DuplicateEntryException

            raise DuplicateEntryException("El email ya está registrado")

        if obj_in.get("username"):
            existing_username = await self.get_by_username(obj_in.get("username"))
            if existing_username:
                from src.shared.domain.exceptions import DuplicateEntryException

                raise DuplicateEntryException("El nombre de usuario ya está en uso")

        # Llamar al método padre para crear el usuario
        return await super().create(obj_in)
