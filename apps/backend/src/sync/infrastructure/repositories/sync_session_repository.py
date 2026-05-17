from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.sync.domain.sync_session import SyncSession


class SyncSessionRepository(BaseRepository[SyncSession]):
    """
    Repositorio específico para el modelo SyncSession.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, SyncSession)

    async def get_by_user_id(
        self, user_id: int, include_deleted: bool = False
    ) -> List[SyncSession]:
        """
        Obtiene sesiones de sincronización por ID de usuario.

        Args:
            user_id: ID del usuario
            include_deleted: Si True, incluye sesiones marcadas como eliminadas

        Returns:
            List[SyncSession]: Lista de sesiones de sincronización
        """
        filters = {"user_id": user_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_status(
        self, status: str, include_deleted: bool = False
    ) -> List[SyncSession]:
        """
        Obtiene sesiones de sincronización por estado.

        Args:
            status: Estado de la sesión de sincronización
            include_deleted: Si True, incluye sesiones marcadas como eliminadas

        Returns:
            List[SyncSession]: Lista de sesiones de sincronización
        """
        filters = {"status": status}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_user_id_and_status(
        self, user_id: int, status: str, include_deleted: bool = False
    ) -> List[SyncSession]:
        """
        Obtiene sesiones de sincronización por ID de usuario y estado.

        Args:
            user_id: ID del usuario
            status: Estado de la sesión de sincronización
            include_deleted: Si True, incluye sesiones marcadas como eliminadas

        Returns:
            List[SyncSession]: Lista de sesiones de sincronización
        """
        filters = {"user_id": user_id, "status": status}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_latest_session_by_user(
        self, user_id: int, include_deleted: bool = False
    ) -> Optional[SyncSession]:
        """
        Obtiene la sesión de sincronización más reciente por ID de usuario.

        Args:
            user_id: ID del usuario
            include_deleted: Si True, incluye sesiones marcadas como eliminadas

        Returns:
            SyncSession: Instancia de la sesión más reciente, None si no se encuentra
        """
        filters = {"user_id": user_id}
        sessions = await self.get_by_filters(
            filters,
            include_deleted=include_deleted,
            order_by="created_at",
            descending=True,
        )
        return sessions[0] if sessions else None
