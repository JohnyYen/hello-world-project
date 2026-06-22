import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.course.api.v1.schemas.course_management import (
    CourseCreateRequest,
    CourseDetailResponse,
    CourseResponse,
    CourseUpdateRequest,
    EnrollmentRequest,
    PaginatedCourseListResponse,
    ProfessorAssignmentResponse,
    StudentEnrollmentResponse,
)
from src.course.application.service.course_service import CourseService
from src.course.application.usecase.create_course_usecase import CreateCourseUseCase
from src.course.application.usecase.manage_enrollment_usecase import ManageEnrollmentUseCase
from src.course.application.usecase.update_course_usecase import UpdateCourseUseCase
from src.course.infrastructure.course_repository import CourseRepository
from src.notification.application.service.email_service import EmailService
from src.shared.deps import get_current_user
from src.shared.infrastructure.config import settings
from src.shared.infrastructure.session import get_db
from src.users.domain.user import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/courses",
    tags=["Course Management"],
    dependencies=[Depends(HTTPBearer())],
)


async def get_course_repository(
    db: AsyncSession = Depends(get_db),
) -> CourseRepository:
    return CourseRepository(db)


async def get_course_service(
    repo: CourseRepository = Depends(get_course_repository),
) -> CourseService:
    return CourseService(repo)


async def get_create_course_usecase(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
) -> CreateCourseUseCase:
    return CreateCourseUseCase(db, CourseRepository(db), current_user)


async def get_update_course_usecase(
    db: AsyncSession = Depends(get_db),
) -> UpdateCourseUseCase:
    return UpdateCourseUseCase(db, CourseRepository(db))


async def get_manage_enrollment_usecase(
    db: AsyncSession = Depends(get_db),
) -> ManageEnrollmentUseCase:
    return ManageEnrollmentUseCase(db, CourseRepository(db))


async def get_email_service() -> EmailService:
    return EmailService(settings)


@router.get("/management", response_model=PaginatedCourseListResponse)
async def list_courses(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Máximo de registros a retornar"),
    professor_id: Optional[UUID] = Query(None, description="Filtrar por ID de profesor"),
    school_year: Optional[str] = Query(None, description="Filtrar por año escolar (ej: 2024-2025)"),
    service: CourseService = Depends(get_course_service),
    current_user = Depends(get_current_user),
):
    """
    Lista cursos paginados con conteo de estudiantes y profesores.
    Filtros opcionales: professor_id, school_year.
    Si el usuario es profesor, filtra automáticamente por su profesor_id.
    """
    # Si es profesor y no se pasó professor_id explícito, usar el suyo
    if current_user.role.role_name == "professor" and not professor_id:
        professor_id_map = await service.repository.get_professor_profile_ids(
            [current_user.id]
        )
        professor_id = professor_id_map.get(current_user.id)

    results, total = await service.list_courses_with_counts(
        professor_id=professor_id,
        school_year=school_year,
        skip=skip,
        limit=limit,
    )
    items = []
    for course, student_count, professor_count in results:
        item = CourseResponse.model_validate(course)
        item.student_count = student_count
        item.professor_count = professor_count
        items.append(item)

    return PaginatedCourseListResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("/management", response_model=CourseDetailResponse, status_code=201)
async def create_course(
    request: CourseCreateRequest,
    background_tasks: BackgroundTasks,
    usecase: CreateCourseUseCase = Depends(get_create_course_usecase),
    email_service: EmailService = Depends(get_email_service),
    current_user: User = Depends(get_current_user),
    course_repo: CourseRepository = Depends(get_course_repository),
):
    """
    Crea un nuevo curso con asignación de estudiantes y profesores.
    Valida que no exista duplicado de school_year + period_label.
    Luego de crear, envía email de notificación a cada estudiante y
    a los profesores asignados (excepto al creador del curso).
    """
    result = await usecase.execute(request)

    professors_list = [
        {"name": p.name, "email": p.email}
        for p in result.professors
    ]

    # ── Envío de emails a estudiantes ──
    # NOTA: Se envía el email aunque el juego no tenga download_link.
    # El template (course_enrollment.html) ya maneja el condicional
    # {% if download_link %} para mostrar/ocultar el botón de descarga.
    if result.students:
        for student in result.students:
            student_name = f"{student.name} {student.lastname or ''}".strip()
            email_service.send_email_async(
                background_tasks=background_tasks,
                to_email=student.email,
                subject=f"Bienvenido al curso: {result.name}",
                template_name="email/course_enrollment.html",
                context={
                    "student_name": student_name,
                    "course_name": result.name,
                    "course_description": result.description or "",
                    "school_year": result.school_year,
                    "period_label": result.period_label,
                    "start_date": result.start_date.isoformat(),
                    "end_date": result.end_date.isoformat(),
                    "professors": professors_list,
                    "download_link": result.game.download_link if result.game else None,
                },
            )

        logger.info(
            "Queued %d enrollment emails for course %s",
            len(result.students),
            result.id,
        )

    # ── Envío de emails a profesores asignados (excluyendo al creador) ──
    professors_for_course = result.professors

    if professors_for_course:
        # Obtener el professor_id del usuario actual para excluirlo
        creator_professor_map = await course_repo.get_professor_profile_ids(
            [current_user.id]
        )
        creator_professor_id = creator_professor_map.get(current_user.id)

        for professor in professors_for_course:
            # No enviar email al creador del curso
            if creator_professor_id and professor.professor_id == creator_professor_id:
                continue

            email_service.send_email_async(
                background_tasks=background_tasks,
                to_email=professor.email,
                subject=f"Has sido asignado al curso: {result.name}",
                template_name="email/course_invitation_professor.html",
                context={
                    "professor_name": professor.name,
                    "course_name": result.name,
                    "course_description": result.description or "",
                    "school_year": result.school_year,
                    "period_label": result.period_label,
                    "start_date": result.start_date.isoformat(),
                    "end_date": result.end_date.isoformat(),
                    "professors": professors_list,
                    "dashboard_url": f"{settings.APP_URL or 'http://localhost:3000'}/dashboard/courses/{result.id}",
                },
            )

        logger.info(
            "Queued %d professor invitation emails for course %s",
            len(professors_for_course) - (1 if creator_professor_id else 0),
            result.id,
        )

    return result


@router.get("/{course_id}", response_model=CourseDetailResponse)
async def get_course_detail(
    course_id: UUID,
    usecase: CreateCourseUseCase = Depends(get_create_course_usecase),
):
    """
    Obtiene detalle completo de un curso: datos, estudiantes y profesores inscritos.
    """
    return await usecase._build_detail_response(course_id)


@router.put("/{course_id}", response_model=CourseDetailResponse)
async def update_course(
    course_id: UUID,
    request: CourseUpdateRequest,
    background_tasks: BackgroundTasks,
    usecase: UpdateCourseUseCase = Depends(get_update_course_usecase),
    email_service: EmailService = Depends(get_email_service),
    current_user: User = Depends(get_current_user),
    course_repo: CourseRepository = Depends(get_course_repository),
):
    """
    Actualiza un curso existente. Sincroniza estudiantes y profesores si se proveen.
    Valida unicidad de school_year + period_label si cambian.
    Si se agregaron nuevos profesores, envía email de notificación.
    """
    # Capturar IDs de profesores existentes ANTES de la actualización
    existing_professor_ids = await course_repo.get_existing_professor_ids(course_id)

    # Obtener professor_id del usuario actual (para excluirlo de las notificaciones)
    creator_professor_map = await course_repo.get_professor_profile_ids(
        [current_user.id]
    )
    creator_professor_id = creator_professor_map.get(current_user.id)

    # Ejecutar la actualización
    result = await usecase.execute(course_id, request)

    # ── Envío de emails a nuevos profesores ──
    if request.professor_ids is not None and result.professors:
        # Detectar profesores NUEVOS (no estaban antes)
        new_professors = [
            p
            for p in result.professors
            if p.professor_id not in existing_professor_ids
        ]

        if new_professors:
            professors_list = [
                {"name": p.name, "email": p.email}
                for p in result.professors
            ]

            for professor in new_professors:
                # No enviar email al creador del curso
                if creator_professor_id and professor.professor_id == creator_professor_id:
                    continue

                email_service.send_email_async(
                    background_tasks=background_tasks,
                    to_email=professor.email,
                    subject=f"Has sido asignado al curso: {result.name}",
                    template_name="email/course_invitation_professor.html",
                    context={
                        "professor_name": professor.name,
                        "course_name": result.name,
                        "course_description": result.description or "",
                        "school_year": result.school_year,
                        "period_label": result.period_label,
                        "start_date": result.start_date.isoformat(),
                        "end_date": result.end_date.isoformat(),
                        "professors": professors_list,
                        "dashboard_url": f"{settings.APP_URL}/dashboard/courses/{result.id}",
                    },
                )

            logger.info(
                "Queued %d professor invitation emails for course %s (update)",
                len([p for p in new_professors if not (creator_professor_id and p.professor_id == creator_professor_id)]),
                course_id,
            )

    return result


@router.delete("/{course_id}", status_code=204)
async def delete_course(
    course_id: UUID,
    usecase: ManageEnrollmentUseCase = Depends(get_manage_enrollment_usecase),
):
    """
    Elimina un curso (soft delete) con cascada:
    inscripciones → asignaciones de profesores → curso.
    """
    await usecase.delete_course(course_id)


@router.get("/{course_id}/students", response_model=list[StudentEnrollmentResponse])
async def list_enrolled_students(
    course_id: UUID,
    usecase: ManageEnrollmentUseCase = Depends(get_manage_enrollment_usecase),
):
    """
    Lista estudiantes inscritos en un curso.
    """
    return await usecase.get_students(course_id)


@router.post("/{course_id}/students", response_model=list[StudentEnrollmentResponse])
async def enroll_students(
    course_id: UUID,
    request: EnrollmentRequest,
    background_tasks: BackgroundTasks,
    usecase: ManageEnrollmentUseCase = Depends(get_manage_enrollment_usecase),
    email_service: EmailService = Depends(get_email_service),
    course_repo: CourseRepository = Depends(get_course_repository),
):
    """
    Inscribe uno o más estudiantes en un curso.
    Deduplica: no crea inscripciones duplicadas.
    Si el curso tiene un juego asignado con download_link,
    envía email de notificación a los nuevos estudiantes.
    """
    # Capturar IDs existentes antes de inscribir (para detectar nuevos)
    existing_ids = await course_repo.get_existing_enrollment_ids(course_id)

    # Inscribir estudiantes
    result = await usecase.enroll_students(course_id, request.student_ids)

    # ── Envío de emails a nuevos estudiantes ──
    # NOTA: Se envía el email aunque el juego no tenga download_link.
    # El template (course_enrollment.html) ya maneja el condicional
    # {% if download_link %} para mostrar/ocultar el botón de descarga.
    if not result:
        return result

    course = await course_repo.get_course_with_game(course_id)
    if not course:
        logger.info(
            "Course %s not found — skipping enrollment emails",
            course_id,
        )
        return result

    # Detectar estudiantes nuevos (los que no estaban inscritos antes)
    new_enrollments = [
        s for s in result if s.student_id not in existing_ids
    ]

    if not new_enrollments:
        logger.info(
            "No new enrollments for course %s — skipping emails",
            course_id,
        )
        return result

    professors_data = await course_repo.get_professors_for_course(course_id)
    professors_list = [
        {"name": p["name"], "email": p["email"]}
        for p in professors_data
    ]

    for student in new_enrollments:
        student_name = f"{student.name} {student.lastname or ''}".strip()
        email_service.send_email_async(
            background_tasks=background_tasks,
            to_email=student.email,
            subject=f"Bienvenido al curso: {course.name}",
            template_name="email/course_enrollment.html",
            context={
                "student_name": student_name,
                "course_name": course.name,
                "course_description": course.description or "",
                "school_year": course.school_year,
                "period_label": course.period_label,
                "start_date": course.start_date.isoformat(),
                "end_date": course.end_date.isoformat(),
                "professors": professors_list,
                "download_link": course.game.download_link if course.game else None,
            },
        )

    logger.info(
        "Queued %d enrollment emails for course %s",
        len(new_enrollments),
        course_id,
    )

    return result


@router.delete("/{course_id}/students/{student_id}", status_code=204)
async def unenroll_student(
    course_id: UUID,
    student_id: UUID,
    usecase: ManageEnrollmentUseCase = Depends(get_manage_enrollment_usecase),
):
    """
    Desinscribe un estudiante de un curso (soft delete).
    """
    result = await usecase.unenroll_student(course_id, student_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no inscrito en el curso",
        )
