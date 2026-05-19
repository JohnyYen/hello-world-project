from typing import Optional
from sqladmin import Admin, ModelView
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.users.domain.user import User
from src.users.domain.role import Role
from src.auth.infrastructure.security import verify_password
from src.shared.infrastructure.session import engine


class AdminAuth:
    """
    Autenticación personalizada para SQLAdmin.
    Utiliza la lógica existente de JWT/password del proyecto.
    """

    def __init__(self):
        self._session_factory = None

    async def get_session(self) -> AsyncSession:
        """Crea una sesión de base de datos para verificar credenciales."""
        from sqlalchemy.orm import sessionmaker
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )
        async with self._session_factory() as session:
            yield session

    async def authenticate(self, username: str, password: str, session: AsyncSession) -> Optional[User]:
        """
        Autentica un usuario usando username/email y password.
        Reutiliza la lógica de authenticate_usecase.
        """
        # Buscar por username o email
        stmt = select(User).where(
            (User.username == username) | (User.email == username)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Verificar contraseña
        if not verify_password(password, user.hashed_password):
            return None

        # Verificar que el usuario esté activo
        if not user.is_active:
            return None

        return user

    async def verify_token(self, request: Request) -> Optional[User]:
        """
        Verifica el token JWT del request.
        Retorna el usuario si el token es válido.
        """
        from sqlalchemy.orm import sessionmaker

        token = request.session.get("token") or request.headers.get("authorization", "").replace("Bearer ", "")
        
        if not token:
            return None

        try:
            from jwt import decode, InvalidTokenError
            from src.shared.infrastructure.config import settings

            payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")

            if not username:
                return None

            session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
            async with session_factory() as session:
                stmt = select(User).where(User.username == username)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()

                return user if user and user.is_active else None

        except InvalidTokenError:
            return None
        except Exception:
            return None


async def get_session():
    """Dependencia para obtener sesión de DB en autenticación."""
    from sqlalchemy.orm import sessionmaker
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session


async def verify_admin_role(user: User, session: AsyncSession) -> bool:
    """
    Verifica si el usuario tiene rol de admin.
    Requiere sesión async para cargar la relación con role.
    """
    from sqlalchemy import select
    from src.users.domain.role import Role

    stmt = select(Role).where(Role.id == user.role_id)
    result = await session.execute(stmt)
    role = result.scalar_one_or_none()

    if not role:
        return False

    return role.role_name == "admin"


# Instancia global del autenticador
admin_auth = AdminAuth()


class AdminUser:
    """Wrapper para usar User en SQLAdmin."""
    def __init__(self, user: User):
        self.user = user
        self.id = user.id
        self.username = user.username
        self.email = user.email
        self.is_active = user.is_active

    @property
    def is_authenticated(self) -> bool:
        return self.user.is_active


class AdminAuthentication:
    """
    Backend de autenticación para SQLAdmin.
    Integra la verificación JWT existente con SQLAdmin.
    """

    async def authenticate(self, request: Request) -> AdminUser | None:
        """
        Autentica el request usando JWT del header o session.
        Retorna AdminUser si es válido, None si no.
        """
        user = await admin_auth.verify_token(request)
        if user and user.is_active:
            return AdminUser(user)
        return None

    async def identity(self, request: Request) -> dict | None:
        """Retorna la identidad del usuario para SQLAdmin."""
        user = await admin_auth.verify_token(request)
        if user:
            return {"id": str(user.id), "username": user.username}
        return None


admin_auth_backend = AdminAuthentication()


async def load_current_user(request: Request) -> AdminUser | None:
    """
    Dependencia que carga el usuario actual desde JWT.
    SQLAdmin la usa para verificar el usuario en cada request.
    """
    user = await admin_auth.verify_token(request)
    if user and user.is_active:
        return AdminUser(user)
    return None


async def load_user_with_session(request: Request) -> tuple[User, AsyncSession] | None:
    """
    Carga el usuario junto con una sesión de DB.
    Necesario para verificar el rol admin en los ModelViews.
    """
    from sqlalchemy.orm import sessionmaker

    user = await admin_auth.verify_token(request)
    if not user or not user.is_active:
        return None

    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        return (user, session)