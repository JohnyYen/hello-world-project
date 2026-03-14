from typing import Optional

from src.users.infrastructure.lms_credential_repository import LMSCredentialRepository
from src.users.domain.lms_credential import LMSCredential
from src.shared.application.usecase.base_service import BaseService


class LMSCredentialService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de credenciales LMS.

    Proporciona una capa de abstracción sobre el repositorio de credenciales LMS,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: LMSCredentialRepository, model: type[LMSCredential]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de credenciales LMS
            model: Clase del modelo LMSCredential
        """
        super().__init__(repository, model)

    async def get_by_user_id(self, user_id: int) -> Optional[LMSCredential]:
        """
        Obtiene las credenciales LMS asociadas a un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            LMSCredential: Credenciales si existen, None en caso contrario
        """
        repo = self.repository  # type: ignore[attr-defined]
        return await repo.get_by_user_id(user_id)

    async def get_by_email(self, lms_email: str) -> Optional[LMSCredential]:
        """
        Obtiene las credenciales LMS por email.

        Args:
            lms_email: Email de la cuenta en el LMS

        Returns:
            LMSCredential: Credenciales si se encuentran, None en caso contrario
        """
        repo = self.repository  # type: ignore[attr-defined]
        return await repo.get_by_lms_email(lms_email)

    async def create_with_user(
        self,
        user_id: int,
        lms_url: str,
        lms_email: str,
        lms_password: str,
        lms_provider: str,
    ) -> LMSCredential:
        """
        Crea nuevas credenciales LMS asociadas a un usuario.

        Args:
            user_id: ID del usuario
            lms_url: URL del LMS
            lms_email: Email de la cuenta LMS
            lms_password: Contraseña de la cuenta LMS
            lms_provider: Proveedor LMS

        Returns:
            LMSCredential: Credenciales creadas
        """
        # Verificar que no existen credenciales para este email
        existing = await self.get_by_email(lms_email)
        if existing:
            from src.shared.domain.exceptions import DuplicateEntryException

            raise DuplicateEntryException("Ya existen credenciales LMS para este email")

        # Crear credencial
        from src.auth.infrastructure.security import get_password_hash

        data = {
            "lms_url": lms_url,
            "lms_email": lms_email,
            "lms_password": get_password_hash(lms_password),
            "lms_provider": lms_provider,
        }

        return await self.create(data)
