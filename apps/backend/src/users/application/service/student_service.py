# app/services/student_service.py
from src.users.infrastructure.student_repository import StudentRepository
from src.users.domain.student import Student
from src.shared.application.usecase.base_service import BaseService


class StudentService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de estudiantes.

    Proporciona una capa de abstracción sobre el repositorio de estudiantes,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: StudentRepository, model: type[Student]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de estudiantes
            model: Clase del modelo Student
        """
        super().__init__(repository, model)
