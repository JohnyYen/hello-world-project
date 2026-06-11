from fastapi import APIRouter, Depends, status
from typing import Dict, Any

from src.statistic.application.usecase.bulk_stats_use_case import (
    BulkStatsUseCase,
)
from src.statistic.api.v1.schemas.raw_stats import (
    RawStatsRecord,
    RawStatsBulkCreate,
)

router = APIRouter(tags=["Raw Stats"])

@router.post(
    "/sync/bulk-stats",
    response_model=Dict[str, Any],
    summary="Sincronizar raw stats al backend",
    description="Recibe raw stats desde el juego móvil y los persiste en la base de datos",
    status_code=status.HTTP_200_OK,
)
async def bulk_stats(
    request: RawStatsBulkCreate,
    use_case: BulkStatsUseCase = Depends(),
) -> Dict[str, Any]:
    """
    Sincroniza raw stats desde el juego móvil.
    
    Args:
        request: Lista de raw stats records para sincronizar
        
    Returns:
        Dict con resultados de la sincronización:
        - processed: Número de registros procesados
        - successful: Número de registros exitosos
        - failed: Número de registros fallidos
        - errors: Detalles de errores por registro
    """
    records_dict = [r.model_dump(exclude_none=True) for r in request.records]
    return await use_case.execute(records_dict)