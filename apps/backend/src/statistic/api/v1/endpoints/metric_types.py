from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.database import get_db
from src.statistic.application.service.metric_type_service import MetricTypeService
from src.statistic.api.v1.schemas.metric_type import (
    MetricTypeSchema,
    MetricTypeCreate,
    MetricTypeUpdate,
)
from src.shared.application.providers import get_metric_type_service

router = APIRouter(prefix="/metric-types", tags=["Metric Types"])


@router.get("", response_model=list[MetricTypeSchema])
async def list_metric_types(
    skip: int = 0,
    limit: int = 100,
    service: MetricTypeService = Depends(get_metric_type_service),
):
    """Lista todos los tipos de métricas disponibles."""
    metric_types = await service.get_all(skip=skip, limit=limit)
    return metric_types


@router.get("/{metric_type_id}", response_model=MetricTypeSchema)
async def get_metric_type(
    metric_type_id: int,
    service: MetricTypeService = Depends(get_metric_type_service),
):
    """Obtiene un tipo de métrica por su ID."""
    metric_type = await service.get_by_id(metric_type_id)
    if not metric_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de métrica con id={metric_type_id} no encontrado",
        )
    return metric_type


@router.post("", response_model=MetricTypeSchema, status_code=status.HTTP_201_CREATED)
async def create_metric_type(
    metric_type_in: MetricTypeCreate,
    service: MetricTypeService = Depends(get_metric_type_service),
):
    """Crea un nuevo tipo de métrica."""
    # Verificar si ya existe un tipo con el mismo código
    existing = await service.get_one_by_filters({"code": metric_type_in.code})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un tipo de métrica con el código '{metric_type_in.code}'",
        )

    metric_type = await service.create(metric_type_in.model_dump())
    return metric_type


@router.patch("/{metric_type_id}", response_model=MetricTypeSchema)
async def update_metric_type(
    metric_type_id: int,
    metric_type_in: MetricTypeUpdate,
    service: MetricTypeService = Depends(get_metric_type_service),
):
    """Actualiza un tipo de métrica existente."""
    # Verificar que existe
    existing = await service.get_by_id(metric_type_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de métrica con id={metric_type_id} no encontrado",
        )

    # Verificar código único si se está actualizando
    if metric_type_in.code and metric_type_in.code != existing.code:
        code_exists = await service.get_one_by_filters({"code": metric_type_in.code})
        if code_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un tipo de métrica con el código '{metric_type_in.code}'",
            )

    update_data = metric_type_in.model_dump(exclude_unset=True)
    updated = await service.update(metric_type_id, update_data)
    return updated


@router.delete("/{metric_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metric_type(
    metric_type_id: int,
    service: MetricTypeService = Depends(get_metric_type_service),
):
    """Elimina un tipo de métrica (soft delete)."""
    existing = await service.get_by_id(metric_type_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de métrica con id={metric_type_id} no encontrado",
        )

    await service.soft_delete(metric_type_id)
    return None
