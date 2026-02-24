from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.api.v1.schemas.game_instance import (
    SingleGameInstanceResponse,
    GameInstanceDetailResponse,
)


router = APIRouter(prefix="/game-instances")


@router.get("/{instance_id}", response_model=SingleGameInstanceResponse)
async def get_instance(
    instance_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtiene los detalles de una instancia de juego.

    - **instance_id**: ID de la instancia
    """
    instance_repo = GameInstanceRepository(db)

    # Obtener instancia con relaciones (eager loading)
    instance = await instance_repo.get_by_id_with_relations(instance_id)

    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instancia con ID {instance_id} no encontrada",
        )

    # Crear respuesta detallada con info del juego y estudiante
    instance_detail = GameInstanceDetailResponse.model_validate(instance)

    # Agregar info adicional si las relaciones están cargadas
    if instance.game:
        instance_detail.game_title = instance.game.title

    return SingleGameInstanceResponse(data=instance_detail)
