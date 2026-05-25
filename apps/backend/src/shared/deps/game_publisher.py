"""
Shared authorization dependencies for game-publisher.

These are FastAPI dependency functions used across course and game domains
to enforce role-based access without duplicating logic in each endpoint.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.deps import get_current_user
from src.shared.infrastructure.session import get_db
from src.users.infrastructure.user_repository import UserRepository
from src.course.infrastructure.course_repository import CourseRepository
from src.users.domain.user import User


# ---------------------------------------------------------------------------
# Admin guard
# ---------------------------------------------------------------------------


async def require_admin_role(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependencia que verifica que el usuario autenticado tenga rol de administrador.

    Returns:
        User: El usuario autenticado (confirmado admin).

    Raises:
        HTTPException 403: Si el usuario no tiene rol admin.
    """
    role_name = current_user.role.role_name.lower() if current_user.role else None
    if role_name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador para esta operación.",
        )
    return current_user


# ---------------------------------------------------------------------------
# Professor-ownership guard
# ---------------------------------------------------------------------------


async def require_professor_ownership(
    course_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependencia que verifica que el usuario autenticado sea profesor
    y esté asignado al curso indicado.

    Args:
        course_id: UUID del curso (inyectado desde el path param del endpoint).

    Returns:
        User: El usuario autenticado (confirmado profesor del curso).

    Raises:
        HTTPException 403: Si el usuario no es profesor del curso.
        HTTPException 404: Si el curso no existe.
    """
    # 1. El usuario debe tener rol profesor
    role_name = current_user.role.role_name.lower() if current_user.role else None
    if role_name != "professor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los profesores pueden acceder a esta operación.",
        )

    # 2. El profesor debe estar asignado al curso
    course_repo = CourseRepository(db)
    is_assigned = await course_repo.is_professor_assigned_to_course(
        current_user.id, course_id
    )
    if not is_assigned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No está asignado como profesor a este curso.",
        )

    return current_user
