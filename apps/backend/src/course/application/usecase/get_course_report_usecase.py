from typing import List, Dict, Optional
from src.course.infrastructure.course_repository import CourseRepository
from src.statistic.infrastructure.progress_repository import ProgressRepository


class GetCourseReportUseCase:
    """
    Caso de uso para obtener reportes a nivel de curso.

    Agrega datos de progreso de estudiantes inscritos en cada curso.
    """

    def __init__(
        self,
        course_repo: CourseRepository,
        progress_repo: ProgressRepository,
    ):
        self.course_repo = course_repo
        self.progress_repo = progress_repo

    async def execute_list(self) -> List[Dict]:
        """
        Obtiene lista de cursos con conteo de estudiantes.
        """
        course_tuples = await self.course_repo.get_all_with_enrollment_counts()
        return [
            {
                "id": course.id,
                "name": course.name,
                "display_period": course.display_period or f"{course.school_year} - {course.period_label}",
                "school_year": course.school_year,
                "start_date": course.start_date.isoformat() if course.start_date else "",
                "end_date": course.end_date.isoformat() if course.end_date else "",
                "totalStudents": student_count,
            }
            for course, student_count in course_tuples
        ]

    async def execute_metrics(self, course_ids: List[int]) -> List[Dict]:
        """
        Obtiene métricas para múltiples cursos usando batch queries (2 queries total).
        """
        if not course_ids:
            return []

        # Batch: 2 queries total regardless of course count
        batch_metrics = await self.progress_repo.aggregate_by_course_ids(course_ids)
        courses = await self.course_repo.get_courses_by_ids(course_ids)
        course_map = {c.id: c for c in courses}

        results = []
        for course_id in course_ids:
            course = course_map.get(course_id)
            if not course:
                continue

            metrics = batch_metrics.get(course_id, {})
            results.append({
                "course_id": str(course_id),
                "course_name": course.name,
                "period": course.display_period or f"{course.school_year} - {course.period_label}",
                "school_year": course.school_year,
                **metrics,
            })

        return results

    async def execute_kpis(self) -> Dict:
        """
        Obtiene KPIs generales para todos los cursos usando batch query (2 queries total).
        """
        course_tuples = await self.course_repo.get_all_with_enrollment_counts()
        all_course_ids = [c.id for c, _ in course_tuples]

        if not all_course_ids:
            return {
                "totalCourses": 0, "totalStudents": 0,
                "overallCompletionRate": 0, "overallAverageGrade": 0,
                "topPerformingCourse": None, "needsAttentionCourse": None,
                "yearOverYearProgress": 0, "yearOverYearGrade": 0,
            }

        # Single batch query for all course metrics
        batch_metrics = await self.progress_repo.aggregate_by_course_ids(all_course_ids)
        course_map = {c.id: c for c, _ in course_tuples}

        all_metrics = []
        for course, _ in course_tuples:
            metrics = batch_metrics.get(course.id, {})
            all_metrics.append({
                "course_id": str(course.id),
                "course_name": course.name,
                "period": course.display_period or f"{course.school_year} - {course.period_label}",
                "school_year": course.school_year,
                **metrics,
            })

        total_students = sum(m["total_students"] for m in all_metrics)
        avg_completion = (
            sum(m["completion_rate"] for m in all_metrics) / len(all_metrics)
            if all_metrics else 0
        )
        avg_grade = (
            sum(m["average_grade"] for m in all_metrics) / len(all_metrics)
            if all_metrics else 0
        )

        # Top and bottom performing courses
        sorted_by_grade = sorted(all_metrics, key=lambda x: x["average_grade"], reverse=True)
        top_course = sorted_by_grade[0] if sorted_by_grade else None
        needs_attention = sorted_by_grade[-1] if sorted_by_grade else None

        # Year over year trends (compare consecutive periods)
        sorted_by_year = sorted(all_metrics, key=lambda x: x["school_year"])
        progress_trends = []
        grade_trends = []
        for i in range(1, len(sorted_by_year)):
            prev = sorted_by_year[i - 1]
            curr = sorted_by_year[i]
            if prev["average_progress"] > 0:
                progress_trends.append(
                    ((curr["average_progress"] - prev["average_progress"])
                     / prev["average_progress"]) * 100
                )
            if prev["average_grade"] > 0:
                grade_trends.append(
                    ((curr["average_grade"] - prev["average_grade"])
                     / prev["average_grade"]) * 100
                )

        return {
            "totalCourses": len(all_metrics),
            "totalStudents": total_students,
            "overallCompletionRate": round(avg_completion, 1),
            "overallAverageGrade": round(avg_grade, 1),
            "topPerformingCourse": self._build_metrics_response(top_course),
            "needsAttentionCourse": self._build_metrics_response(needs_attention),
            "yearOverYearProgress": round(sum(progress_trends) / max(len(progress_trends), 1), 1),
            "yearOverYearGrade": round(sum(grade_trends) / max(len(grade_trends), 1), 1),
        }

    async def execute_progress_over_time(self, course_id: int) -> List[Dict]:
        """
        Obtiene progreso a lo largo del tiempo para un curso.
        """
        student_ids = await self.course_repo.get_student_ids_for_course(course_id)
        return await self.progress_repo.get_progress_over_time_by_student_ids(student_ids)

    async def execute_activity_summary(self, course_id: int, days: int = 30) -> List[Dict]:
        """
        Obtiene resumen de actividad para un curso.
        """
        student_ids = await self.course_repo.get_student_ids_for_course(course_id)
        return await self.progress_repo.get_activity_summary_by_student_ids(student_ids, days)

    def _build_metrics_response(self, metrics: Optional[Dict]) -> Optional[Dict]:
        if not metrics:
            return None
        # Build new dict instead of mutating the repo result
        return {
            "course_id": metrics["course_id"],
            "course_name": metrics["course_name"],
            "period": metrics["period"],
            "school_year": metrics["school_year"],
            "averageProgress": metrics["average_progress"],
            "averageGrade": metrics["average_grade"],
            "completionRate": metrics["completion_rate"],
            "studentsCompleted": metrics["students_completed"],
            "averageActiveTime": metrics["average_active_time"],
            # TODO: Implementar cálculo real desde logs de actividad del servidor
            "dailyActiveUsers": 0,
            "weeklyActiveUsers": 0,
            "averageSessionsPerStudent": metrics["average_sessions"],
            "highPerformers": metrics["high_performers"],
            "mediumPerformers": metrics["medium_performers"],
            "lowPerformers": metrics["low_performers"],
            # TODO: Implementar cálculo de tendencias comparando períodos consecutivos
            "progressTrend": 0.0,
            "gradeTrend": 0.0,
            "engagementTrend": 0.0,
        }
