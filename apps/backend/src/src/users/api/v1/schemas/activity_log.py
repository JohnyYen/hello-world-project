from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActivityLogCreate(BaseModel):
    """Esquema para registrar una actividad"""
    activity_type: str
    occurred_at: Optional[datetime] = None
    metadata: Optional[dict] = None


class HeatMapDataPoint(BaseModel):
    """Punto de datos para el heatmap"""
    day: str
    hour: int
    value: int


class HeatMapResponse(BaseModel):
    """Respuesta para los datos del heatmap"""
    student_id: str
    days: int
    data: list[HeatMapDataPoint]
    total_activities: int


class ActivitySummaryResponse(BaseModel):
    """Resumen de actividad del estudiante"""
    student_id: str
    last_active_at: Optional[datetime]
    total_sessions: int
    current_streak: int
    active_today: bool