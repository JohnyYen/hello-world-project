from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.users.domain.user import User
from src.users.domain.role import Role
from src.users.infrastructure.role_repository import RoleRepository
from src.users.api.v1.schemas.user import UserListResponse, UserResponse
from src.shared.domain.exceptions import NotFoundException


class ListUsersByRoleUseCase:
    """
    Caso de uso para listar usuarios filtrados por rol (student/professor).
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(
        self, role: str, skip: int = 0, limit: int = 100
    ) -> UserListResponse:
        role_repo = RoleRepository(self.db)
        role_obj = await role_repo.get_by_name(role)
        if not role_obj:
            raise NotFoundException(f"Rol '{role}' no encontrado")

        query = (
            select(User)
            .options(selectinload(User.role))
            .where(
                User.role_id == role_obj.id,
                User.deleted_at.is_(None),
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        users = list(result.scalars().all())

        return UserListResponse(
            message="Usuarios obtenidos con éxito",
            data=[UserResponse.model_validate(u) for u in users],
        )
