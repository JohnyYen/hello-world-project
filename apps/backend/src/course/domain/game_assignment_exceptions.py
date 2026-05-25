"""
Excepciones de dominio para la asignación de juegos a cursos.

Estas excepciones representan errores de negocio específicos del flujo
de game publisher, sin depender de FastAPI directamente.
"""

from src.shared.domain.exceptions import AppException


class GameAlreadyAssignedException(AppException):
    """Se lanza cuando se intenta asignar un juego a un curso que ya tiene uno."""

    def __init__(self, course_name: str = "el curso"):
        super().__init__(
            status_code=409,
            detail=f"{course_name} ya tiene un juego asignado.",
        )


class GameHasActiveInstancesException(AppException):
    """Se lanza cuando se intenta cambiar el juego de un curso que tiene instancias activas."""

    def __init__(self, course_name: str = "el curso"):
        super().__init__(
            status_code=409,
            detail=(
                f"No se puede cambiar el juego de {course_name} mientras "
                "existan instancias de juego activas."
            ),
        )


class GameNotFoundException(AppException):
    """Se lanza cuando el juego buscado no existe."""

    def __init__(self, game_id: str):
        super().__init__(
            status_code=404,
            detail=f"Juego con ID {game_id} no encontrado.",
        )


class UnauthorizedCourseAccessException(AppException):
    """Se lanza cuando un profesor intenta modificar un curso que no le pertenece."""

    def __init__(self):
        super().__init__(
            status_code=403,
            detail="No tiene permisos para modificar este curso.",
        )
