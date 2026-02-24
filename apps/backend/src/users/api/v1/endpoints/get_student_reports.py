from fastapi import APIRouter
from src.users.api.v1.schemas.student import StudentReportsResponse


router = APIRouter(prefix="/students")


@router.get("/{id}/reports", response_model=StudentReportsResponse)
async def get_student_reports(id: int):
    """
    Obtener reportes individuales (desempeño, actividad, etc.)
    """
    # Datos de prueba
    mock_reports = {
        "student_id": id,
        "performance_report": {
            "average_score": 85.5,
            "completed_assignments": 12,
            "passed_assignments": 10,
            "failed_assignments": 2
        },
        "activity_report": {
            "total_sessions": 25,
            "total_time_spent": "20h 45m",
            "last_login": "2023-01-20T14:30:00"
        },
        "engagement_report": {
            "participation_rate": 78.3,
            "completed_activities": 45,
            "total_activities": 58
        }
    }

    return StudentReportsResponse(
        success=True,
        message="Reportes del estudiante obtenidos exitosamente",
        data=mock_reports
    )
