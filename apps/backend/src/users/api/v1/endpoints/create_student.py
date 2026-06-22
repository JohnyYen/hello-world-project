import logging

from fastapi import APIRouter, BackgroundTasks, Depends

from src.notification.application.service.email_service import EmailService
from src.shared.infrastructure.config import settings
from src.users.application.usecase.create_student_usecase import CreateStudentUseCase
from src.users.api.v1.schemas.student import StudentCreate, StudentResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students")


async def get_email_service() -> EmailService:
    return EmailService(settings)


@router.post("", response_model=StudentResponse)
async def create_student(
    student_data: StudentCreate,
    background_tasks: BackgroundTasks,
    create_student_uc: CreateStudentUseCase = Depends(),
    email_service: EmailService = Depends(get_email_service),
):
    """
    Registrar un nuevo estudiante.

    Requiere autenticación y rol de professor o admin.
    Luego de crear el estudiante, envía un email con sus credenciales.
    """
    result = await create_student_uc.execute(student_data=student_data)

    # ── Envío de email con credenciales ──
    student_name = f"{result.name} {result.lastname or ''}".strip()
    email_service.send_email_async(
        background_tasks=background_tasks,
        to_email=result.email,
        subject="Bienvenido a Hello World - Tus credenciales de acceso",
        template_name="email/student_credentials.html",
        context={
            "student_name": student_name,
            "username": result.username,
            "email": result.email,
        },
    )

    logger.info(
        "Queued credentials email for student %s (%s)",
        result.id,
        result.email,
    )

    return result
