from pydantic import BaseModel, Field
from uuid import UUID
from typing import List


class StudentGameItem(BaseModel):
    """Juego disponible para un estudiante en el contexto del profesor logueado."""

    id: str = Field(..., description="UUID del juego")
    title: str = Field(..., description="Título del juego")
    description: str | None = Field(None, description="Descripción del juego")


class StudentGamesResponse(BaseModel):
    """Lista de juegos disponibles para un estudiante."""

    games: List[StudentGameItem] = Field(
        default_factory=list,
        description="Juegos a los que el estudiante tiene acceso a través de los cursos del profesor",
    )
