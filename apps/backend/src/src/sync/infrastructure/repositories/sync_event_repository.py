from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.sync.domain.sync_event import SyncEvent


class SyncEventRepository(BaseRepository[SyncEvent]):
    """
    Repositorio específico para el modelo SyncEvent.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, SyncEvent)

    async def get_by_session_id(
        self, session_id: int, include_deleted: bool = False
    ) -> List[SyncEvent]:
        """
        Obtiene eventos de sincronización por ID de sesión.

        Args:
            session_id: ID de la sesión de sincronización
            include_deleted: Si True, incluye eventos marcados como eliminados

        Returns:
            List[SyncEvent]: Lista de eventos de sincronización
        """
        filters = {"session_id": session_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_user_id(
        self, user_id: int, include_deleted: bool = False
    ) -> List[SyncEvent]:
        """
        Obtiene eventos de sincronización por ID de usuario.

        Args:
            user_id: ID del usuario
            include_deleted: Si True, incluye eventos marcados como eliminados

        Returns:
            List[SyncEvent]: Lista de eventos de sincronización
        """
        filters = {"user_id": user_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_event_type(
        self, event_type: str, include_deleted: bool = False
    ) -> List[SyncEvent]:
        """
        Obtiene eventos de sincronización por tipo de evento.

        Args:
            event_type: Tipo de evento de sincronización
            include_deleted: Si True, incluye eventos marcados como eliminados

        Returns:
            List[SyncEvent]: Lista de eventos de sincronización
        """
        filters = {"event_type": event_type}
        return await self.get_by_filters(filters, include_deleted=include_deleted)
