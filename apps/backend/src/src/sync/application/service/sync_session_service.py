from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from src.sync.infrastructure.repositories.sync_session_repository import (
    SyncSessionRepository,
)
from src.sync.domain.sync_session import SyncSession
from src.shared.domain.exceptions import NotFoundException


class SyncSessionService:
    """
    Service para manejar operaciones de sesiones de sincronización.
    """

    def __init__(self, db: AsyncSession):
        self.repository = SyncSessionRepository(db)

    async def create(
        self,
        instance_id: int,
    ) -> SyncSession:
        """
        Crea una nueva sesión de sincronización.

        Args:
            instance_id: ID de la instancia de juego

        Returns:
            SyncSession: La sesión creada
        """
        now = datetime.utcnow()
        session_data = {
            "instance_id": instance_id,
            "start_time": now,
            "end_time": None,
            "status": "active",
        }
        return await self.repository.create(session_data)

    async def end_session(
        self,
        session_id: int,
    ) -> SyncSession:
        """
        Finaliza una sesión de sincronización.

        Args:
            session_id: ID de la sesión a finalizar

        Returns:
            SyncSession: La sesión finalizada

        Raises:
            NotFoundException: Si la sesión no existe
        """
        session = await self.repository.get_by_id(session_id)
        if not session:
            raise NotFoundException(f"Sesión {session_id} no encontrada")

        now = datetime.utcnow()
        updated = await self.repository.update(
            session_id,
            {"end_time": now, "status": "completed"},
        )
        return updated

    async def get_session(
        self,
        session_id: int,
        include_deleted: bool = False,
    ) -> Optional[SyncSession]:
        """
        Obtiene una sesión por ID.

        Args:
            session_id: ID de la sesión
            include_deleted: Si True, incluye sesiones eliminadas

        Returns:
            Optional[SyncSession]: La sesión o None si no existe
        """
        return await self.repository.get_by_id(session_id, include_deleted)

    async def get_by_instance(
        self,
        instance_id: int,
        include_deleted: bool = False,
    ) -> List[SyncSession]:
        """
        Obtiene todas las sesiones de una instancia de juego.

        Args:
            instance_id: ID de la instancia de juego
            include_deleted: Si True, incluye sesiones eliminadas

        Returns:
            List[SyncSession]: Lista de sesiones
        """
        filters = {"instance_id": instance_id}
        return await self.repository.get_by_filters(
            filters,
            include_deleted=include_deleted,
            order_by="start_time",
            descending=True,
        )

    async def get_active_session_by_instance(
        self,
        instance_id: int,
    ) -> Optional[SyncSession]:
        """
        Obtiene la sesión activa de una instancia de juego.

        Args:
            instance_id: ID de la instancia de juego

        Returns:
            Optional[SyncSession]: La sesión activa o None
        """
        sessions = await self.repository.get_all(
            filters={"instance_id": instance_id, "status": "active"},
            limit=1,
        )
        return sessions[0] if sessions else None

    async def get_latest_session_by_instance(
        self,
        instance_id: int,
    ) -> Optional[SyncSession]:
        """
        Obtiene la última sesión de una instancia de juego.

        Args:
            instance_id: ID de la instancia de juego

        Returns:
            Optional[SyncSession]: La última sesión o None
        """
        sessions = await self.repository.get_all(
            filters={"instance_id": instance_id},
            order_by="start_time",
            descending=True,
            limit=1,
        )
        return sessions[0] if sessions else None

    async def delete(
        self,
        session_id: int,
    ) -> bool:
        """
        Elimina (soft delete) una sesión.

        Args:
            session_id: ID de la sesión a eliminar

        Returns:
            bool: True si se eliminó correctamente
        """
        return await self.repository.delete(session_id)
