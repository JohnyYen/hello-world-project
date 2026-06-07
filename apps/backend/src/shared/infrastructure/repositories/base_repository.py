from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import and_, or_, select, update, delete, func, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase
from src.shared.domain.exceptions import (
    NotFoundException,
    DuplicateEntryException,
    ForeignKeyViolationException,
    DatabaseException,
)

# PostgreSQL SQLSTATE codes that surface as SQLAlchemy IntegrityError.
# Without dispatching on these, every FK / NOT NULL / CHECK failure gets
# misreported as a duplicate-entry 400 and, in unhandled flows, as 500.
_INTEGRITY_UNIQUE_VIOLATION = "23505"
_INTEGRITY_FOREIGN_KEY_VIOLATION = "23503"
_INTEGRITY_NOT_NULL_VIOLATION = "23502"
_INTEGRITY_CHECK_VIOLATION = "23514"


def _integrity_error_to_domain(integrity_error: IntegrityError, operation: str) -> Exception:
    """
    Convert a SQLAlchemy IntegrityError into the most specific domain exception
    we have, based on the underlying PostgreSQL SQLSTATE code. Falls back to
    DatabaseException for codes we don't yet model explicitly.
    """
    orig = getattr(integrity_error, "orig", None)
    pgcode = getattr(orig, "pgcode", None)

    if pgcode == _INTEGRITY_UNIQUE_VIOLATION:
        return DuplicateEntryException(
            f"Duplicate value violates a unique constraint during {operation}"
        )
    if pgcode == _INTEGRITY_FOREIGN_KEY_VIOLATION:
        return ForeignKeyViolationException(
            f"Referenced resource does not exist ({operation})"
        )
    if pgcode in (_INTEGRITY_NOT_NULL_VIOLATION, _INTEGRITY_CHECK_VIOLATION):
        return DatabaseException(
            f"Constraint violation ({pgcode}) during {operation}"
        )
    # Unknown integrity error: keep as a database error so the caller can map it.
    return DatabaseException(
        f"Unhandled integrity error during {operation}: {integrity_error}"
    )

# Define the generic type variable for the model
ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(ABC, Generic[ModelType]):
    """
    Repository abstracto base que proporciona operaciones CRUD genéricas para modelos SQLAlchemy.

    Este repositorio implementa operaciones comunes como:
    - Crear entidades
    - Leer entidades (con y sin filtros)
    - Actualizar entidades
    - Eliminar lógico (soft delete)
    """

    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        """
        Inicializa el repositorio con una sesión de base de datos y un modelo.

        Args:
            db: Sesión de base de datos SQLAlchemy
            model: Clase del modelo SQLAlchemy
        """
        self.db = db
        self.model = model

    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """
        Crea una nueva entidad en la base de datos.

        Args:
            obj_in: Diccionario con los datos para la nueva entidad

        Returns:
            ModelType: Instancia del nuevo objeto creado

        Raises:
            DuplicateEntryException: Si hay una violación de unicidad
            ForeignKeyViolationException: Si una FK apunta a un registro inexistente
            DatabaseException: Para cualquier otro fallo de integridad
        """
        try:
            db_obj = self.model(**obj_in)
            self.db.add(db_obj)
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await self.db.rollback()
            raise _integrity_error_to_domain(e, f"create {self.model.__name__}") from e

    async def get_by_id(
        self, id: Union[int, UUID, str], include_deleted: bool = False
    ) -> Optional[ModelType]:
        """
        Obtiene una entidad por su ID.

        Args:
            id: ID de la entidad a buscar
            include_deleted: Si True, incluye entidades marcadas como eliminadas

        Returns:
            ModelType: Instancia del modelo si se encuentra, None en caso contrario
        """
        query = select(self.model).where(self.model.id == id)
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        descending: bool = False,
    ) -> List[ModelType]:
        """
        Obtiene todas las entidades con opciones de paginación y filtrado.

        Args:
            skip: Número de registros a saltar (para paginación)
            limit: Máximo número de registros a devolver
            include_deleted: Si True, incluye entidades marcadas como eliminadas
            filters: Diccionario con condiciones de filtrado
            order_by: Nombre del campo por el cual ordenar
            descending: Si True, ordena en forma descendente

        Returns:
            List[ModelType]: Lista de instancias del modelo
        """
        query = select(self.model)

        # Aplicar condiciones de filtrado
        if filters:
            conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        # Si el valor es una lista, usar operador IN
                        conditions.append(getattr(self.model, field).in_(value))
                    else:
                        conditions.append(getattr(self.model, field) == value)

            if conditions:
                query = query.where(and_(*conditions))

        # Aplicar soft delete si no se incluyen eliminados
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))

        # Aplicar ordenamiento
        if order_by and hasattr(self.model, order_by):
            order_field = getattr(self.model, order_by)
            if descending:
                query = query.order_by(order_field.desc())
            else:
                query = query.order_by(order_field)

        # Aplicar paginación
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_filters(
        self,
        filters: Dict[str, Any],
        include_deleted: bool = False,
        order_by: Optional[str] = None,
        descending: bool = False,
    ) -> List[ModelType]:
        """
        Obtiene entidades que coinciden con los filtros especificados.

        Args:
            filters: Diccionario con condiciones de filtrado
            include_deleted: Si True, incluye entidades marcadas como eliminadas
            order_by: Nombre del campo por el cual ordenar
            descending: Si True, ordena en forma descendente

        Returns:
            List[ModelType]: Lista de instancias del modelo que cumplen con los filtros
        """
        query = select(self.model)

        # Aplicar condiciones de filtrado
        conditions = []
        for field, value in filters.items():
            if hasattr(self.model, field):
                if isinstance(value, list):
                    # Si el valor es una lista, usar operador IN
                    conditions.append(getattr(self.model, field).in_(value))
                else:
                    conditions.append(getattr(self.model, field) == value)

        if conditions:
            query = query.where(and_(*conditions))

        # Aplicar soft delete si no se incluyen eliminados
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))

        # Aplicar ordenamiento
        if order_by and hasattr(self.model, order_by):
            order_field = getattr(self.model, order_by)
            if descending:
                query = query.order_by(order_field.desc())
            else:
                query = query.order_by(order_field)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_one_by_filters(
        self, filters: Dict[str, Any], include_deleted: bool = False
    ) -> Optional[ModelType]:
        """
        Obtiene una entidad que coincida con los filtros especificados.

        Args:
            filters: Diccionario con condiciones de filtrado
            include_deleted: Si True, incluye entidades marcadas como eliminadas

        Returns:
            ModelType: Instancia del modelo si se encuentra, None en caso contrario
        """
        query = select(self.model)

        # Aplicar condiciones de filtrado
        conditions = []
        for field, value in filters.items():
            if hasattr(self.model, field):
                conditions.append(getattr(self.model, field) == value)

        if conditions:
            query = query.where(and_(*conditions))

        # Aplicar soft delete si no se incluyen eliminados
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, id: Union[int, UUID, str], obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """
        Actualiza una entidad existente.

        Args:
            id: ID de la entidad a actualizar
            obj_in: Diccionario con los campos a actualizar

        Returns:
            ModelType: Instancia del objeto actualizado, None si no se encuentra

        Raises:
            DuplicateEntryException: Si hay una violación de unicidad
        """
        try:
            # Filtrar para no actualizar campos con valores None si no es intencional
            update_data = {k: v for k, v in obj_in.items() if v is not None}

            if not update_data:
                # Si no hay datos para actualizar, devolver el objeto actual
                return await self.get_by_id(id)

            # Verificar si el registro existe antes de actualizar
            existing = await self.get_by_id(id)
            if not existing:
                return None

            # Ejecutar update sin RETURNING para evitar problemas con scalar_one_or_none
            result = await self.db.execute(
                update(self.model)
                .where(and_(self.model.id == id, self.model.deleted_at.is_(None)))
                .values(**update_data)
            )
            await self.db.commit()

            if result.rowcount == 0:
                return None

            # Refrescar el objeto existente en sesión
            await self.db.refresh(existing)
            return existing

        except IntegrityError as e:
            await self.db.rollback()
            raise _integrity_error_to_domain(e, f"update {self.model.__name__}") from e

    async def delete(self, id: Union[int, UUID, str]) -> bool:
        """
        Realiza un soft delete de la entidad (marca como eliminada con timestamp).

        Args:
            id: ID de la entidad a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no se encontró la entidad
        """
        result = await self.db.execute(
            update(self.model)
            .where(and_(self.model.id == id, self.model.deleted_at.is_(None)))
            .values(deleted_at=datetime.now(timezone.utc), is_deleted=True)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def hard_delete(self, id: Union[int, UUID, str]) -> bool:
        """
        Elimina permanentemente la entidad de la base de datos.

        Args:
            id: ID de la entidad a eliminar permanentemente

        Returns:
            bool: True si se eliminó correctamente, False si no se encontró la entidad
        """
        result = await self.db.execute(delete(self.model).where(self.model.id == id))
        await self.db.commit()
        return result.rowcount > 0

    async def restore(self, id: Union[int, UUID, str]) -> Optional[ModelType]:
        """
        Restaura una entidad previamente marcada como eliminada.

        Args:
            id: ID de la entidad a restaurar

        Returns:
            ModelType: Instancia del objeto restaurado, None si no se encontró o ya estaba activo
        """
        result = await self.db.execute(
            update(self.model)
            .where(
                and_(self.model.id == id, self.model.deleted_at.is_(None) == False)
            )  # not is_(None)
            .values(deleted_at=None, is_deleted=False)
            .returning(self.model)
        )
        updated_obj = result.scalar_one_or_none()
        if updated_obj:
            await self.db.commit()
            await self.db.refresh(updated_obj)
        else:
            await self.db.commit()
        return updated_obj

    async def count(
        self, filters: Optional[Dict[str, Any]] = None, include_deleted: bool = False
    ) -> int:
        """
        Cuenta el número de entidades que coinciden con los filtros.

        Args:
            filters: Diccionario con condiciones de filtrado
            include_deleted: Si True, incluye entidades marcadas como eliminadas

        Returns:
            int: Número de entidades que cumplen con los filtros
        """
        query = select(func.count(self.model.id))

        # Aplicar condiciones de filtrado
        if filters:
            conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        # Si el valor es una lista, usar operador IN
                        conditions.append(getattr(self.model, field).in_(value))
                    else:
                        conditions.append(getattr(self.model, field) == value)

            if conditions:
                query = query.where(and_(*conditions))

        # Aplicar soft delete si no se incluyen eliminados
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))

        result = await self.db.execute(query)
        return result.scalar()

    async def exists(self, id: Union[int, UUID, str], include_deleted: bool = False) -> bool:
        """
        Verifica si existe una entidad con el ID especificado.

        Args:
            id: ID de la entidad a verificar
            include_deleted: Si True, incluye entidades marcadas como eliminadas

        Returns:
            bool: True si la entidad existe, False en caso contrario
        """
        query = select(exists(self.model)).where(self.model.id == id)

        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))

        result = await self.db.execute(query)
        return result.scalar()
