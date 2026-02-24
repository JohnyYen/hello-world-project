from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.domain.role import Role
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.shared.domain.exceptions import NotFoundException


class RoleRepository(BaseRepository[Role]):
    """Repositorio para operaciones relacionadas con roles de usuario."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Role)

    async def get_by_name(self, role_name: str) -> Optional[Role]:
        """
        Busca un rol por su nombre.

        Args:
            role_name: Nombre del rol a buscar (ej: 'admin', 'professor', 'student')

        Returns:
            Optional[Role]: Instancia del rol si se encuentra, None en caso contrario
        """
        query = select(self.model).where(self.model.role_name == role_name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_professor_role(self) -> Role:
        """
        Obtiene el rol de 'professor'.

        Returns:
            Role: Instancia del rol professor

        Raises:
            NotFoundException: Si el rol professor no existe en la base de datos
        """
        role = await self.get_by_name("professor")
        if not role:
            raise NotFoundException(
                "Error del sistema: rol 'professor' no configurado. "
                "Ejecute el seed de roles antes de registrar usuarios."
            )
        return role

    async def get_admin_role(self) -> Role:
        """
        Obtiene el rol de 'admin'.

        Returns:
            Role: Instancia del rol admin

        Raises:
            NotFoundException: Si el rol admin no existe en la base de datos
        """
        role = await self.get_by_name("admin")
        if not role:
            raise NotFoundException(
                "Error del sistema: rol 'admin' no configurado. "
                "Ejecute el seed de roles antes de continuar."
            )
        return role

    async def get_student_role(self) -> Role:
        """
        Obtiene el rol de 'student'.

        Returns:
            Role: Instancia del rol student

        Raises:
            NotFoundException: Si el rol student no existe en la base de datos
        """
        role = await self.get_by_name("student")
        if not role:
            raise NotFoundException(
                "Error del sistema: rol 'student' no configurado. "
                "Ejecute el seed de roles antes de continuar."
            )
        return role
