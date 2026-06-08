from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.game.domain.game_instance import GameInstance
from src.shared.domain.enums import GameStatus


class GameInstanceRepository(BaseRepository[GameInstance]):
    """
    Repositorio específico para el modelo GameInstance.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, GameInstance)

    async def get_by_id_with_relations(
        self, id: UUID, include_deleted: bool = False
    ) -> Optional[GameInstance]:
        """
        Obtiene una instancia de juego por ID con juego y estudiante cargados.

        Args:
            id: ID de la instancia (UUID)
            include_deleted: Si True, incluye instancias marcadas como eliminadas

        Returns:
            GameInstance: Instancia con game y student cargados
        """
        query = (
            select(GameInstance)
            .options(selectinload(GameInstance.game))
            .options(selectinload(GameInstance.student))
            .where(GameInstance.id == id)
        )
        if not include_deleted:
            query = query.where(GameInstance.deleted_at.is_(None))

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_with_relations(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[GameInstance]:
        """
        Obtiene todas las instancias con juego y estudiante cargados.

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye instancias eliminadas

        Returns:
            List[GameInstance]: Lista de instancias con relaciones cargadas
        """
        query = (
            select(GameInstance)
            .options(selectinload(GameInstance.game))
            .options(selectinload(GameInstance.student))
        )
        if not include_deleted:
            query = query.where(GameInstance.deleted_at.is_(None))

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_game_id(
        self, game_id: UUID, include_deleted: bool = False
    ) -> List[GameInstance]:
        """
        Obtiene instancias de juego por ID de juego.

        Args:
            game_id: ID del juego (UUID)
            include_deleted: Si True, incluye instancias marcadas como eliminadas

        Returns:
            List[GameInstance]: Lista de instancias de juego
        """
        filters = {"game_id": game_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_user_id(
        self, user_id: UUID, include_deleted: bool = False
    ) -> List[GameInstance]:
        """
        Obtiene instancias de juego por ID de usuario.

        Args:
            user_id: ID del usuario (UUID)
            include_deleted: Si True, incluye instancias marcadas como eliminadas

        Returns:
            List[GameInstance]: Lista de instancias de juego
        """
        filters = {"user_id": user_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_status(
        self, status: str, include_deleted: bool = False
    ) -> List[GameInstance]:
        """
        Obtiene instancias de juego por estado.

        Args:
            status: Estado de la instancia de juego
            include_deleted: Si True, incluye instancias marcadas como eliminadas

        Returns:
            List[GameInstance]: Lista de instancias de juego
        """
        filters = {"status": status}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_game_and_user(
        self, game_id: UUID, user_id: UUID, include_deleted: bool = False
    ) -> Optional[GameInstance]:
        """
        Obtiene una instancia de juego por ID de juego y ID de usuario.

        Args:
            game_id: ID del juego (UUID)
            user_id: ID del usuario (UUID)
            include_deleted: Si True, incluye instancias marcadas como eliminadas

        Returns:
            GameInstance: Instancia del modelo GameInstance si se encuentra, None en caso contrario
        """
        filters = {"game_id": game_id, "user_id": user_id}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_student_id(
        self, student_id: UUID, include_deleted: bool = False
    ) -> List[GameInstance]:
        """
        Obtiene instancias de juego por ID de estudiante.

        Args:
            student_id: ID del estudiante (referencia a students.id, UUID)
            include_deleted: Si True, incluye instancias marcadas como eliminadas

        Returns:
            List[GameInstance]: Lista de instancias de juego
        """
        filters = {"student_id": student_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def has_active_instances_for_course(
        self, course_id: UUID, include_deleted: bool = False
    ) -> bool:
        """
        Verifica si un curso tiene instancias de juego activas o en pausa.

        Args:
            course_id: UUID del curso
            include_deleted: Si True, incluye instancias eliminadas en el conteo

        Returns:
            bool: True si existe al menos una instancia con status ACTIVE o PAUSED.
        """
        query = (
            select(func.count())
            .where(
                GameInstance.course_id == course_id,
                GameInstance.status.in_([GameStatus.ACTIVE, GameStatus.PAUSED]),
            )
        )
        if not include_deleted:
            query = query.where(GameInstance.deleted_at.is_(None))

        result = await self.db.execute(query)
        return (result.scalar() or 0) > 0
