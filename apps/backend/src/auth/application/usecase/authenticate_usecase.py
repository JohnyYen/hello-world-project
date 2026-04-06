from datetime import timedelta
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.shared.infrastructure.config import settings
from src.auth.infrastructure.security import create_access_token
from src.shared.infrastructure.session import get_db
from src.users.application.service.user_service import UserService
from src.users.infrastructure.user_repository import UserRepository
from src.users.domain.user import User
from src.shared.domain.exceptions import InvalidCredentialsException
from src.users.api.v1.schemas.user import UserLoginResponse, UserResponse
from sqlalchemy import select


class AuthenticateUseCase:
    """
    Caso de uso para autenticar un usuario.

    Responsabilidades:
    - Verificar las credenciales del usuario (username/email y contraseña)
    - Generar token JWT de acceso
    - Devolver respuesta de login con token y usuario

    Este UseCase NO maneja:
    - Creación de usuarios (ver RegisterUserUseCase)
    - Cambio de contraseña (ver ChangePasswordUseCase)
    - Refresco de tokens
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def execute(
        self, username: str = None, email: str = None, password: str = None
    ) -> UserLoginResponse:
        """
        Ejecuta el flujo de autenticación.

        Args:
            username: Username del usuario (opcional)
            email: Email del usuario (opcional)
            password: Contraseña en texto plano

        Returns:
            UserLoginResponse: Respuesta con token JWT y datos del usuario

        Raises:
            InvalidCredentialsException: Si las credenciales son inválidas
        """
        # 1. Autenticar usuario usando el repositorio (soporta username o email)
        user_repo = UserRepository(self.db)
        try:
            user = await user_repo.authenticate_by_username_or_email(
                username=username, email=email, password=password
            )
        except InvalidCredentialsException:
            raise
        except Exception:
            raise InvalidCredentialsException("Credenciales incorrectas")

        if user is None:
            raise InvalidCredentialsException("Credenciales incorrectas")

        # 2. Cargar relaciones eager para evitar lazy loading
        stmt = select(User).options(selectinload(User.role)).where(User.id == user.id)
        result = await self.db.execute(stmt)
        user_with_role = result.scalar_one()

        # 3. Generar token JWT
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        # 4. Devolver respuesta con token y usuario
        return UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            user=UserResponse.model_validate(user_with_role),
        )
