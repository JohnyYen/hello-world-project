from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.domain.professor import Professor
from src.users.infrastructure.professor_repository import ProfessorRepository
from src.users.infrastructure.user_repository import UserRepository
from src.users.api.v1.schemas.teacher import (
    TeacherProfileUpdate,
    TeacherProfileResponseSchema,
    TeacherProfileResponse,
)


class UpdateProfessorProfileUseCase:
    """
    Caso de uso para actualizar el perfil del profesor autenticado.

    Responsabilidades:
    - Obtener el usuario actual del JWT token
    - Validar que tenga rol de professor
    - Buscar el registro de Professor asociado
    - Actualizar campos de User y Professor
    - Retornar datos combinados actualizados
    """

    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        self.db = db
        self.current_user = current_user

    async def execute(
        self, profile_data: TeacherProfileUpdate
    ) -> TeacherProfileResponseSchema:
        """
        Actualiza el perfil del profesor autenticado.

        Args:
            profile_data: Datos a actualizar

        Returns:
            TeacherProfileResponseSchema: Perfil actualizado

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

        # Actualizar campos de User
        user_update_data = {}
        if profile_data.name is not None:
            user_update_data["name"] = profile_data.name
        if profile_data.lastname is not None:
            user_update_data["lastname"] = profile_data.lastname
        if profile_data.email is not None:
            user_update_data["email"] = profile_data.email
        if profile_data.avatar_url is not None:
            user_update_data["avatar_url"] = profile_data.avatar_url

        user_repo = UserRepository(self.db)
        if user_update_data:
            await user_repo.update(self.current_user.id, user_update_data)

        # Actualizar campos de Professor
        professor_update_data = {}
        if profile_data.department is not None:
            professor_update_data["department"] = profile_data.department
        if profile_data.contact_phone is not None:
            professor_update_data["contact_phone"] = profile_data.contact_phone

        if professor_update_data:
            await professor_repo.update(professor.id, professor_update_data)

        # Refrescar datos
        updated_user = await user_repo.get_by_id(self.current_user.id)
        updated_professor = await professor_repo.get_by_id(professor.id)

        # Construir respuesta
        profile_response = TeacherProfileResponse(
            id=updated_user.id,
            username=updated_user.username,
            name=updated_user.name,
            lastname=updated_user.lastname,
            email=updated_user.email,
            department=updated_professor.department,
            contact_phone=updated_professor.contact_phone,
            avatar_url=updated_user.avatar_url,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )

        return TeacherProfileResponseSchema(
            success=True,
            message="Perfil actualizado exitosamente",
            data=profile_response,
        )
