# app/services/progress_service.py
import logging
from typing import Dict, Any, List
from uuid import UUID
from datetime import datetime

from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.domain.progress import Progress
from src.shared.application.usecase.base_service import BaseService
from src.shared.domain.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class BulkUpdateResult:
    """Resultado de una operación bulk_update."""
    
    def __init__(
        self,
        processed: int = 0,
        successful: int = 0,
        failed: int = 0,
        errors: List[Dict[str, Any]] = None,
    ):
        self.processed = processed
        self.successful = successful
        self.failed = failed
        self.errors = errors or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "processed": self.processed,
            "successful": self.successful,
            "failed": self.failed,
            "errors": self.errors,
        }


class ProgressService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de progresos.

    Proporciona una capa de abstracción sobre el repositorio de progresos,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: ProgressRepository, model: type[Progress]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de progresos
            model: Clase del modelo Progress
        """
        super().__init__(repository, model)

    async def bulk_create_or_update(
        self, records: List[Dict[str, Any]]
    ) -> BulkUpdateResult:
        """
        Crea o actualiza múltiples registros de progreso de forma atómica.

        Para cada record, verifica si ya existe un Progress con el mismo
        student_id + segment_level_id. Si existe, lo actualiza. Si no, crea uno nuevo.

        La operación es atómica: si falla, hace rollback de todo.

        Args:
            records: Lista de diccionarios con datos de progreso.
                     Cada record debe tener student_id (UUID) y segment_level_id (int).

        Returns:
            BulkUpdateResult con el resultado de la operación.

        Raises:
            DatabaseException: Si ocurre un error grave de base de datos.
        """
        if not records:
            return BulkUpdateResult()

        logger.info(
            f"Iniciando bulk_create_or_update con {len(records)} registros"
        )

        try:
            result = await self.repository.bulk_upsert_progress(records)
            return BulkUpdateResult(
                processed=result.get("inserted", 0) + result.get("updated", 0),
                successful=result.get("inserted", 0) + result.get("updated", 0),
                failed=result.get("errors", 0),
            )
        except Exception as e:
            logger.error(f"Error en bulk_create_or_update: {str(e)}")
            raise DatabaseException(
                f"Error al procesar bulk de progreso: {str(e)}"
            )

    async def get_existing_combinations(
        self, student_ids: List[UUID], segment_level_ids: List[int]
    ) -> List[UUID]:
        """
        Obtiene los IDs de progreso existentes para combinaciones específicas.

        Args:
            student_ids: Lista de UUIDs de estudiantes
            segment_level_ids: Lista de IDs de segmentos de nivel

        Returns:
            List[UUID]: IDs de progreso que ya existen
        """
        try:
            return await self.repository.get_existing_progress_ids(
                student_ids, segment_level_ids
            )
        except Exception as e:
            logger.error(f"Error al verificar combinaciones existentes: {str(e)}")
            raise DatabaseException(
                f"Error al verificar progreso existente: {str(e)}"
            )
