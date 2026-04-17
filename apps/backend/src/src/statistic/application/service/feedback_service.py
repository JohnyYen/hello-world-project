# app/services/feedback_service.py
from src.statistic.infrastructure.feedback_repository import FeedbackRepository
from src.statistic.domain.feedback import Feedback
from src.shared.application.usecase.base_service import BaseService


class FeedbackService(BaseService):
    """
    Servicio para gestionar la lógica de negocio de feedback.

    Proporciona una capa de abstracción sobre el repositorio de feedback,
    manejando la lógica de negocio antes de interactuar con la base de datos.
    """

    def __init__(self, repository: FeedbackRepository, model: type[Feedback]):
        """
        Inicializa el servicio con un repositorio y modelo.

        Args:
            repository: Instancia del repositorio de feedback
            model: Clase del modelo Feedback
        """
        super().__init__(repository, model)

    async def get_by_student_id(
        self,
        student_id: int,
        include_deleted: bool = False,
    ):
        """
        Obtiene feedback por ID de estudiante.

        Args:
            student_id: ID del estudiante
            include_deleted: Si True, incluye feedback eliminados

        Returns:
            Lista de Feedback
        """
        return await self.repository.get_by_student_id(
            student_id=student_id, include_deleted=include_deleted
        )
