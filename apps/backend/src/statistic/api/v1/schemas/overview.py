from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional


class OverviewKPIs(BaseModel):
    """KPIs globales del sistema educativo."""

    total_students: int = Field(
        ..., ge=0, description="Total de estudiantes registrados"
    )
    active_students_this_week: int = Field(
        ..., ge=0, description="Estudiantes activos esta semana"
    )
    active_students_this_month: int = Field(
        ..., ge=0, description="Estudiantes activos este mes"
    )
    total_levels_completed: int = Field(
        ..., ge=0, description="Total de niveles completados"
    )
    total_play_time_minutes: int = Field(
        ..., ge=0, description="Tiempo total de juego en minutos"
    )
    average_score: float = Field(
        ..., ge=0, le=100, description="Puntuación promedio (0-100)"
    )


class ActivityOverTimeItem(BaseModel):
    """Item individual de actividad temporal."""

    date: date = Field(..., description="Fecha del registro")
    sessions: int = Field(..., ge=0, description="Número de sesiones")
    active_students: int = Field(..., ge=0, description="Estudiantes activos ese día")
    play_time_minutes: int = Field(
        ..., ge=0, description="Tiempo de juego total en minutos"
    )


class LevelPerformanceItem(BaseModel):
    """Item de rendimiento por nivel."""

    level_name: str = Field(..., description="Nombre del nivel")
    completion_rate: float = Field(
        ..., ge=0, le=1, description="Tasa de completación (0-1)"
    )
    average_attempts: float = Field(
        ..., ge=0, description="Número promedio de intentos"
    )
    average_time_minutes: float = Field(
        ..., ge=0, description="Tiempo promedio en minutos"
    )


class OverviewTrends(BaseModel):
    """Tendencias comparadas con período anterior."""

    students_change_percent: float = Field(
        ..., description="Cambio porcentual en estudiantes"
    )
    activity_change_percent: float = Field(
        ..., description="Cambio porcentual en actividad"
    )
    score_change_percent: float = Field(
        ..., description="Cambio porcentual en puntuación"
    )


class OverviewResponse(BaseModel):
    """Respuesta completa del endpoint de overview."""

    kpis: OverviewKPIs = Field(..., description="KPIs globales")
    activity_over_time: List[ActivityOverTimeItem] = Field(
        default_factory=list, description="Evolución temporal de actividad"
    )
    level_performance: List[LevelPerformanceItem] = Field(
        default_factory=list, description="Rendimiento por nivel"
    )
    trends: OverviewTrends = Field(..., description="Tendencias vs período anterior")


class OverviewQueryParams(BaseModel):
    """Parámetros de query para el endpoint de overview."""

    start_date: Optional[date] = Field(None, description="Fecha de inicio para filtrar")
    end_date: Optional[date] = Field(None, description="Fecha de fin para filtrar")
    period: Optional[str] = Field(
        None,
        description="Período predefinido: 7d (7 días), 30d (30 días), 3m (3 meses)",
    )

    def validate_params(self) -> tuple[bool, Optional[str]]:
        """
        Valida los parámetros de query.

        Returns:
            tuple: (es_válido, mensaje_error)
        """
        # No se puede tener start_date Y period juntos
        if self.start_date and self.period:
            return False, "No se puede usar start_date y period simultáneamente"

        # end_date no puede ser menor que start_date
        if self.start_date and self.end_date and self.end_date < self.start_date:
            return False, "end_date no puede ser menor que start_date"

        # Validar valor de period
        if self.period and self.period not in ["7d", "30d", "3m"]:
            return False, "Period debe ser uno de: 7d, 30d, 3m"

        return True, None
