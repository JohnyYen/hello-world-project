from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.statistic.domain.metric_type import MetricType


class MetricTypeRepository(BaseRepository[MetricType]):
    """
    Repositorio específico para el modelo MetricType.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, MetricType)

    async def get_by_name(
        self, name: str, include_deleted: bool = False
    ) -> Optional[MetricType]:
        """
        Obtiene un tipo de métrica por nombre.

        Args:
            name: Nombre del tipo de métrica
            include_deleted: Si True, incluye tipos de métrica marcados como eliminados

        Returns:
            MetricType: Instancia del modelo MetricType si se encuentra, None en caso contrario
        """
        filters = {"name": name}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_code(
        self, code: str, include_deleted: bool = False
    ) -> Optional[MetricType]:
        """
        Obtiene un tipo de métrica por código.

        Args:
            code: Código del tipo de métrica
            include_deleted: Si True, incluye tipos de métrica marcados como eliminados

        Returns:
            MetricType: Instancia del modelo MetricType si se encuentra, None en caso contrario
        """
        filters = {"code": code}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)
