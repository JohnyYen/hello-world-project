# app/services/professor_service.py
from src.users.infrastructure.professor_repository import ProfessorRepository
from src.users.domain.professor import Professor
from src.shared.application.usecase.base_service import BaseService


class ProfessorService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de profesores.

    Proporciona una capa de abstracción sobre el repositorio de profesores,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: ProfessorRepository, model: type[Professor]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de profesores
            model: Clase del modelo Professor
        """
        super().__init__(repository, model)
