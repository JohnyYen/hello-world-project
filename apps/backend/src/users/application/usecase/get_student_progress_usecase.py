from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.infrastructure.user_repository import UserRepository
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.users.api.v1.schemas.student import StudentProgressResponse


class GetStudentProgressUseCase:
    """
    Caso de uso para obtener el progreso de un estudiante.

    Responsabilidades:
    - Validar que el usuario actual sea professor, admin, o el propio estudiante
    - Calcular progreso basado en game_instances
    - Retornar métricas de progreso
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(self, student_id: int) -> StudentProgressResponse:
        """
        Obtiene el progreso de un estudiante.

        Args:
            student_id: ID del estudiante

        Returns:
            StudentProgressResponse: Métricas de progreso

        Raises:
            HTTPException 403: Si no tiene permisos
            HTTPException 404: Si el estudiante no existe
        """
        # Verificar permisos: admin, professor, o el propio estudiante
        is_admin_or_professor = self.current_user.role.role_name in [
            "admin",
            "professor",
        ]
        is_own_profile = self.current_user.id == student_id

        if not is_admin_or_professor and not is_own_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para ver el progreso de este estudiante",
            )

        # Buscar usuario
        user_repo = UserRepository(self.db)
        student = await user_repo.get_by_id(student_id)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )

        # Verificar que sea estudiante
        if not student.role or student.role.role_name != "student":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario no es un estudiante",
            )

        # Obtener game_instances del estudiante
        game_instance_repo = GameInstanceRepository(self.db)
        instances = await game_instance_repo.get_by_student_id(student_id)

        # Calcular métricas de progreso
        completed_instances = [i for i in instances if i.status == "completed"]
        in_progress_instances = [i for i in instances if i.status == "in_progress"]

        total_levels = len(instances)
        completed_levels = len(completed_instances)
        completion_percentage = (
            (completed_levels / total_levels * 100) if total_levels > 0 else 0.0
        )

        # Obtener nivel actual (último no completado)
        current_level = None
        last_activity = None
        if in_progress_instances:
            # Ordenar por created_at descendente
            current_instance = sorted(
                in_progress_instances, key=lambda x: x.created_at, reverse=True
            )[0]
            current_level = (
                f"Nivel {current_instance.level_id}"
                if current_instance.level_id
                else "Nivel actual"
            )
            last_activity = (
                current_instance.created_at.isoformat()
                if current_instance.created_at
                else None
            )
        elif completed_instances:
            current_level = "Completado"
            last_activity = sorted(
                completed_instances, key=lambda x: x.created_at, reverse=True
            )[0].created_at.isoformat()

        # Calcular tiempo total (esto sería aproximado)
        total_time_spent = "0h 0m"

        progress_data = {
            "student_id": student_id,
            "completed_levels": completed_levels,
            "total_levels": total_levels,
            "completion_percentage": round(completion_percentage, 1),
            "current_level": current_level or "Sin iniciar",
            "last_activity": last_activity,
            "total_time_spent": total_time_spent,
        }

        return StudentProgressResponse(
            success=True,
            message="Progreso del estudiante obtenido exitosamente",
            data=progress_data,
        )
