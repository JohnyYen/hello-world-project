from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date, timedelta, datetime
from sqlalchemy import select, func, and_, text, cast, Date
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

    async def get_enriched_by_student_id(
        self,
        student_id: UUID,
        include_deleted: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Obtiene progresos enriquecidos con nombres de nivel y juego.

        Joins Progress -> SegmentLevel -> Level -> Game para obtener nombres reales.

        Args:
            student_id: UUID del estudiante
            include_deleted: Si True, incluye progresos marcados como eliminados

        Returns:
            List[Dict]: Lista de diccionarios con datos enriquecidos
        """
        from src.game.domain.segment_level import SegmentLevel
        from src.game.domain.level import Level
        from src.game.domain.game import Game

        stmt = (
            select(
                Progress,
                Level.title.label("level_title"),
                Level.level_number.label("level_number"),
                Game.title.label("game_title"),
            )
            .join(SegmentLevel, Progress.segment_level_id == SegmentLevel.id)
            .join(Level, SegmentLevel.level_number_id == Level.id)
            .join(Game, Level.game_id == Game.id)
            .where(Progress.student_id == student_id)
        )

        if not include_deleted:
            stmt = stmt.where(Progress.deleted_at.is_(None))

        stmt = stmt.order_by(Progress.created_at.asc())

        result = await self.db.execute(stmt)
        rows = result.fetchall()

        return [
            {
                "progress": row.Progress,
                "level_title": row.level_title,
                "level_number": row.level_number,
                "game_title": row.game_title,
            }
            for row in rows
        ]

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

    async def get_active_students_in_range(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> int:
        """
        Cuenta estudiantes únicos con actividad en un rango de fechas.

        Args:
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)

        Returns:
            int: Número de estudiantes activos en el rango
        """
        conditions = []
        if start_date:
            conditions.append(cast(Progress.created_at, Date) >= start_date)
        if end_date:
            conditions.append(cast(Progress.created_at, Date) <= end_date)

        stmt = select(func.count(func.distinct(Progress.student_id)))
        if conditions:
            stmt = stmt.where(and_(*conditions))

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
            conditions.append(cast(Progress.created_at, Date) >= start_date)
        if end_date:
            conditions.append(cast(Progress.created_at, Date) <= end_date)

        # Total de niveles completados (objectives_completed > 0 indica completado)
        stmt_completed = select(func.count(Progress.id)).where(
            and_(*conditions, Progress.objectives_completed > 0)
            if conditions
            else Progress.objectives_completed > 0
        )
        result = await self.db.execute(stmt_completed)
        total_levels_completed = result.scalar() or 0

        # Tiempo total (suma de attempt_count como proxy - sin multiplicadores arbitrarios)
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
        from src.game.domain.segment_level import SegmentLevel
        from src.game.domain.level import Level

        stmt = (
            select(
                Level.title.label("level_name"),
                func.avg(Progress.efficiency_rating).label("average_score"),
                func.avg(Progress.attempt_count).label("average_attempts"),
                func.sum(Progress.objectives_completed).label("total_completed"),
                func.count(Progress.id).label("total_attempts"),
            )
            .join(SegmentLevel, Progress.segment_level_id == SegmentLevel.id)
            .join(Level, SegmentLevel.level_number_id == Level.id)
            .group_by(Level.id, Level.title)
        )

        result = await self.db.execute(stmt)
        rows = result.fetchall()

        return [
            {
                "level_name": row.level_name,
                "completion_rate": min(row.total_completed / row.total_attempts, 1.0)
                if row.total_attempts > 0
                else 0.0,
                "average_attempts": float(row.average_attempts or 0),
                "average_time_minutes": float(row.average_attempts or 0),
            }
            for row in rows
        ]

    # ===== Course Reports Aggregation Methods =====

    async def aggregate_by_student_ids(
        self,
        student_ids: List[UUID],
    ) -> dict:
        """
        Agrega métricas de progreso para una lista de estudiantes usando SQL nativo.
        """
        if not student_ids:
            return {
                "average_progress": 0,
                "average_grade": 0,
                "completion_rate": 0,
                "students_completed": 0,
                "average_active_time": 0,
                "average_sessions": 0,
                "high_performers": 0,
                "medium_performers": 0,
                "low_performers": 0,
                "total_students": 0,
            }

        query = text("""
            SELECT
                student_id,
                AVG(efficiency_rating) as avg_efficiency,
                SUM(attempt_count) as total_attempts,
                COUNT(*) as record_count,
                MAX(CASE WHEN efficiency_rating > 0 OR objectives_completed > 0
                    THEN 1 ELSE 0 END) as has_progress
            FROM progresses
            WHERE student_id = ANY(:student_ids)
              AND deleted_at IS NULL
            GROUP BY student_id
        """)
        result = await self.db.execute(query, {"student_ids": student_ids})
        rows = result.fetchall()

        total_students = len(student_ids)
        if not rows:
            return {
                "average_progress": 0,
                "average_grade": 0,
                "completion_rate": 0,
                "students_completed": 0,
                "average_active_time": 0,
                "average_sessions": 0,
                "high_performers": 0,
                "medium_performers": 0,
                "low_performers": 0,
                "total_students": total_students,
            }

        all_efficiencies = [float(r.avg_efficiency) for r in rows]
        all_attempts = [int(r.total_attempts) for r in rows]
        students_completed = sum(1 for r in rows if r.has_progress)
        avg_progress = sum(all_efficiencies) / len(all_efficiencies)
        completion_rate = (students_completed / max(total_students, 1)) * 100
        avg_active_time = sum(all_attempts)
        avg_sessions = sum(all_attempts) / max(len(all_attempts), 1)

        return {
            "average_progress": round(avg_progress, 1),
            "average_grade": round(avg_progress, 1),
            "completion_rate": round(completion_rate, 1),
            "students_completed": students_completed,
            "average_active_time": round(avg_active_time, 1),
            "average_sessions": round(avg_sessions, 1),
            "high_performers": sum(1 for e in all_efficiencies if e >= 80),
            "medium_performers": sum(1 for e in all_efficiencies if 50 <= e < 80),
            "low_performers": sum(1 for e in all_efficiencies if e < 50),
            "total_students": total_students,
        }

    async def aggregate_by_course_ids(
        self,
        course_ids: List[UUID],
    ) -> Dict[UUID, dict]:
        """
        Computa métricas agregadas para múltiples cursos en una sola query SQL.
        """
        if not course_ids:
            return {}

        query = text("""
            SELECT
                ce.course_id,
                COUNT(DISTINCT ce.student_id) AS total_students,
                COALESCE(AVG(sa.avg_efficiency), 0) AS average_progress,
                COALESCE(COUNT(DISTINCT CASE WHEN sa.has_progress = 1 THEN ce.student_id END) * 100.0
                    / NULLIF(COUNT(DISTINCT ce.student_id), 0), 0) AS completion_rate,
                COUNT(DISTINCT CASE WHEN sa.has_progress = 1 THEN ce.student_id END) AS students_completed,
                COALESCE(SUM(sa.total_attempts), 0) AS total_attempts,
                COALESCE(AVG(sa.total_attempts), 0) AS avg_sessions,
                COUNT(DISTINCT CASE WHEN sa.avg_efficiency >= 80 THEN ce.student_id END) AS high_performers,
                COUNT(DISTINCT CASE WHEN sa.avg_efficiency BETWEEN 50 AND 79 THEN ce.student_id END) AS medium_performers,
                COUNT(DISTINCT CASE WHEN sa.avg_efficiency < 50 THEN ce.student_id END) AS low_performers
            FROM course_enrollments ce
            LEFT JOIN (
                SELECT student_id,
                    AVG(efficiency_rating) AS avg_efficiency,
                    SUM(attempt_count) AS total_attempts,
                    MAX(CASE WHEN efficiency_rating > 0 OR objectives_completed > 0
                        THEN 1 ELSE 0 END) AS has_progress
                FROM progresses
                WHERE deleted_at IS NULL
                GROUP BY student_id
            ) sa ON ce.student_id = sa.student_id
            WHERE ce.course_id = ANY(:course_ids)
              AND ce.deleted_at IS NULL
            GROUP BY ce.course_id
        """)
        result = await self.db.execute(query, {"course_ids": course_ids})
        rows = result.fetchall()

        metrics_map: Dict[UUID, dict] = {}
        for row in rows:
            metrics_map[row.course_id] = {
                "average_progress": round(float(row.average_progress), 1),
                "average_grade": round(float(row.average_progress), 1),  # Note: same source as progress since system only tracks efficiency_rating
                "completion_rate": round(float(row.completion_rate), 1),
                "students_completed": int(row.students_completed),
                "average_active_time": round(float(row.total_attempts), 1),
                "average_sessions": round(float(row.avg_sessions), 1),
                "high_performers": int(row.high_performers),
                "medium_performers": int(row.medium_performers),
                "low_performers": int(row.low_performers),
                "total_students": int(row.total_students),
            }

        for cid in course_ids:
            if cid not in metrics_map:
                metrics_map[cid] = {
                    "average_progress": 0,
                    "average_grade": 0,
                    "completion_rate": 0,
                    "students_completed": 0,
                    "average_active_time": 0,
                    "average_sessions": 0,
                    "high_performers": 0,
                    "medium_performers": 0,
                    "low_performers": 0,
                    "total_students": 0,
                }

        return metrics_map

    async def get_progress_over_time_by_student_ids(
        self,
        student_ids: List[UUID],
    ) -> List[dict]:
        """
        Obtiene progreso mensual agregado para estudiantes de un curso.
        """
        if not student_ids:
            return []

        query = text("""
            SELECT EXTRACT(MONTH FROM created_at) as month,
                   EXTRACT(YEAR FROM created_at) as year,
                   AVG(efficiency_rating) as avg_progress
            FROM progresses
            WHERE student_id = ANY(:student_ids)
              AND deleted_at IS NULL
            GROUP BY EXTRACT(MONTH FROM created_at), EXTRACT(YEAR FROM created_at)
            ORDER BY year, month
        """)
        result = await self.db.execute(query, {"student_ids": student_ids})
        rows = result.fetchall()

        month_names = [
            "Ene",
            "Feb",
            "Mar",
            "Abr",
            "May",
            "Jun",
            "Jul",
            "Ago",
            "Sep",
            "Oct",
            "Nov",
            "Dic",
        ]

        return [
            {
                "date": f"{month_names[int(r[0]) - 1]} {int(r[1])}",
                "average_progress": round(float(r[2]), 1),
                "average_grade": round(float(r[2]), 1),
            }
            for r in rows
        ]

    async def get_activity_summary_by_student_ids(
        self,
        student_ids: List[UUID],
        days: int = 30,
    ) -> List[dict]:
        """
        Obtiene resumen de actividad diario para los últimos N días.
        """
        if not student_ids:
            return []

        query = text("""
            SELECT DATE(created_at) as activity_date,
                   COUNT(DISTINCT student_id) as active_students,
                   SUM(attempt_count) as total_time_spent,
                   AVG(attempt_count) as avg_session_time
            FROM progresses
            WHERE student_id = ANY(:student_ids)
              AND created_at >= CURRENT_DATE - make_interval(days := :days)
              AND deleted_at IS NULL
            GROUP BY DATE(created_at)
            ORDER BY activity_date
        """)
        result = await self.db.execute(
            query, {"student_ids": student_ids, "days": days}
        )
        rows = result.fetchall()

        return [
            {
                "date": r[0].strftime("%d %b")
                if hasattr(r[0], "strftime")
                else str(r[0]),
                "activeStudents": int(r[1]),
                "totalTimeSpent": float(r[2]),
                "averageSessionTime": round(float(r[3]), 1),
            }
            for r in rows
        ]
