from typing import Optional
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from jwt import decode, encode, InvalidTokenError

from src.users.domain.user import User
from src.users.domain.role import Role
from src.auth.infrastructure.security import verify_password
from src.shared.infrastructure.session import engine
from src.shared.infrastructure.config import settings


class HWPAdminAuth(AuthenticationBackend):
    """
    AuthenticationBackend para SQLAdmin 0.20.0.
    Usa el mismo sistema JWT + roles que el resto de la API.
    """

    async def login(self, request: Request) -> bool:
        """Login desde el formulario de SQLAdmin."""
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            return False

        session_factory = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with session_factory() as session:
            user = await self._authenticate_user(username, password, session)
            if not user:
                return False

            # Generar JWT y guardar en session de Starlette
            token = encode(
                {"sub": user.username},
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM,
            )
            request.session["token"] = token
            return True

    async def logout(self, request: Request) -> bool:
        """Logout - limpia la session."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """
        Verifica que el request tenga un JWT válido y el usuario sea admin.
        Se llama en cada request a las rutas protegidas de SQLAdmin.
        """
        token = (
            request.session.get("token")
            or request.headers.get("authorization", "").replace("Bearer ", "")
        )

        if not token:
            return False

        try:
            payload = decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username = payload.get("sub")
            if not username:
                return False

            session_factory = sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )
            async with session_factory() as session:
                stmt = select(User).where(User.username == username)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()

                if not user or not user.is_active:
                    return False

                # Verificar rol admin
                role_stmt = select(Role).where(Role.id == user.role_id)
                role_result = await session.execute(role_stmt)
                role = role_result.scalar_one_or_none()

                return bool(role and role.role_name == "admin")

        except InvalidTokenError:
            return False
        except Exception:
            return False

    async def _authenticate_user(
        self, username: str, password: str, session: AsyncSession
    ) -> Optional[User]:
        """
        Autentica un usuario con username/password y verifica que sea admin.
        """
        stmt = select(User).where(
            (User.username == username) | (User.email == username)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        # Verificar rol admin
        role_stmt = select(Role).where(Role.id == user.role_id)
        role_result = await session.execute(role_stmt)
        role = role_result.scalar_one_or_none()

        if not role or role.role_name != "admin":
            return None

        return user


# Instancia global del backend de autenticación para SQLAdmin
admin_auth_backend = HWPAdminAuth(secret_key=settings.SECRET_KEY)
