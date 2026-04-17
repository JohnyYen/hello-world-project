# app/db/repositories/user_repository.py
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, update, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from src.users.domain.user import User
from src.users.api.v1.schemas.user import UserCreate, UserUpdate
from src.auth.infrastructure.security import get_password_hash, verify_password
from src.shared.domain.exceptions import (
    NotFoundException,
    DuplicateEntryException,
    InvalidCredentialsException,
)
from src.shared.infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repositorio para operaciones de base de datos relacionadas con usuarios.

    Hereda del BaseRepository y provee métodos CRUD con validaciones y manejo de errores específicos.
    También incluye métodos adicionales específicos para la autenticación de usuarios.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(
        self, email: str, include_deleted: bool = False
    ) -> Optional[User]:
        """Busca un usuario por email.

        Args:
            email: Email del usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados

        Returns:
            User: Instancia del modelo User si se encuentra, None en caso contrario
        """
        filters = {"email": email}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_username(
        self, username: str, include_deleted: bool = False
    ) -> Optional[User]:
        """Busca un usuario por nombre de usuario.

        Args:
            username: Nombre de usuario a buscar
            include_deleted: Si True, incluye usuarios marcados como eliminados

        Returns:
            User: Instancia del modelo User si se encuentra, None en caso contrario
        """
        filters = {"username": username}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def create(self, user_data: UserCreate) -> User:
        """Crea un nuevo usuario en la base de datos.

        Args:
            user_data: Datos validados para la creación del usuario

        Returns:
            User: Instancia del nuevo usuario creado

        Raises:
            DuplicateEntryException: Si el email o username ya existen
        """
        # Verifica unicidad de email y username antes de crear
        # user_data puede ser dict o objeto Pydantic
        email = (
            user_data.get("email") if isinstance(user_data, dict) else user_data.email
        )
        existing_email = await self.get_by_email(email)
        if existing_email:
            raise DuplicateEntryException("El email ya está registrado")

        username = (
            user_data.get("username")
            if isinstance(user_data, dict)
            else user_data.username
        )
        if username:
            existing_username = await self.get_by_username(username)
            if existing_username:
                raise DuplicateEntryException("El nombre de usuario ya está en uso")

        # Preparar datos para la creación, incluyendo la contraseña hash
        if isinstance(user_data, dict):
            user_dict = user_data.copy()
        else:
            user_dict = user_data.model_dump()

        # Solo hacer hash si viene password en texto plano
        if "password" in user_dict:
            user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        # Si viene hashed_password directamente, se usa sin modificar

        # Remover la contraseña original del diccionario si aún existe
        user_dict.pop("password", None)

        # Crear el usuario usando el método del BaseRepository
        return await super().create(user_dict)

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Actualiza un usuario existente.

        Solo actualiza los campos que no son None en user_data.
        Verifica unicidad de email y username si son proporcionados.

        Args:
            user_id: ID del usuario a actualizar
            user_data: Datos validados para la actualización

        Returns:
            User: Instancia del usuario actualizado, None si no se encuentra

        Raises:
            DuplicateEntryException: Si el nuevo email o username ya existen
        """
        # Obtener datos no nulos para actualizar
        if isinstance(user_data, dict):
            update_data = {k: v for k, v in user_data.items() if v is not None}
        else:
            update_data = user_data.model_dump(exclude_unset=True)

        if not update_data:
            return await self.get_by_id(user_id)

        # Verificar unicidad si se actualiza email o username
        if "email" in update_data:
            # Verificar si el email ya existe para otro usuario
            existing_user = await self.get_by_email(update_data["email"])
            if existing_user and existing_user.id != user_id:
                raise DuplicateEntryException("El nuevo email ya está registrado")

        if "username" in update_data and update_data["username"] is not None:
            # Verificar si el username ya existe para otro usuario
            existing_user = await self.get_by_username(update_data["username"])
            if existing_user and existing_user.id != user_id:
                raise DuplicateEntryException(
                    "El nuevo nombre de usuario ya está en uso"
                )

        # Actualizar contraseña si se proporciona
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )
        # Si se proporciona password pero no se actualiza, remover del update
        elif "password" in update_data:
            update_data.pop("password", None)

        # Usar el método del BaseRepository para actualizar
        return await super().update(user_id, update_data)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Autentica un usuario verificando email y contraseña.

        Args:
            email: Email del usuario
            password: Contraseña en texto plano

        Returns:
            User: Instancia del usuario si las credenciales son válidas, None en caso contrario

        Raises:
            InvalidCredentialsException: Si las credenciales son inválidas
        """
        user = await self.get_by_email(email, include_deleted=True)
        if not user or user.is_deleted:
            raise InvalidCredentialsException("Credenciales inválidas")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException("Credenciales inválidas")

        return user

    async def authenticate_by_username_or_email(
        self, username: str = None, email: str = None, password: str = None
    ) -> Optional[User]:
        """Autentica un usuario verificando username O email y contraseña.

        Args:
            username: Username del usuario (opcional)
            email: Email del usuario (opcional)
            password: Contraseña en texto plano

        Returns:
            User: Instancia del usuario si las credenciales son válidas, None en caso contrario

        Raises:
            InvalidCredentialsException: Si las credenciales son inválidas
        """
        user = None

        if email:
            user = await self.get_by_email(email, include_deleted=True)
        elif username:
            user = await self.get_by_username(username, include_deleted=True)

        if not user or user.is_deleted:
            raise InvalidCredentialsException("Credenciales inválidas")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException("Credenciales inválidas")

        return user

    async def get_all_with_role(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> List[User]:
        """Obtiene todos los usuarios con todas las relaciones cargadas de forma eager.

        Args:
            skip: Número de registros a saltar para paginación
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye usuarios eliminados (soft deleted)

        Returns:
            List[User]: Lista de usuarios con todas las relaciones ya cargadas
        """
        from src.users.domain.student import Student
        from src.users.domain.lms_credential import LMSCredential
        from src.users.domain.professor import Professor
        from src.users.domain.teacher_settings import TeacherSettings

        query = select(User).options(
            # Cargar role directamente
            selectinload(User.role),
            # Cargar lms_credential y sus relaciones (si las hay)
            selectinload(User.lms_credential),
            # Cargar student y sus relaciones anidadas
            selectinload(User.student).selectinload(Student.game_instances),
            selectinload(User.student).selectinload(Student.feedbacks),
            # Cargar professor
            selectinload(User.professor),
            # Cargar teacher_settings
            selectinload(User.teacher_settings),
        )

        # Filtrar por deleted_at solo si include_deleted es False
        if not include_deleted:
            query = query.where(User.deleted_at.is_(None))

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id_with_role(self, user_id: UUID) -> Optional[User]:
        """Obtiene un usuario por ID con todas las relaciones cargadas de forma eager.

        Args:
            user_id: UUID del usuario a buscar

        Returns:
            Optional[User]: Usuario con todas las relaciones ya cargadas, o None si no existe
        """
        from uuid import UUID as UUIDType
        from src.users.domain.student import Student
        from src.users.domain.lms_credential import LMSCredential
        from src.users.domain.professor import Professor
        from src.users.domain.teacher_settings import TeacherSettings
        from src.course.domain.course_enrollment import CourseEnrollment

        query = (
            select(User)
            .options(
                # Cargar role directamente
                selectinload(User.role),
                # Cargar lms_credential y sus relaciones (si las hay)
                selectinload(User.lms_credential),
                # Cargar student y sus relaciones anidadas
                selectinload(User.student).selectinload(Student.game_instances),
                selectinload(User.student).selectinload(Student.feedbacks),
                selectinload(User.student).selectinload(
                    Student.course_enrollments
                ).selectinload(CourseEnrollment.course),
                # Cargar professor
                selectinload(User.professor),
                # Cargar teacher_settings
                selectinload(User.teacher_settings),
            )
            .where(User.id == user_id, User.deleted_at.is_(None))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_students_with_pagination(
        self,
        skip: int = 0,
        limit: int = 100,
        search: str = None,
        course_id: UUID = None,
    ) -> List[User]:
        """Obtiene usuarios con rol de student con paginación y búsqueda.

        Args:
            skip: Número de registros a saltar
            limit: Máximo número de registros
            search: Búsqueda por nombre, email o username
            course_id: Filtrar por curso específico

        Returns:
            List[User]: Lista de usuarios con rol de student
        """
        from uuid import UUID as UUIDType
        from src.users.domain.student import Student
        from src.course.domain.course_enrollment import CourseEnrollment
        from src.users.infrastructure.role_repository import RoleRepository
        from sqlalchemy.orm import selectinload

        # Obtener el rol de student
        role_repo = RoleRepository(self.db)
        student_role = await role_repo.get_student_role()
        # Usar UUID directamente, no convertir a int
        student_role_id = student_role.id

        # Construir query base con eager loading
        query = (
            select(User)
            .options(
                selectinload(User.student).selectinload(
                    Student.course_enrollments
                ).selectinload(CourseEnrollment.course)
            )
            .where(
                User.role_id == student_role_id, User.deleted_at.is_(None)
            )
        )

        # Filtrar por curso si se proporciona
        if course_id:
            enrolled_student_ids = (
                select(Student.user_id)
                .join(CourseEnrollment, CourseEnrollment.student_id == Student.id)
                .where(CourseEnrollment.course_id == course_id)
            )
            query = query.where(User.id.in_(enrolled_student_ids))

        # Agregar búsqueda si se proporciona
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    User.name.ilike(search_pattern),
                    User.lastname.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.username.ilike(search_pattern),
                )
            )

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
