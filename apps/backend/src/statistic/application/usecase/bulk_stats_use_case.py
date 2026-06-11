from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Dict, Any, List

from src.shared.infrastructure.session import get_db
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.domain.progress import Progress
from src.statistic.application.service.progress_service import ProgressService, BulkUpdateResult


class BulkStatsUseCase:
    """
    Caso de uso para sincronización masiva de raw stats desde el juego.

    Orquesta la validación, consistencia y persistencia de raw stats
    usando ProgressService como capa de negocio intermedia.

    Flujo:
    1. Validar estructura de cada registro
    2. Verificar consistencia (student_id + segment_level_id)
    3. Delegar a ProgressService.bulk_create_or_update()
    4. Retornar resultado estructurado
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self._service: ProgressService | None = None

    @property
    def service(self) -> ProgressService:
        if self._service is None:
            repo = ProgressRepository(self.db)
            self._service = ProgressService(repo, Progress)
        return self._service

    async def execute(self, records: List[Dict]) -> Dict[str, Any]:
        """
        Ejecuta la sincronización masiva de raw stats.

        Args:
            records: Lista de raw stats records desde el juego.
                     Cada uno debe tener al menos student_id y segment_level_id.

        Returns:
            Dict con:
            - processed: total procesados
            - successful: exitosos
            - failed: fallidos
            - errors: lista de errores por registro
        """
        if not records:
            return {
                "processed": 0,
                "successful": 0,
                "failed": 0,
                "errors": [],
            }

        # 1. Validar estructura mínima de cada registro
        validated, validation_errors = self._validate_records(records)
        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": "Registros inválidos en el payload",
                    "errors": validation_errors,
                },
            )

        # 2. Ejecutar bulk upsert vía service
        try:
            result: BulkUpdateResult = await self.service.bulk_create_or_update(
                validated
            )
            return result.to_dict()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar raw stats: {str(e)}",
            )

    def _validate_records(
        self, records: List[Dict]
    ) -> tuple[List[Dict], List[Dict]]:
        """
        Valida estructura básica de cada registro.

        Returns:
            (validados, errores): tupla con listas de registros válidos y errores.
        """
        validated: List[Dict] = []
        errors: List[Dict] = []

        for i, record in enumerate(records):
            record_errors: List[str] = []

            # Validar student_id (debe ser UUID válido o convertible)
            raw_student_id = record.get("student_id") or record.get("actor_id")
            if not raw_student_id:
                record_errors.append("Falta student_id o actor_id")
            else:
                try:
                    UUID(str(raw_student_id))
                    record["student_id"] = str(raw_student_id)
                except ValueError:
                    record_errors.append(
                        f"student_id/actor_id no es UUID válido: {raw_student_id}"
                    )

            # Validar segment_level_id (debe ser int)
            raw_segment = record.get("segment_level_id") or record.get("segment_id")
            if raw_segment is None:
                record_errors.append("Falta segment_level_id o segment_id")
            else:
                record["segment_level_id"] = int(raw_segment)

            if record_errors:
                errors.append({"index": i, "errors": record_errors})
            else:
                # Normalizar campos
                validated.append(self._normalize_record(record))

        return validated, errors

    def _normalize_record(self, record: Dict) -> Dict:
        """
        Normaliza un registro: mapea alias a los campos que espera el service.
        """
        return {
            "student_id": record.get("student_id"),
            "segment_level_id": record.get("segment_level_id"),
            "attempt_count": record.get("attempt_count", 0),
            "error_count": record.get("error_count", 0),
            "hints_used_count": record.get("hints_used_count", 0),
            "errors_details": record.get("errors_details"),
            "objectives_completed": record.get("objectives_completed", 0),
            "efficiency_rating": record.get("efficiency_rating", 0),
        }