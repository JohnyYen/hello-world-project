"""
Shared dependencies (FastAPI dependency injection).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.shared.infrastructure.config import settings
from src.shared.infrastructure.session import get_db
from src.users.infrastructure.user_repository import UserRepository
from src.users.domain.user import User
from src.auth.api.v1.schemas.auth import TokenData


# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        raise credentials_exception

    user_repo = UserRepository(db)
    # Load role eagerly to avoid lazy loading issues
    from sqlalchemy import select

    query = (
        select(User)
        .where(User.username == token_data.username)
        .options(selectinload(User.role))
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
