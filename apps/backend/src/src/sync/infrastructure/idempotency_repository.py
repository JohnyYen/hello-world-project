from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Text, Index
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.shared.infrastructure.base import Base


class IdempotencyKey(Base):
    """
    Modelo para almacenar claves de idempotencia del pipeline de estadísticas.

    Utilizado para prevenir el procesamiento duplicado de eventos basado en
    un hash único del evento.
    """

    __tablename__ = "idempotency_keys"

    event_hash = Column(String(64), nullable=False, unique=True, index=True)
    processed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    result = Column(Text, nullable=True)

    __table_args__ = (
        Index("ix_idempotency_event_hash_processed", "event_hash", "processed_at"),
    )


class IdempotencyRepository:
    """
    Repositorio para gestionar claves de idempotencia.

    Implementa verificación y almacenamiento de claves usando SELECT FOR UPDATE
    para manejar condiciones de carrera apropiadamente.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_key(self, event_hash: str) -> Optional[IdempotencyKey]:
        """
        Verifica si una clave de idempotencia ya existe.

        Usa SELECT FOR UPDATE para prevenir condiciones de carrera durante
        la verificación inicial (gap locking).

        Args:
            event_hash: Hash único del evento

        Returns:
            IdempotencyKey si existe, None en caso contrario
        """
        query = (
            select(IdempotencyKey)
            .where(IdempotencyKey.event_hash == event_hash)
            .with_for_update()
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def store_key(
        self, event_hash: str, result: Optional[str] = None
    ) -> IdempotencyKey:
        """
        Almacena una nueva clave de idempotencia.

        Args:
            event_hash: Hash único del evento
            result: Resultado opcional del procesamiento (serializado)

        Returns:
            IdempotencyKey: La entidad creada
        """
        idempotency_key = IdempotencyKey(
            event_hash=event_hash,
            processed_at=datetime.utcnow(),
            result=result,
        )
        self.db.add(idempotency_key)
        await self.db.commit()
        await self.db.refresh(idempotency_key)
        return idempotency_key

    async def is_processed(self, event_hash: str) -> bool:
        """
        Verifica rápidamente si un evento ya fue procesado.

        Args:
            event_hash: Hash único del evento

        Returns:
            bool: True si el evento ya fue procesado
        """
        query = select(IdempotencyKey.event_hash).where(
            IdempotencyKey.event_hash == event_hash
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_result(self, event_hash: str) -> Optional[str]:
        """
        Obtiene el resultado almacenado para un evento.

        Args:
            event_hash: Hash único del evento

        Returns:
            str or None: Resultado del procesamiento si existe
        """
        query = select(IdempotencyKey.result).where(
            IdempotencyKey.event_hash == event_hash
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
