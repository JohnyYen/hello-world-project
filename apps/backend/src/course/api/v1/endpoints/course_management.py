from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
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
from src.shared.deps import get_current_user
from src.shared.infrastructure.session import get_db

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
    usecase: CreateCourseUseCase = Depends(get_create_course_usecase),
):
    """
    Crea un nuevo curso con asignación de estudiantes y profesores.
    Valida que no exista duplicado de school_year + period_label.
    """
    return await usecase.execute(request)


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
    usecase: UpdateCourseUseCase = Depends(get_update_course_usecase),
):
    """
    Actualiza un curso existente. Sincroniza estudiantes y profesores si se proveen.
    Valida unicidad de school_year + period_label si cambian.
    """
    return await usecase.execute(course_id, request)


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
    usecase: ManageEnrollmentUseCase = Depends(get_manage_enrollment_usecase),
):
    """
    Inscribe uno o más estudiantes en un curso.
    Deduplica: no crea inscripciones duplicadas.
    """
    return await usecase.enroll_students(course_id, request.student_ids)


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
