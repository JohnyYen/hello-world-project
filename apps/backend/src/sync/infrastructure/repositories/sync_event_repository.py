from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
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
        self, session_id: Union[int, str, UUID], include_deleted: bool = False
    ) -> List[SyncEvent]:
        """
        Obtiene eventos de sincronización por ID de sesión.

        Args:
            session_id: ID de la sesión de sincronización
            include_deleted: Si True, incluye eventos marcados como eliminados

        Returns:
            List[SyncEvent]: Lista de eventos de sincronización
        """
        filters = {"sync_session_id": session_id}
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

    async def get_by_client_event_id(
        self, client_event_id: UUID, include_deleted: bool = False
    ) -> Optional[SyncEvent]:
        """
        Obtiene un evento por su client_event_id.

        Args:
            client_event_id: UUID del evento generado por el cliente
            include_deleted: Si True, incluye eventos marcados como eliminados

        Returns:
            Optional[SyncEvent]: El evento o None si no existe
        """
        filters = {"client_event_id": client_event_id}
        return await self.get_one_by_filters(
            filters, include_deleted=include_deleted
        )

    async def upsert_by_client_event_id(
        self, event_data: dict
    ) -> Optional[SyncEvent]:
        """
        Inserta un evento o devuelve el existente si ya hay uno con el mismo client_event_id.

        Usa INSERT ... ON CONFLICT (client_event_id) WHERE client_event_id IS NOT NULL DO NOTHING
        con fallback SELECT.

        Args:
            event_data: Diccionario con los datos del evento (debe incluir client_event_id)

        Returns:
            Optional[SyncEvent]: El evento creado o el existente
        """
        client_event_id = event_data.get("client_event_id")
        if client_event_id is None:
            return await self.create(event_data)

        stmt = pg_insert(SyncEvent).values(**event_data)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["client_event_id"],
            index_where=SyncEvent.client_event_id.isnot(None),
        )
        result = await self.db.execute(stmt)
        await self.db.commit()

        if result.rowcount == 0:
            return await self.get_by_client_event_id(client_event_id)

        return await self.get_by_client_event_id(client_event_id)
