from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
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
        student_id: int,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Progress]:
        """
        Obtiene progresos por ID de estudiante.

        Args:
            student_id: ID del estudiante
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

    async def aggregate_by_student_ids(
        self,
        student_ids: List[int],
    ) -> dict:
        """
        Agrega métricas de progreso para una lista de estudiantes.

        Returns:
            Dict con: average_progress, average_grade, completion_rate,
                     students_completed, average_active_time, average_sessions,
                     high_performers, medium_performers, low_performers
        """
        if not student_ids:
            return {
                "average_progress": 0, "average_grade": 0, "completion_rate": 0,
                "students_completed": 0, "average_active_time": 0,
                "average_sessions": 0, "high_performers": 0,
                "medium_performers": 0, "low_performers": 0, "total_students": 0,
            }

        # Get all progress records for these students
        query = select(Progress).where(Progress.student_id.in_(student_ids))
        result = await self.db.execute(query)
        progresses = result.scalars().all()

        if not progresses:
            return {
                "average_progress": 0, "average_grade": 0, "completion_rate": 0,
                "students_completed": 0, "average_active_time": 0,
                "average_sessions": 0, "high_performers": 0,
                "medium_performers": 0, "low_performers": 0, "total_students": len(student_ids),
            }

        # Aggregate per student
        student_stats = {}
        for p in progresses:
            if p.student_id not in student_stats:
                student_stats[p.student_id] = {
                    "efficiency_sum": 0, "attempts_sum": 0, "count": 0, "has_progress": False
                }
            student_stats[p.student_id]["efficiency_sum"] += p.efficiency_rating
            student_stats[p.student_id]["attempts_sum"] += p.attempt_count
            student_stats[p.student_id]["count"] += 1
            if p.efficiency_rating > 0 or p.objectives_completed > 0:
                student_stats[p.student_id]["has_progress"] = True

        total_students = len(student_ids)
        students_with_data = len(student_stats)
        students_completed = sum(1 for s in student_stats.values() if s["has_progress"])

        all_efficiencies = [s["efficiency_sum"] / max(s["count"], 1) for s in student_stats.values()]
        all_attempts = [s["attempts_sum"] for s in student_stats.values()]

        avg_progress = sum(all_efficiencies) / max(len(all_efficiencies), 1)
        avg_grade = avg_progress  # Same source in current schema
        completion_rate = (students_completed / max(total_students, 1)) * 100
        avg_active_time = sum(all_attempts) * 5  # 5 min per attempt convention
        avg_sessions = sum(all_attempts) / max(len(all_attempts), 1)

        # Performance distribution
        high = sum(1 for e in all_efficiencies if e >= 80)
        medium = sum(1 for e in all_efficiencies if 50 <= e < 80)
        low = sum(1 for e in all_efficiencies if e < 50)

        return {
            "average_progress": round(avg_progress, 1),
            "average_grade": round(avg_grade, 1),
            "completion_rate": round(completion_rate, 1),
            "students_completed": students_completed,
            "average_active_time": round(avg_active_time, 1),
            "average_sessions": round(avg_sessions, 1),
            "high_performers": high,
            "medium_performers": medium,
            "low_performers": low,
            "total_students": total_students,
        }

    async def get_progress_over_time_by_student_ids(
        self,
        student_ids: List[int],
    ) -> List[dict]:
        """
        Obtiene progreso mensual agregado para estudiantes de un curso.

        Returns:
            Lista de dicts con: month, year, average_progress, average_grade
        """
        if not student_ids:
            return []

        # Use raw SQL for date extraction
        query = """
            SELECT
                EXTRACT(MONTH FROM created_at) as month,
                EXTRACT(YEAR FROM created_at) as year,
                AVG(efficiency_rating) as avg_progress,
                AVG(objectives_completed) as avg_objectives
            FROM progresses
            WHERE student_id = ANY(:student_ids)
              AND deleted_at IS NULL
            GROUP BY EXTRACT(MONTH FROM created_at), EXTRACT(YEAR FROM created_at)
            ORDER BY year, month
        """
        result = await self.db.execute(
            query, {"student_ids": student_ids}
        )
        rows = result.fetchall()

        month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                       'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

        return [
            {
                "date": f"{month_names[int(r[0]) - 1]} {int(r[1])}",
                "averageProgress": round(float(r[2]), 1),
                "averageGrade": round(float(r[2]), 1),  # Same source
            }
            for r in rows
        ]

    async def get_activity_summary_by_student_ids(
        self,
        student_ids: List[int],
        days: int = 30,
    ) -> List[dict]:
        """
        Obtiene resumen de actividad diario para los últimos N días.

        Returns:
            Lista de dicts con: date, activeStudents, totalTimeSpent, averageSessionTime
        """
        if not student_ids:
            return []

        query = """
            SELECT
                DATE(created_at) as activity_date,
                COUNT(DISTINCT student_id) as active_students,
                SUM(attempt_count) * 5 as total_time_spent,
                AVG(attempt_count) * 5 as avg_session_time
            FROM progresses
            WHERE student_id = ANY(:student_ids)
              AND created_at >= CURRENT_DATE - INTERVAL ':days days'
              AND deleted_at IS NULL
            GROUP BY DATE(created_at)
            ORDER BY activity_date
        """
        result = await self.db.execute(
            query.replace(":days", str(days)),
            {"student_ids": student_ids}
        )
        rows = result.fetchall()

        return [
            {
                "date": r[0].strftime("%d %b") if hasattr(r[0], 'strftime') else str(r[0]),
                "activeStudents": int(r[1]),
                "totalTimeSpent": float(r[2]),
                "averageSessionTime": round(float(r[3]), 1),
            }
            for r in rows
        ]
