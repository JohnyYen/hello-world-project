from typing import List, Dict, Optional
from uuid import UUID
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
                "school_year": course.school_year,
                "period_label": course.period_label,
                "start_date": course.start_date.isoformat() if course.start_date else "",
                "end_date": course.end_date.isoformat() if course.end_date else "",
                "totalStudents": student_count,
            }
            for course, student_count in course_tuples
        ]

    async def execute_metrics(self, course_ids: List[UUID]) -> List[Dict]:
        """
        Obtiene métricas para múltiples cursos usando batch queries.
        """
        if not course_ids:
            return []

        # Batch query for metrics
        batch_metrics = await self.progress_repo.aggregate_by_course_ids(course_ids)
        courses = await self.course_repo.get_courses_by_ids(course_ids)
        course_map = {c.id: c for c in courses}

        results = []
        for course_id in course_ids:
            course = course_map.get(course_id)
            if not course:
                continue
            
            # Get metrics from batch query
            metrics = batch_metrics.get(course_id, {})
            
            # Build result with proper field mapping
            results.append({
                "courseId": str(course_id),
                "courseName": course.name or "",  # From course object
                "schoolYear": course.school_year,
                "periodLabel": course.period_label,
                "averageProgress": round(float(metrics.get("average_progress", 0)), 1),
                "averageGrade": round(float(metrics.get("average_grade", 0)), 1),
                "completionRate": round(float(metrics.get("completion_rate", 0)), 1),
                "studentsCompleted": int(metrics.get("students_completed", 0)),
                "averageActiveTime": round(float(metrics.get("average_active_time", 0)), 1),
                "averageSessionsPerStudent": round(float(metrics.get("average_sessions", 0)), 1),
                "highPerformers": int(metrics.get("high_performers", 0)),
                "mediumPerformers": int(metrics.get("medium_performers", 0)),
                "lowPerformers": int(metrics.get("low_performers", 0)),
                "totalStudents": int(metrics.get("total_students", 0)),  # From batch_metrics
                "progressTrend": 0.0,
                "gradeTrend": 0.0,
                "engagementTrend": 0.0,
            })

        # Calculate trends by comparing consecutive courses
        if len(results) > 1:
            # Sort by school_year and period for proper comparison
            results_sorted = sorted(results, key=lambda x: (x["schoolYear"], x["period"]))
            
            for i in range(1, len(results_sorted)):
                current = results_sorted[i]
                previous = results_sorted[i - 1]
                
                # Only compare if consecutive periods
                if current["schoolYear"] == previous["schoolYear"]:
                    if previous["averageProgress"] > 0:
                        current["progressTrend"] = round(
                            ((current["averageProgress"] - previous["averageProgress"]) 
                             / previous["averageProgress"]) * 100, 1
                        )
                    if previous["averageGrade"] > 0:
                        current["gradeTrend"] = round(
                            ((current["averageGrade"] - previous["averageGrade"]) 
                             / previous["averageGrade"]) * 100, 1
                        )
                    if previous["averageSessionsPerStudent"] > 0:
                        current["engagementTrend"] = round(
                            ((current["averageSessionsPerStudent"] - previous["averageSessionsPerStudent"]) 
                             / previous["averageSessionsPerStudent"]) * 100, 1
                        )

        return results

    async def execute_kpis(self) -> Dict:
        """
        Obtiene KPIs generales para todos los cursos.
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

        # Batch query for all course metrics
        batch_metrics = await self.progress_repo.aggregate_by_course_ids(all_course_ids)
        course_map = {c.id: c for c, _ in course_tuples}

        # Build all_metrics with proper structure
        all_metrics = []
        for course, _ in course_tuples:
            metrics = batch_metrics.get(course.id, {})
            all_metrics.append({
                "course_id": str(course.id),
                "course_name": course.name,
                "school_year": course.school_year,
                "period_label": course.period_label,
                "average_progress": float(metrics.get("average_progress", 0)),
                "average_grade": float(metrics.get("average_grade", 0)),
                "completion_rate": float(metrics.get("completion_rate", 0)),
                "total_students": int(metrics.get("total_students", 0)),
            })

        # Get unique students count (not sum of enrollments)
        from sqlalchemy import text
        result = await self.course_repo.db.execute(
            text("SELECT COUNT(DISTINCT student_id) as unique_students FROM course_enrollments WHERE deleted_at IS NULL")
        )
        total_students = result.scalar() or 0
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

        # Calculate trends for individual courses
        trends_by_course_id = {}
        if len(all_metrics) > 1:
            all_metrics_sorted = sorted(all_metrics, key=lambda x: (x["school_year"], x.get("period", "")))
            
            for i in range(1, len(all_metrics_sorted)):
                current = all_metrics_sorted[i]
                previous = all_metrics_sorted[i - 1]
                
                course_id = current["course_id"]
                progress_trend = 0.0
                grade_trend = 0.0
                engagement_trend = 0.0
                
                if previous["average_progress"] > 0:
                    progress_trend = round(
                        ((current["average_progress"] - previous["average_progress"]) 
                         / previous["average_progress"]) * 100, 1
                    )
                if previous["average_grade"] > 0:
                    grade_trend = round(
                        ((current["average_grade"] - previous["average_grade"]) 
                         / previous["average_grade"]) * 100, 1
                    )
                
                trends_by_course_id[course_id] = {
                    "progress_trend": progress_trend,
                    "grade_trend": grade_trend,
                    "engagement_trend": 0.0,
                }

        # Year over year trends
        by_year = {}
        for m in all_metrics:
            year = m["school_year"]
            if year not in by_year:
                by_year[year] = []
            by_year[year].append(m)

        sorted_years = sorted(by_year.keys())
        progress_trends = []
        grade_trends = []
        
        for i in range(1, len(sorted_years)):
            prev_year = sorted_years[i - 1]
            curr_year = sorted_years[i]
            
            prev_avg_progress = sum(m["average_progress"] for m in by_year[prev_year]) / len(by_year[prev_year])
            curr_avg_progress = sum(m["average_progress"] for m in by_year[curr_year]) / len(by_year[curr_year])
            
            prev_avg_grade = sum(m["average_grade"] for m in by_year[prev_year]) / len(by_year[prev_year])
            curr_avg_grade = sum(m["average_grade"] for m in by_year[curr_year]) / len(by_year[curr_year])
            
            if prev_avg_progress > 0:
                progress_trends.append(((curr_avg_progress - prev_avg_progress) / prev_avg_progress) * 100)
            if prev_avg_grade > 0:
                grade_trends.append(((curr_avg_grade - prev_avg_grade) / prev_avg_grade) * 100)

        return {
            "totalCourses": len(all_metrics),
            "totalStudents": total_students,
            "overallCompletionRate": round(avg_completion, 1),
            "overallAverageGrade": round(avg_grade, 1),
            "topPerformingCourse": self._build_metrics_response(top_course, trends_by_course_id),
            "needsAttentionCourse": self._build_metrics_response(needs_attention, trends_by_course_id),
            "yearOverYearProgress": round(sum(progress_trends) / max(len(progress_trends), 1), 1) if progress_trends else 0.0,
            "yearOverYearGrade": round(sum(grade_trends) / max(len(grade_trends), 1), 1) if grade_trends else 0.0,
        }

    async def execute_progress_over_time(self, course_id: UUID) -> List[Dict]:
        """
        Obtiene progreso a lo largo del tiempo para un curso.
        """
        student_ids = await self.course_repo.get_student_ids_for_course(course_id)
        return await self.progress_repo.get_progress_over_time_by_student_ids(student_ids)

    async def execute_activity_summary(self, course_id: UUID, days: int = 30) -> List[Dict]:
        """
        Obtiene resumen de actividad para un curso.
        """
        student_ids = await self.course_repo.get_student_ids_for_course(course_id)
        return await self.progress_repo.get_activity_summary_by_student_ids(student_ids, days)

    def _build_metrics_response(self, metrics: Optional[Dict], trends_by_course_id: Optional[Dict] = None) -> Optional[Dict]:
        if not metrics:
            return None
        
        course_id = metrics.get("course_id", "")
        progress_trend = 0.0
        grade_trend = 0.0
        engagement_trend = 0.0
        
        if trends_by_course_id and course_id in trends_by_course_id:
            progress_trend = trends_by_course_id[course_id].get("progress_trend", 0.0)
            grade_trend = trends_by_course_id[course_id].get("grade_trend", 0.0)
            engagement_trend = trends_by_course_id[course_id].get("engagement_trend", 0.0)
        
        return {
            "courseId": course_id,
            "courseName": metrics.get("course_name", ""),  # From the dict
            "period": metrics.get("period", ""),
            "schoolYear": metrics.get("school_year", ""),
            "averageProgress": round(float(metrics.get("average_progress", 0)), 1),
            "averageGrade": round(float(metrics.get("average_grade", 0)), 1),
            "completionRate": round(float(metrics.get("completion_rate", 0)), 1),
            "studentsCompleted": 0,  # TODO: calculate properly
            "averageActiveTime": 0.0,
            "dailyActiveUsers": 0,
            "weeklyActiveUsers": 0,
            "averageSessionsPerStudent": 0.0,
            "highPerformers": 0,
            "mediumPerformers": 0,
            "lowPerformers": 0,
            "totalStudents": int(metrics.get("total_students", 0)),
            "progressTrend": progress_trend,
            "gradeTrend": grade_trend,
            "engagementTrend": engagement_trend,
        }
