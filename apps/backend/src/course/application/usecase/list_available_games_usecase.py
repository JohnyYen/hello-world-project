"""
UseCase: ListAvailableGamesUseCase

Lista juegos no eliminados que NO están asignados a ningún curso.
Anti-join: juegos cuya id NO aparece como course.game_id de ningún curso.
"""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.game.domain.game import Game
from src.course.domain.course import Course
from src.course.api.v1.schemas.course_management import (
    AvailableGameResponse,
    AvailableGamesResponse,
)


class ListAvailableGamesUseCase:
    """
    Caso de uso para listar juegos disponibles del catálogo global.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self) -> AvailableGamesResponse:
        """
        Retorna todos los juegos no eliminados que no están en ningún curso.

        Returns:
            AvailableGamesResponse con success, message y lista de juegos.
        """
        # Subquery: game_ids ya asignados a algún curso no eliminado
        assigned_ids_subq = (
            select(Course.game_id)
            .where(
                Course.deleted_at.is_(None),
                Course.game_id.isnot(None),
            )
        )

        # Main query: juegos que no están en la lista de asignados
        query = (
            select(Game)
            .where(
                Game.deleted_at.is_(None),
                ~Game.id.in_(assigned_ids_subq),
            )
            .order_by(Game.title)
        )

        result = await self.db.execute(query)
        games = list(result.scalars().all())

        return AvailableGamesResponse(
            success=True,
            message="Juegos disponibles",
            data=[AvailableGameResponse.model_validate(g) for g in games],
        )
