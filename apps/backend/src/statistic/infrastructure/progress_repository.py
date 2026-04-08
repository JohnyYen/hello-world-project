from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.statistic.domain.progress import Progress


class ProgressRepository(BaseRepository[Progress]):
    """
    Repositorio específico para el modelo Progress.

    Hereda todas las operaciones CRUD del BaseRepository.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Progress)

    async def get_by_student_id(
        self,
        student_id: UUID,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Progress]:
        """
        Obtiene progresos por ID de estudiante.

        Args:
            student_id: UUID del estudiante
            include_deleted: Si True, incluye progresos marcados como eliminados
            skip: Número de registros a saltar
            limit: Máximo número de registros a devolver

        Returns:
            List[Progress]: Lista de progresos
        """
        filters = {"student_id": student_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_segment_level_id(
        self,
        segment_level_id: int,
        include_deleted: bool = False,
    ) -> List[Progress]:
        """
        Obtiene progresos por ID de segmento de nivel.

        Args:
            segment_level_id: ID del segmento de nivel
            include_deleted: Si True, incluye progresos marcados como eliminados

        Returns:
            List[Progress]: Lista de progresos
        """
        filters = {"segment_level_id": segment_level_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_by_student_and_segment(
        self,
        student_id: int,
        segment_level_id: int,
        include_deleted: bool = False,
    ) -> Optional[Progress]:
        """
        Obtiene progreso por ID de estudiante y segmento de nivel.

        Args:
            student_id: ID del estudiante
            segment_level_id: ID del segmento de nivel
            include_deleted: Si True, incluye progresos marcados como eliminados

        Returns:
            Progress: Instancia del modelo Progress si se encuentra, None en caso contrario
        """
        filters = {"student_id": student_id, "segment_level_id": segment_level_id}
        return await self.get_one_by_filters(filters, include_deleted=include_deleted)

    async def get_by_student_and_game(
        self,
        student_id: int,
        game_id: int,
        include_deleted: bool = False,
    ) -> List[Progress]:
        """
        Obtiene progresos por ID de estudiante y juego (a través de segmentos).

        Args:
            student_id: ID del estudiante
            game_id: ID del juego
            include_deleted: Si True, incluye progresos marcados como eliminados

        Returns:
            List[Progress]: Lista de progresos
        """
        # Get all progress for student, filter in service layer with game_id
        filters = {"student_id": student_id}
        return await self.get_by_filters(filters, include_deleted=include_deleted)

    async def get_aggregate_by_game(
        self,
        game_id: int,
        include_deleted: bool = False,
    ) -> dict:
        """
        Obtiene estadísticas agregadas de progreso por juego.

        Args:
            game_id: ID del juego
            include_deleted: Si True, incluye progresos eliminados

        Returns:
            dict: Diccionario con estadísticas agregadas
        """
        # TODO: Implement with proper SQL aggregation
        return {
            "total_attempts": 0,
            "total_errors": 0,
            "total_objectives_completed": 0,
            "average_efficiency_rating": 0,
        }

    async def count_students(self) -> int:
        """
        Cuenta el número total de estudiantes únicos con progreso.

        Returns:
            int: Número de estudiantes únicos
        """
        stmt = select(func.count(func.distinct(Progress.student_id)))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_active_students(self, days: int) -> int:
        """
        Cuenta estudiantes con actividad en los últimos N días.

        Args:
            days: Número de días hacia atrás

        Returns:
            int: Número de estudiantes activos
        """
        cutoff_date = date.today() - timedelta(days=days)
        stmt = select(func.count(func.distinct(Progress.student_id))).where(
            and_(Progress.created_at >= cutoff_date)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def aggregate_kpis(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Agrega KPIs totales del sistema.

        Args:
            start_date: Fecha de inicio opcional
            end_date: Fecha de fin opcional

        Returns:
            dict: Diccionario con métricas agregadas
        """
        conditions = []
        if start_date:
            conditions.append(Progress.created_at >= start_date)
        if end_date:
            conditions.append(Progress.created_at <= end_date)

        # Total de niveles completados (efficiency_rating > 0 indica completado)
        stmt_completed = select(func.count(Progress.id)).where(
            and_(*conditions, Progress.efficiency_rating > 0)
            if conditions
            else Progress.efficiency_rating > 0
        )
        result = await self.db.execute(stmt_completed)
        total_levels_completed = result.scalar() or 0

        # Tiempo total (suma de attempt_count como proxy de tiempo)
        stmt_time = select(func.sum(Progress.attempt_count)).where(
            and_(*conditions) if conditions else True
        )
        result = await self.db.execute(stmt_time)
        total_play_time_minutes = int(result.scalar() or 0)

        # Score promedio
        stmt_avg = select(func.avg(Progress.efficiency_rating)).where(
            and_(*conditions) if conditions else True
        )
        result = await self.db.execute(stmt_avg)
        average_score = float(result.scalar() or 0.0)

        return {
            "total_levels_completed": total_levels_completed,
            "total_play_time_minutes": total_play_time_minutes,
            "average_score": average_score,
        }

    async def aggregate_activity_by_date(
        self, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        """
        Agrega actividad por fecha.

        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin

        Returns:
            List[dict]: Lista de actividad por fecha
        """
        from sqlalchemy import cast, Date

        stmt = (
            select(
                cast(Progress.created_at, Date).label("date"),
                func.count(Progress.id).label("sessions"),
                func.count(func.distinct(Progress.student_id)).label("active_students"),
                func.sum(Progress.attempt_count).label("play_time_minutes"),
            )
            .where(
                and_(
                    cast(Progress.created_at, Date) >= start_date,
                    cast(Progress.created_at, Date) <= end_date,
                )
            )
            .group_by(cast(Progress.created_at, Date))
            .order_by(cast(Progress.created_at, Date))
        )

        result = await self.db.execute(stmt)
        rows = result.fetchall()

        return [
            {
                "date": row.date,
                "sessions": row.sessions,
                "active_students": row.active_students,
                "play_time_minutes": int(row.play_time_minutes or 0),
            }
            for row in rows
        ]

    async def aggregate_level_performance(self) -> List[Dict[str, Any]]:
        """
        Agrega rendimiento por nivel.

        Returns:
            List[dict]: Lista de rendimiento por nivel
        """
        from src.levels.domain.segment_level import SegmentLevel

        stmt = (
            select(
                SegmentLevel.name.label("level_name"),
                func.avg(Progress.efficiency_rating).label("average_score"),
                func.avg(Progress.attempt_count).label("average_attempts"),
                func.sum(Progress.objectives_completed).label("total_completed"),
                func.count(Progress.id).label("total_attempts"),
            )
            .join(SegmentLevel, Progress.segment_level_id == SegmentLevel.id)
            .group_by(SegmentLevel.id, SegmentLevel.name)
        )

        result = await self.db.execute(stmt)
        rows = result.fetchall()

        return [
            {
                "level_name": row.level_name,
                "completion_rate": row.total_completed / row.total_attempts
                if row.total_attempts > 0
                else 0.0,
                "average_attempts": float(row.average_attempts or 0),
                "average_time_minutes": float(row.average_attempts or 0)
                * 5,  # Estimación: 5 min por intento
            }
            for row in rows
        ]
