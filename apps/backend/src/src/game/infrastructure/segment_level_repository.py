from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.game.domain.segment_level import SegmentLevel


class SegmentLevelRepository(BaseRepository[SegmentLevel]):
    """
    Repositorio específico para el modelo SegmentLevel.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, SegmentLevel)

    async def get_by_level_id(
        self, level_id: int, include_deleted: bool = False
    ) -> List[SegmentLevel]:
        """
        Obtiene segmentos de nivel por ID de nivel.

        Args:
            level_id: ID del nivel
            include_deleted: Si True, incluye segmentos marcados como eliminados

        Returns:
            List[SegmentLevel]: Lista de segmentos de nivel
        """
        filters = {"level_id": level_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_segment_name(
        self, segment_name: str, include_deleted: bool = False
    ) -> Optional[SegmentLevel]:
        """
        Obtiene un segmento de nivel por nombre de segmento.

        Args:
            segment_name: Nombre del segmento
            include_deleted: Si True, incluye segmentos marcados como eliminados

        Returns:
            SegmentLevel: Instancia del modelo SegmentLevel si se encuentra, None en caso contrario
        """
        filters = {"segment_name": segment_name}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)
