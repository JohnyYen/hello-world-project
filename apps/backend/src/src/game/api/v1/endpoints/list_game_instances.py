from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game_instance import (
    GameInstanceListResponse,
    GameInstanceResponse,
)


router = APIRouter(prefix="/game-instances")


@router.get("/{game_id}/instances", response_model=GameInstanceListResponse)
async def list_game_instances(
    game_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a devolver"),
    status_filter: str = Query(
        None, description="Filtrar por estado (active, completed, abandoned)"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista las instancias de un juego con paginación.

    - **game_id**: ID del juego
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a devolver
    - **status_filter**: Filtrar por estado (opcional)
    """
    # Verificar que el juego existe
    game_repo = GameRepository(db)
    game = await game_repo.get_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Juego con ID {game_id} no encontrado",
        )

    instance_repo = GameInstanceRepository(db)

    # Obtener instancias por juego
    instances = await instance_repo.get_by_game_id(game_id)

    # Filtrar por estado si se especifica
    if status_filter:
        instances = [i for i in instances if i.status == status_filter]

    # Aplicar paginación manual
    total = len(instances)
    paginated_instances = instances[skip : skip + limit]

    # Convertir a respuestas
    instance_responses = [
        GameInstanceResponse.model_validate(instance)
        for instance in paginated_instances
    ]

    return GameInstanceListResponse(
        data=instance_responses,
        total=total,
        skip=skip,
        limit=limit,
    )
