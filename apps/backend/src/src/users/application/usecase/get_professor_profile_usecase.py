from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.domain.professor import Professor
from src.users.infrastructure.professor_repository import ProfessorRepository
from src.users.api.v1.schemas.teacher import (
    TeacherProfileResponseSchema,
    TeacherProfileResponse,
)


class GetProfessorProfileUseCase:
    """
    Caso de uso para obtener el perfil del profesor autenticado.

    Responsabilidades:
    - Obtener el usuario actual del JWT token
    - Validar que tenga rol de professor
    - Buscar el registro de Professor asociado
    - Retornar datos combinados de User + Professor
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(self) -> TeacherProfileResponseSchema:
        """
        Obtiene el perfil del profesor autenticado.

        Returns:
            TeacherProfileResponseSchema: Perfil del profesor

        Raises:
            HTTPException 403: Si el usuario no tiene rol de professor
            HTTPException 404: Si no existe registro de Professor
        """
        # Validar que el usuario tenga rol de professor
        if (
            not self.current_user.role
            or self.current_user.role.role_name != "professor"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario no tiene permisos de profesor",
            )

        # Buscar registro de Professor
        professor_repo = ProfessorRepository(self.db)
        professor = await professor_repo.get_by_user_id(self.current_user.id)

        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existe perfil de profesor para este usuario",
            )

        # Construir respuesta combinada
        profile_data = TeacherProfileResponse(
            id=self.current_user.id,
            username=self.current_user.username,
            name=self.current_user.name,
            lastname=self.current_user.lastname,
            email=self.current_user.email,
            department=professor.department,
            contact_phone=professor.contact_phone,
            avatar_url=self.current_user.avatar_url,
            is_active=self.current_user.is_active,
            created_at=self.current_user.created_at,
            updated_at=self.current_user.updated_at,
        )

        return TeacherProfileResponseSchema(
            success=True,
            message="Perfil obtenido exitosamente",
            data=profile_data,
        )
