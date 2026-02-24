from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.level_repository import LevelRepository
from src.game.api.v1.schemas.level import (
    LevelUpdate,
    LevelUpdateResponse,
    LevelResponse,
)
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


router = APIRouter(prefix="/levels")


@router.put("/{level_id}", response_model=LevelUpdateResponse)
async def update_level(
    level_id: int,
    level: LevelUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza un nivel existente.

    - **level_id**: ID del nivel a actualizar
    - **level_number**: Nuevo número de nivel (opcional)
    - **title**: Nuevo título (opcional)
    - **description**: Nueva descripción (opcional)
    - **goal**: Nuevo objetivo (opcional)
    """
    level_repo = LevelRepository(db)

    # Verificar que el nivel existe
    existing_level = await level_repo.get_by_id(level_id)
    if not existing_level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nivel con ID {level_id} no encontrado",
        )

    try:
        # Filtrar solo campos que no son None
        update_data = {k: v for k, v in level.model_dump().items() if v is not None}

        if update_data:
            updated_level = await level_repo.update(level_id, update_data)
        else:
            updated_level = existing_level

        return LevelUpdateResponse(data=LevelResponse.model_validate(updated_level))

    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
