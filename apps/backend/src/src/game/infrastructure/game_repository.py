from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.game.domain.game import Game


class GameRepository(BaseRepository[Game]):
    """
    Repositorio específico para el modelo Game.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Game)

    async def get_by_id_with_levels(
        self, id: int, include_deleted: bool = False
    ) -> Optional[Game]:
        """
        Obtiene un juego por ID con sus niveles cargados (eager loading).

        Args:
            id: ID del juego
            include_deleted: Si True, incluye juegos marcados como eliminados

        Returns:
            Game: Instancia del modelo Game con niveles cargados
        """
        query = select(Game).options(selectinload(Game.levels)).where(Game.id == id)
        if not include_deleted:
            query = query.where(Game.deleted_at.is_(None))

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_with_levels(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[Game]:
        """
        Obtiene todos los juegos con sus niveles cargados (eager loading).

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye juegos eliminados

        Returns:
            List[Game]: Lista de juegos con niveles cargados
        """
        query = select(Game).options(selectinload(Game.levels))
        if not include_deleted:
            query = query.where(Game.deleted_at.is_(None))

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_name(
        self, name: str, include_deleted: bool = False
    ) -> Optional[Game]:
        """
        Obtiene un juego por nombre.

        Args:
            name: Nombre del juego
            include_deleted: Si True, incluye juegos marcados como eliminados

        Returns:
            Game: Instancia del modelo Game si se encuentra, None en caso contrario
        """
        filters = {"name": name}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_slug(
        self, slug: str, include_deleted: bool = False
    ) -> Optional[Game]:
        """
        Obtiene un juego por slug.

        Args:
            slug: Slug del juego
            include_deleted: Si True, incluye juegos marcados como eliminados

        Returns:
            Game: Instancia del modelo Game si se encuentra, None en caso contrario
        """
        filters = {"slug": slug}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_owner_id(
        self, owner_id: int, include_deleted: bool = False
    ) -> List[Game]:
        """
        Obtiene juegos por ID del propietario.

        Args:
            owner_id: ID del propietario del juego
            include_deleted: Si True, incluye juegos marcados como eliminados

        Returns:
            List[Game]: Lista de juegos
        """
        filters = {"owner_id": owner_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)
