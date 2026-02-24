from fastapi import Depends

from src.users.application.service.user_service import UserService
from src.shared.domain.exceptions import NotFoundException, InvalidCredentialsException
from src.auth.infrastructure.security import verify_password, get_password_hash


class InvalidPasswordException(Exception):
    """Excepción para contraseñas que no cumplen los requisitos."""

    pass


class ChangePasswordUseCase:
    """
    Caso de uso para cambiar la contraseña de un usuario.

    Responsabilidades:
    - Verificar que el usuario existe
    - Validar que la contraseña actual es correcta
    - Validar reglas de complejidad de la nueva contraseña
    - Actualizar la contraseña con hashing
    - (Opcional) Invalidar tokens activos
    - (Opcional) Registrar evento de seguridad
    """

    def __init__(self, user_service: UserService = Depends()):
        self.user_service = user_service

    async def execute(
        self, user_id: int, current_password: str, new_password: str
    ) -> bool:
        """
        Ejecuta el flujo de cambio de contraseña.

        Args:
            user_id: ID del usuario
            current_password: Contraseña actual para verificar
            new_password: Nueva contraseña

        Returns:
            bool: True si se cambió correctamente

        Raises:
            InvalidCredentialsException: Si la contraseña actual es incorrecta o no cumple requisitos
            NotFoundException: Si el usuario no existe
        """
        # 1. Validar reglas de negocio de complejidad
        if not self._validate_password_strength(new_password):
            raise InvalidPasswordException(
                "La contraseña debe tener al menos 8 caracteres"
            )

        # 2. Buscar usuario
        user = await self.user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"Usuario con id={user_id} no encontrado")

        # 3. Verificar contraseña actual
        if not verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsException("La contraseña actual es incorrecta")

        # 4. Actualizar contraseña
        await self.user_service.update(
            user_id, {"hashed_password": get_password_hash(new_password)}
        )

        # 5. Aquí podrías agregar lógica adicional:
        #    - Invalidar todos los tokens activos del usuario
        #    - Enviar email de notificación de cambio de contraseña
        #    - Registrar evento de seguridad para auditoría

        return True

    def _validate_password_strength(self, password: str) -> bool:
        """
        Valida que la contraseña cumple los requisitos del dominio.

        Args:
            password: Contraseña a validar

        Returns:
            bool: True si cumple los requisitos
        """
        # Reglas de negocio: mínimo 8 caracteres
        return len(password) >= 8
