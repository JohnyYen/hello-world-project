from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class StudentReportKPIs(BaseModel):
    total_levels_completed: int = Field(..., description="Total de niveles completados")
    total_games_played: int = Field(..., description="Total de juegos jugados")
    total_play_time: int = Field(..., description="Tiempo total de juego en minutos")
    average_score: float = Field(..., description="Puntuación promedio")
    current_streak: int = Field(..., description="Racha actual de días")
    last_activity: Optional[datetime] = Field(None, description="Última actividad")


class ProgressOverTimeItem(BaseModel):
    date: str = Field(..., description="Fecha del registro")
    level: int = Field(..., description="Número de nivel")
    score: int = Field(..., description="Puntuación obtenida")
    time_spent: int = Field(..., description="Tiempo invertido en minutos")


class LevelPerformanceItem(BaseModel):
    level_name: str = Field(..., description="Nombre del nivel")
    score: float = Field(..., description="Puntuación promedio obtenida")
    attempts: int = Field(..., description="Número de intentos")
    time_spent: int = Field(..., description="Tiempo invertido en minutos")
    completed: bool = Field(..., description="Si el nivel fue completado")


class ActivityDistributionItem(BaseModel):
    game_name: str = Field(..., description="Nombre del juego")
    time_spent: int = Field(..., description="Tiempo invertido en minutos")
    sessions: int = Field(..., description="Número de sesiones")


class StudentProgressResponse(BaseModel):
    student_id: str = Field(..., description="ID del estudiante (UUID)")
    kpis: StudentReportKPIs = Field(..., description="KPIs del progreso del estudiante")
    progress_over_time: List[ProgressOverTimeItem] = Field(
        default_factory=list, description="Progreso a lo largo del tiempo"
    )
    level_performance: List[LevelPerformanceItem] = Field(
        default_factory=list, description="Rendimiento por nivel"
    )
    activity_distribution: List[ActivityDistributionItem] = Field(
        default_factory=list, description="Distribución de actividades"
    )
