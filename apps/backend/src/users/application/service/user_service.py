from typing import Optional

from src.users.infrastructure.user_repository import UserRepository
from src.users.api.v1.schemas.user import UserCreate, UserUpdate
from src.users.domain.user import User
from src.shared.domain.exceptions import (
    NotFoundException,
    DuplicateEntryException,
)
from src.auth.infrastructure.security import get_password_hash
from src.shared.application.usecase.base_service import BaseService


class UserService(BaseService):
    """
    Servicio para operaciones CRUD y validaciones sencilla de usuarios.

    Responsabilidades:
    - Operaciones CRUD directas (crear, leer, actualizar, eliminar)
    - Búsquedas por campos específicos (email, username)
    - Transformaciones simples (hashing de contraseñas en create/update)
    - Validaciones sencilla de unicidad (delegado al repositorio)

    NO contiene:
    - Lógica de negocio compleja (ver ChangePasswordUseCase en src/auth/application/usecase/)
    - Orquestación de múltiples entidades
    - Workflows completos
    """

    def __init__(self, repository: UserRepository, model: type[User]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de usuarios
            model: Clase del modelo User
        """
        super().__init__(repository, model)

    async def create_user(
        self, user_data: UserCreate, role_id: Optional[int] = None
    ) -> User:
        """
        Crea un nuevo usuario con hash de contraseña.

        Args:
            user_data: Datos validados para la creación del usuario
            role_id: ID del rol a asignar (opcional). Si es None, se asignará
                     posteriormente o quedará como NULL en la base de datos.

        Returns:
            User: Instancia del nuevo usuario creado

        Raises:
            DuplicateEntryException: Si el email o username ya existen
        """
        # Convertir el schema a dict (Pydantic v2 usa model_dump())
        data = user_data.model_dump()
        # Hashear la contraseña antes de guardar
        if "password" in data:
            data["hashed_password"] = get_password_hash(data.pop("password"))
        # Asignar role_id si se proporciona
        if role_id is not None:
            data["role_id"] = role_id

        # Crear el usuario usando el método genérico del servicio base
        return await self.create(data)

    async def get_by_email(
        self, email: str, include_deleted: bool = False
    ) -> Optional[User]:
        """
        Busca un usuario por email.

        Args:
            email: Email del usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados

        Returns:
            Optional[User]: Instancia del usuario si se encuentra, None en caso contrario
        """
        return await self.get_one_by_filters({"email": email}, include_deleted)

    async def get_by_username(
        self, username: str, include_deleted: bool = False
    ) -> Optional[User]:
        """
        Busca un usuario por nombre de usuario.

        Args:
            username: Nombre de usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados

        Returns:
            Optional[User]: Instancia del usuario si se encuentra, None en caso contrario
        """
        return await self.get_one_by_filters({"username": username}, include_deleted)

    # Métodos de conveniencia para mantener compatibilidad con endpoints existentes
    # Estos delegan a los métodos genéricos de BaseService

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario

        Returns:
            Optional[User]: Instancia del usuario si se encuentra, None en caso contrario
        """
        return await self.get_by_id(user_id)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Obtiene todos los usuarios con paginación.

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros a devolver

        Returns:
            list[User]: Lista de usuarios
        """
        return await self.get_all(skip=skip, limit=limit)

    async def get_all_users_with_role(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> list[User]:
        """
        Obtiene todos los usuarios con la relación role cargada de forma eager.

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye usuarios eliminados (soft deleted)

        Returns:
            list[User]: Lista de usuarios con role cargado
        """
        # Cast to UserRepository to access specific methods
        repo: UserRepository = self.repository  # type: ignore[assignment]
        return await repo.get_all_with_role(
            skip=skip, limit=limit, include_deleted=include_deleted
        )

    async def get_user_by_id_with_role(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por ID con la relación role cargada de forma eager.

        Args:
            user_id: ID del usuario

        Returns:
            Optional[User]: Usuario con role cargado, o None si no existe
        """
        # Cast to UserRepository to access specific methods
        repo: UserRepository = self.repository  # type: ignore[assignment]
        return await repo.get_by_id_with_role(user_id)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Actualiza un usuario existente.

        Args:
            user_id: ID del usuario a actualizar
            user_data: Datos validados para la actualización

        Returns:
            Optional[User]: Instancia del usuario actualizado, None si no se encuentra
        """
        import logging

        logger = logging.getLogger(__name__)

        # Convertir el schema a dict, solo con campos no nulos (Pydantic v2 usa model_dump)
        data = user_data.model_dump(exclude_unset=True)

        logger.info(f"[DEBUG] update_user({user_id}): data={data}")

        # Si no hay datos para actualizar, retornar el usuario actual
        if not data:
            user = await self.get_by_id(user_id)
            logger.info(
                f"[DEBUG] No data to update, returning user: {user.id if user else None}"
            )
            return user

        # Si se incluye contraseña, hashearla
        if "password" in data:
            data["hashed_password"] = get_password_hash(data.pop("password"))

        result = await self.update(user_id, data)
        logger.info(f"[DEBUG] update result: {result.id if result else None}")
        return result

    async def delete_user(self, user_id: int) -> bool:
        """
        Elimina (soft delete) un usuario.

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no se encontró
        """
        return await self.soft_delete(user_id)
