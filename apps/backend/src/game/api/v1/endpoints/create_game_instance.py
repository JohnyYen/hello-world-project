from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.infrastructure.game_repository import GameRepository
from src.game.api.v1.schemas.game_instance import (
    GameInstanceCreate,
    GameInstanceCreateResponse,
    GameInstanceResponse,
)
from src.shared.domain.exceptions import (
    DuplicateEntryException,
    ForeignKeyViolationException,
)
from src.users.infrastructure.student_repository import StudentRepository


router = APIRouter(prefix="/game-instances")


@router.post(
    "/{game_id}/instances",
    response_model=GameInstanceCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_game_instance(
    game_id: UUID,
    instance_data: GameInstanceCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Crea una nueva instancia de juego para un estudiante.

    - **game_id**: ID del juego
    - **student_id**: ID del estudiante (requerido)
    - **status**: Estado inicial (default: active)
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
    student_repo = StudentRepository(db)

    # Auto-mapping: si el student_id no existe en students,
    # buscar si es un user_id y mapearlo al student.id real
    student = await student_repo.get_by_id(instance_data.student_id)
    if not student:
        student = await student_repo.get_by_user_id(instance_data.student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Estudiante con ID {instance_data.student_id} no encontrado. "
                    "Verificá que el estudiante exista en la base de datos."
                ),
            )

    try:
        # Preparar datos de la instancia
        instance_dict = instance_data.model_dump(exclude={"game_id", "student_id"})
        instance_dict["game_id"] = game_id
        instance_dict["student_id"] = student.id  # student.id real (no user_id)
        instance_dict["started_at"] = datetime.now(timezone.utc)

        # Crear instancia
        new_instance = await instance_repo.create(instance_dict)

        return GameInstanceCreateResponse(
            data=GameInstanceResponse.model_validate(new_instance)
        )

    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ForeignKeyViolationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
