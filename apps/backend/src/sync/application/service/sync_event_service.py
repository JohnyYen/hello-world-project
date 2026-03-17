import asyncio
import logging
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.infrastructure.repositories.sync_event_repository import (
    SyncEventRepository,
)
from src.sync.infrastructure.repositories.sync_session_repository import (
    SyncSessionRepository,
)
from src.sync.domain.sync_event import SyncEvent
from src.sync.api.v1.schemas.sync_event import SyncEventCreate, SyncEventUpdate
from src.sync.application.service.sync_to_stats_pipeline_service import (
    SyncToStatsPipelineService,
)
from src.shared.domain.exceptions import NotFoundException
from src.shared.infrastructure.session import SessionLocal

logger = logging.getLogger(__name__)


class SyncEventService:
    """
    Service para manejar operaciones CRUD de eventos de sincronización.
    """

    def __init__(self, db: AsyncSession):
        self.repository = SyncEventRepository(db)
        self.session_repository = SyncSessionRepository(db)

    async def create(self, event_data: SyncEventCreate) -> SyncEvent:
        """
        Crea un nuevo evento de sincronización.

        Args:
            event_data: Datos del evento a crear

        Returns:
            SyncEvent: El evento creado

        Raises:
            NotFoundException: Si la sesión no existe
        """
        await self._validate_session_exists(event_data.sync_session_id)

        event_dict = event_data.model_dump()
        event_dict["timestamp"] = datetime.utcnow()
        event_dict["status"] = "pending"

        event = await self.repository.create(event_dict)

        asyncio.create_task(self._trigger_pipeline_with_retry(event.id))

        return event

    async def _trigger_pipeline_with_retry(self, event_id: int) -> None:
        """
        Trigger the stats pipeline with retry logic and exponential backoff.

        Args:
            event_id: ID of the event to process
        """
        max_attempts = 3
        base_delay = 1.0

        for attempt in range(1, max_attempts + 1):
            try:
                async with SessionLocal() as db:
                    pipeline = SyncToStatsPipelineService(db)
                    event = await self.repository.get_by_id(event_id)

                    if not event:
                        logger.warning(
                            f"Event {event_id} not found for pipeline processing"
                        )
                        return

                    await pipeline.process_event(event)
                    logger.info(f"Pipeline processing completed for event {event_id}")
                    return

            except Exception as e:
                logger.warning(
                    f"Pipeline attempt {attempt}/{max_attempts} failed for event {event_id}: {str(e)}"
                )

                if attempt < max_attempts:
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"Pipeline failed after {max_attempts} attempts for event {event_id}. "
                        f"Sending to dead letter."
                    )
                    await self._send_to_dead_letter(event_id, str(e))

    async def _send_to_dead_letter(self, event_id: int, error_message: str) -> None:
        """
        Send a failed event to the dead letter handler.

        Args:
            event_id: ID of the failed event
            error_message: Error message from the failure
        """
        try:
            async with SessionLocal() as db:
                from src.sync.application.handler.dead_letter_handler import (
                    DeadLetterHandler,
                )

                event = await self.repository.get_by_id(event_id)
                if event:
                    dead_letter_handler = DeadLetterHandler(db)
                    await dead_letter_handler.handle(event, error_message)
                    logger.info(f"Event {event_id} sent to dead letter")
        except Exception as e:
            logger.error(f"Failed to send event {event_id} to dead letter: {str(e)}")

    async def create_batch(self, events_data: List[SyncEventCreate]) -> List[SyncEvent]:
        """
        Crea múltiples eventos de sincronización en batch.

        Args:
            events_data: Lista de datos de eventos a crear

        Returns:
            List[SyncEvent]: Lista de eventos creados

        Raises:
            NotFoundException: Si alguna sesión no existe
        """
        if not events_data:
            return []

        session_ids = {event.sync_session_id for event in events_data}
        for session_id in session_ids:
            await self._validate_session_exists(session_id)

        now = datetime.utcnow()
        created_events = []

        for event_data in events_data:
            event_dict = event_data.model_dump()
            event_dict["timestamp"] = now
            event_dict["status"] = "pending"
            event = await self.repository.create(event_dict)
            created_events.append(event)

        return created_events

    async def get_by_id(
        self, event_id: int, include_deleted: bool = False
    ) -> Optional[SyncEvent]:
        """
        Obtiene un evento por su ID.

        Args:
            event_id: ID del evento
            include_deleted: Si True, incluye eventos eliminados

        Returns:
            Optional[SyncEvent]: El evento o None si no existe
        """
        return await self.repository.get_by_id(event_id, include_deleted)

    async def get_by_session(
        self,
        session_id: int,
        include_deleted: bool = False,
    ) -> List[SyncEvent]:
        """
        Obtiene todos los eventos de una sesión de sincronización.

        Args:
            session_id: ID de la sesión de sincronización
            include_deleted: Si True, incluye eventos eliminados

        Returns:
            List[SyncEvent]: Lista de eventos de la sesión
        """
        filters = {"sync_session_id": session_id}
        return await self.repository.get_by_filters(
            filters,
            include_deleted=include_deleted,
            order_by="timestamp",
            descending=True,
        )

    async def get_events_by_session(
        self,
        session_id: int,
        event_type: Optional[str] = None,
        include_deleted: bool = False,
    ) -> List[SyncEvent]:
        """
        Obtiene todos los eventos de una sesión con filtro opcional por tipo.

        Args:
            session_id: ID de la sesión de sincronización
            event_type: Filtrar por tipo de evento (opcional)
            include_deleted: Si True, incluye eventos eliminados

        Returns:
            List[SyncEvent]: Lista de eventos filtrados
        """
        filters = {"sync_session_id": session_id}
        if event_type:
            filters["event_type"] = event_type

        return await self.repository.get_by_filters(
            filters,
            include_deleted=include_deleted,
            order_by="timestamp",
            descending=True,
        )

    async def get_all(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> List[SyncEvent]:
        """
        Obtiene todos los eventos con paginación.

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye eventos eliminados

        Returns:
            List[SyncEvent]: Lista de eventos
        """
        return await self.repository.get_all(
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
            order_by="timestamp",
            descending=True,
        )

    async def update(
        self, event_id: int, event_data: SyncEventUpdate
    ) -> Optional[SyncEvent]:
        """
        Actualiza un evento existente.

        Args:
            event_id: ID del evento a actualizar
            event_data: Datos a actualizar

        Returns:
            Optional[SyncEvent]: El evento actualizado o None si no existe
        """
        event = await self.repository.get_by_id(event_id)
        if not event:
            return None

        update_dict = event_data.model_dump(exclude_unset=True)
        if not update_dict:
            return event

        return await self.repository.update(event_id, update_dict)

    async def delete(self, event_id: int) -> bool:
        """
        Elimina (soft delete) un evento.

        Args:
            event_id: ID del evento a eliminar

        Returns:
            bool: True si se eliminó correctamente
        """
        return await self.repository.delete(event_id)

    async def _validate_session_exists(self, session_id: int) -> None:
        """
        Valida que exista una sesión de sincronización.

        Args:
            session_id: ID de la sesión a validar

        Raises:
            NotFoundException: Si la sesión no existe
        """
        exists = await self.session_repository.exists(session_id)
        if not exists:
            raise NotFoundException(
                f"Sesión de sincronización {session_id} no encontrada"
            )
