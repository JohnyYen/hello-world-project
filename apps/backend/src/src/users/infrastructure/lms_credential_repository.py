from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.users.domain.lms_credential import LMSCredential


class LMSCredentialRepository(BaseRepository[LMSCredential]):
    """
    Repositorio específico para el modelo LMSCredential.

    Hereda todas las operaciones CRUD del BaseRepository.
    Proporciona métodos específicos para buscar credenciales LMS.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, LMSCredential)

    async def get_by_lms_email(self, lms_email: str) -> Optional[LMSCredential]:
        """
        Obtiene una credencial LMS por email de la plataforma.

        Args:
            lms_email: Email de la cuenta en el LMS

        Returns:
            LMSCredential: Instancia del modelo si se encuentra, None en caso contrario
        """
        return await self.get_one_by_filters({"lms_email": lms_email})

    async def get_by_user_id(self, user_id: int) -> Optional[LMSCredential]:
        """
        Obtiene la credencial LMS asociada a un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            LMSCredential: Instancia del modelo si se encuentra, None en caso contrario
        """
        # Buscar el usuario y obtener su credencial LMS
        from src.users.domain.user import User

        query = select(self.model).join(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_provider(self, provider: str) -> list[LMSCredential]:
        """
        Obtiene todas las credenciales LMS para un proveedor específico.

        Args:
            provider: Nombre del proveedor (moodle, canvas, etc.)

        Returns:
            list[LMSCredential]: Lista de credenciales para el proveedor
        """
        return await self.get_by_filters({"lms_provider": provider})
