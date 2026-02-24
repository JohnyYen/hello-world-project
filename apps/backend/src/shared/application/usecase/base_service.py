import logging
from abc import ABC
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import DeclarativeBase
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.shared.domain.exceptions import NotFoundException, DatabaseException

# Configurar logger
logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseService(ABC, Generic[ModelType]):
    """
    Servicio base que proporciona una capa de abstracción sobre el repositorio.

    Esta clase implementa operaciones CRUD genéricas delegando al repositorio,
    con validaciones comunes y manejo de excepciones.

    Los servicios específicos pueden heredar de esta clase y añadir lógica de negocio adicional.
    """

    def __init__(self, repository: BaseRepository[ModelType], model: Type[ModelType]):
        """
        Inicializa el servicio base con un repositorio y un modelo.

        Args:
            repository: Instancia del repositorio para operaciones de base de datos
            model: Clase del modelo SQLAlchemy
        """
        self.repository = repository
        self.model = model

    def _validate_id(self, id: int) -> None:
        """
        Valida que el ID sea un entero positivo.

        Args:
            id: ID a validar

        Raises:
            ValueError: Si el ID no es válido
        """
        if not isinstance(id, int) or id <= 0:
            raise ValueError(
                f"ID inválido: {id}. Debe ser un entero positivo mayor a 0."
            )

    def _validate_pagination(self, skip: int, limit: int) -> None:
        """
        Valida parámetros de paginación.

        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a devolver

        Raises:
            ValueError: Si los parámetros de paginación son inválidos
        """
        if not isinstance(skip, int) or skip < 0:
            raise ValueError(
                f"skip inválido: {skip}. Debe ser un entero mayor o igual a 0."
            )

        if not isinstance(limit, int) or limit <= 0:
            raise ValueError(f"limit inválido: {limit}. Debe ser un entero mayor a 0.")

        if limit > 100:
            raise ValueError(
                f"limit excede el máximo permitido: {limit}. El máximo es 100."
            )

    def _validate_data_not_empty(
        self, data: Dict[str, Any], operation_name: str
    ) -> None:
        """
        Valida que el diccionario de datos no esté vacío.

        Args:
            data: Diccionario de datos a validar
            operation_name: Nombre de la operación para el mensaje de error

        Raises:
            ValueError: Si los datos están vacíos
        """
        if not isinstance(data, dict) or not data:
            raise ValueError(
                f"No se proporcionaron datos para la operación '{operation_name}'."
            )

    async def get_by_id(
        self, id: int, include_deleted: bool = False
    ) -> Optional[ModelType]:
        """
        Obtiene una entidad por su ID.

        Args:
            id: ID de la entidad a buscar
            include_deleted: Si True, incluye entidades marcadas como eliminadas

        Returns:
            Optional[ModelType]: Instancia del modelo si se encuentra, None en caso contrario

        Raises:
            ValueError: Si el ID es inválido
        """
        self._validate_id(id)

        try:
            logger.debug(f"Buscando {self.model.__name__} con id={id}")
            result = await self.repository.get_by_id(id, include_deleted)

            if not result:
                logger.debug(f"{self.model.__name__} con id={id} no encontrado")

            return result

        except Exception as e:
            logger.error(f"Error al buscar {self.model.__name__} con id={id}: {str(e)}")
            raise DatabaseException(f"Error al buscar {self.model.__name__}: {str(e)}")

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

        Raises:
            ValueError: Si los parámetros de paginación son inválidos
        """
        self._validate_pagination(skip, limit)

        try:
            logger.debug(
                f"Listando {self.model.__name__} con skip={skip}, limit={limit}"
            )
            result = await self.repository.get_all(
                skip, limit, include_deleted, filters, order_by, descending
            )
            logger.debug(
                f"Se encontraron {len(result)} registros de {self.model.__name__}"
            )
            return result

        except Exception as e:
            logger.error(f"Error al listar {self.model.__name__}: {str(e)}")
            raise DatabaseException(f"Error al listar {self.model.__name__}: {str(e)}")

    async def create(self, data: Dict[str, Any]) -> ModelType:
        """
        Crea una nueva entidad en la base de datos.

        Args:
            data: Diccionario con los datos para la nueva entidad

        Returns:
            ModelType: Instancia del nuevo objeto creado

        Raises:
            ValueError: Si no se proporcionan datos
            DatabaseException: Si ocurre un error en la base de datos
        """
        self._validate_data_not_empty(data, "create")

        try:
            logger.debug(f"Creando {self.model.__name__} con datos: {data}")
            result = await self.repository.create(data)
            logger.info(f"{self.model.__name__} creado exitosamente con id={result.id}")
            return result

        except Exception as e:
            logger.error(f"Error al crear {self.model.__name__}: {str(e)}")
            raise DatabaseException(f"Error al crear {self.model.__name__}: {str(e)}")

    async def update(self, id: int, data: Dict[str, Any]) -> Optional[ModelType]:
        """
        Actualiza una entidad existente.

        Args:
            id: ID de la entidad a actualizar
            data: Diccionario con los campos a actualizar

        Returns:
            Optional[ModelType]: Instancia del objeto actualizado, None si no se encuentra

        Raises:
            ValueError: Si el ID es inválido o no hay datos para actualizar
            DatabaseException: Si ocurre un error en la base de datos
        """
        self._validate_id(id)
        self._validate_data_not_empty(data, "update")

        try:
            logger.debug(
                f"Actualizando {self.model.__name__} con id={id}, datos: {data}"
            )
            result = await self.repository.update(id, data)

            if result:
                logger.info(
                    f"{self.model.__name__} con id={id} actualizado exitosamente"
                )
            else:
                logger.warning(
                    f"No se pudo actualizar {self.model.__name__} con id={id} (no encontrado)"
                )

            return result

        except Exception as e:
            logger.error(
                f"Error al actualizar {self.model.__name__} con id={id}: {str(e)}"
            )
            raise DatabaseException(
                f"Error al actualizar {self.model.__name__}: {str(e)}"
            )

    async def soft_delete(self, id: int) -> bool:
        """
        Realiza un soft delete de la entidad (marca como eliminada con timestamp).

        Args:
            id: ID de la entidad a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no se encontró la entidad

        Raises:
            ValueError: Si el ID es inválido
            DatabaseException: Si ocurre un error en la base de datos
        """
        self._validate_id(id)

        try:
            logger.debug(f"Realizando soft delete de {self.model.__name__} con id={id}")
            result = await self.repository.delete(id)

            if result:
                logger.info(f"{self.model.__name__} con id={id} marcado como eliminado")
            else:
                logger.warning(
                    f"No se pudo eliminar {self.model.__name__} con id={id} (no encontrado)"
                )

            return bool(result)

        except Exception as e:
            logger.error(
                f"Error al realizar soft delete de {self.model.__name__} con id={id}: {str(e)}"
            )
            raise DatabaseException(
                f"Error al eliminar {self.model.__name__}: {str(e)}"
            )

    async def hard_delete(self, id: int) -> bool:
        """
        Elimina permanentemente la entidad de la base de datos.

        ⚠️ PRECAUCIÓN: Esta operación es irreversible.

        Args:
            id: ID de la entidad a eliminar permanentemente

        Returns:
            bool: True si se eliminó correctamente, False si no se encontró la entidad

        Raises:
            ValueError: Si el ID es inválido
            DatabaseException: Si ocurre un error en la base de datos
        """
        self._validate_id(id)

        try:
            logger.warning(
                f"Realizando hard delete IRREVERSIBLE de {self.model.__name__} con id={id}"
            )
            result = await self.repository.hard_delete(id)

            if result:
                logger.warning(
                    f"{self.model.__name__} con id={id} eliminado permanentemente"
                )
            else:
                logger.warning(
                    f"No se pudo eliminar permanentemente {self.model.__name__} con id={id} (no encontrado)"
                )

            return bool(result)

        except Exception as e:
            logger.error(
                f"Error al realizar hard delete de {self.model.__name__} con id={id}: {str(e)}"
            )
            raise DatabaseException(
                f"Error al eliminar permanentemente {self.model.__name__}: {str(e)}"
            )

    async def restore(self, id: int) -> Optional[ModelType]:
        """
        Restaura una entidad previamente marcada como eliminada.

        Args:
            id: ID de la entidad a restaurar

        Returns:
            Optional[ModelType]: Instancia del objeto restaurado, None si no se encontró o ya estaba activo

        Raises:
            ValueError: Si el ID es inválido
            DatabaseException: Si ocurre un error en la base de datos
        """
        self._validate_id(id)

        try:
            logger.debug(f"Restaurando {self.model.__name__} con id={id}")
            result = await self.repository.restore(id)

            if result:
                logger.info(
                    f"{self.model.__name__} con id={id} restaurado exitosamente"
                )
            else:
                logger.warning(
                    f"No se pudo restaurar {self.model.__name__} con id={id} (no encontrado o ya activo)"
                )

            return result

        except Exception as e:
            logger.error(
                f"Error al restaurar {self.model.__name__} con id={id}: {str(e)}"
            )
            raise DatabaseException(
                f"Error al restaurar {self.model.__name__}: {str(e)}"
            )

    async def get_one_by_filters(
        self, filters: Dict[str, Any], include_deleted: bool = False
    ) -> Optional[ModelType]:
        """
        Obtiene una entidad que coincida con los filtros especificados.

        Args:
            filters: Diccionario con condiciones de filtrado
            include_deleted: Si True, incluye entidades marcadas como eliminadas

        Returns:
            Optional[ModelType]: Instancia del modelo si se encuentra, None en caso contrario

        Raises:
            ValueError: Si no se proporcionan filtros
            DatabaseException: Si ocurre un error en la base de datos
        """
        if not isinstance(filters, dict) or not filters:
            raise ValueError(
                f"Se deben proporcionar filtros para buscar {self.model.__name__}"
            )

        try:
            logger.debug(f"Buscando {self.model.__name__} con filtros: {filters}")
            result = await self.repository.get_one_by_filters(filters, include_deleted)

            if not result:
                logger.debug(
                    f"{self.model.__name__} no encontrado con filtros: {filters}"
                )

            return result

        except Exception as e:
            logger.error(
                f"Error al buscar {self.model.__name__} con filtros {filters}: {str(e)}"
            )
            raise DatabaseException(f"Error al buscar {self.model.__name__}: {str(e)}")

    async def count(
        self, filters: Optional[Dict[str, Any]] = None, include_deleted: bool = False
    ) -> int:
        """
        Cuenta el número de entidades que coinciden con los filtros.

        Args:
            filters: Diccionario con condiciones de filtrado (opcional)
            include_deleted: Si True, incluye entidades marcadas como eliminadas

        Returns:
            int: Número de entidades que cumplen con los filtros

        Raises:
            DatabaseException: Si ocurre un error en la base de datos
        """
        try:
            logger.debug(f"Contando {self.model.__name__} con filtros: {filters}")
            result = await self.repository.count(filters, include_deleted)
            logger.debug(f"Se encontraron {result} registros de {self.model.__name__}")
            return result

        except Exception as e:
            logger.error(
                f"Error al contar {self.model.__name__} con filtros {filters}: {str(e)}"
            )
            raise DatabaseException(f"Error al contar {self.model.__name__}: {str(e)}")

    async def exists(self, id: int, include_deleted: bool = False) -> bool:
        """
        Verifica si existe una entidad con el ID especificado.

        Este método es más eficiente que get_by_id() cuando solo necesitas
        verificar la existencia sin recuperar los datos de la entidad.

        Args:
            id: ID de la entidad a verificar
            include_deleted: Si True, incluye entidades marcadas como eliminadas

        Returns:
            bool: True si la entidad existe, False en caso contrario

        Raises:
            ValueError: Si el ID es inválido
            DatabaseException: Si ocurre un error en la base de datos
        """
        self._validate_id(id)

        try:
            logger.debug(f"Verificando existencia de {self.model.__name__} con id={id}")
            result = await self.repository.exists(id, include_deleted)
            logger.debug(
                f"{self.model.__name__} con id={id} {'existe' if result else 'no existe'}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Error al verificar existencia de {self.model.__name__} con id={id}: {str(e)}"
            )
            raise DatabaseException(
                f"Error al verificar existencia de {self.model.__name__}: {str(e)}"
            )
