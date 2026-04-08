from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.api.v1.schemas.game_instance import (
    GameInstanceEnd,
    GameInstanceEndResponse,
    GameInstanceResponse,
)
from src.shared.domain.exceptions import NotFoundException


router = APIRouter(prefix="/game-instances")


@router.put("/{instance_id}/end", response_model=GameInstanceEndResponse)
async def end_instance(
    instance_id: int,
    end_data: GameInstanceEnd = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Finaliza una instancia de juego.

    - **instance_id**: ID de la instancia a finalizar
    - **status**: Estado final (default: completed)
    """
    instance_repo = GameInstanceRepository(db)

    # Verificar que la instancia existe
    existing_instance = await instance_repo.get_by_id(instance_id)
    if not existing_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instancia con ID {instance_id} no encontrada",
        )

    # Determinar estado final
    final_status = end_data.status if end_data else "completed"

    # Actualizar instancia
    update_data = {
        "status": final_status,
        "ended_at": datetime.utcnow(),
    }

    updated_instance = await instance_repo.update(instance_id, update_data)

    return GameInstanceEndResponse(
        data=GameInstanceResponse.model_validate(updated_instance)
    )
