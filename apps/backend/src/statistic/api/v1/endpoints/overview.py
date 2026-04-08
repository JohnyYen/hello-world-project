from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from datetime import date as datetime_date

from src.statistic.application.usecase.get_overview_stats_usecase import (
    GetOverviewStatsUseCase,
)
from src.statistic.infrastructure.progress_repository import ProgressRepository
from src.statistic.api.v1.schemas.overview import (
    OverviewResponse,
    OverviewQueryParams,
)
from src.shared.infrastructure.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["Overview Stats"])

# Cache simple en memoria
_overview_cache: dict = {}
_CACHE_TTL_SECONDS = 60


@router.get(
    "/overview",
    response_model=OverviewResponse,
    summary="Obtener estadísticas globales del sistema",
    description="Retorna KPIs globales, evolución temporal, rendimiento por nivel y tendencias",
    status_code=status.HTTP_200_OK,
)
async def get_overview_stats(
    start_date: Optional[datetime_date] = Query(
        None, description="Fecha de inicio para filtrar"
    ),
    end_date: Optional[datetime_date] = Query(
        None, description="Fecha de fin para filtrar"
    ),
    period: Optional[str] = Query(None, description="Período: 7d, 30d, 3m"),
    db: AsyncSession = Depends(get_db),
) -> OverviewResponse:
    """
    Obtiene estadísticas globales del sistema educativo.

    Parámetros opcionales:
    - start_date: Filtrar desde fecha específica
    - end_date: Filtrar hasta fecha específica
    - period: Período predefinido (7d = 7 días, 30d = 30 días, 3m = 3 meses)

    Retorna:
    - kpis: Métricas clave globales
    - activity_over_time: Evolución temporal de actividad
    - level_performance: Rendimiento por nivel
    - trends: Tendencias vs período anterior
    """
    # Validar parámetros
    query_params = OverviewQueryParams(
        start_date=start_date, end_date=end_date, period=period
    )

    is_valid, error_msg = query_params.validate_params()
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

    # Verificar cache
    cache_key = f"{start_date}-{end_date}-{period}"
    if cache_key in _overview_cache:
        cached_data, cached_time = _overview_cache[cache_key]
        import time

        if time.time() - cached_time < _CACHE_TTL_SECONDS:
            return cached_data

    # Ejecutar caso de uso
    progress_repo = ProgressRepository(db)
    use_case = GetOverviewStatsUseCase(progress_repo)

    result = await use_case.execute(
        start_date=start_date, end_date=end_date, period=period
    )

    # Guardar en cache
    import time

    _overview_cache[cache_key] = (result, time.time())

    return result
