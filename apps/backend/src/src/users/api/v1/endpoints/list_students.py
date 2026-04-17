from uuid import UUID
from typing import List
from fastapi import APIRouter, Query, Depends
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User
from src.users.application.usecase.list_students_usecase import ListStudentsUseCase
from src.users.api.v1.schemas.student import StudentListResponse
from src.users.domain.student import Student
from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment


router = APIRouter(prefix="/students")


@router.get("", response_model=StudentListResponse)
async def list_students(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a devolver"),
    search: str = Query(None, description="Búsqueda por nombre o email"),
    course_id: UUID = Query(None, description="Filtrar estudiantes por curso"),
    list_students_uc: ListStudentsUseCase = Depends(),
):
    """
    Listar estudiantes (con filtros y paginación).

    Requiere autenticación y rol de professor o admin.
    """
    return await list_students_uc.execute(
        skip=skip, limit=limit, search=search, course_id=course_id
    )


@router.get("/courses", response_model=List[str])
async def get_student_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtener lista de cursos únicos que tienen estudiantes inscritos.

    Requiere autenticación y rol de professor o admin.
    """
    # Validar rol
    if current_user.role.role_name not in ["admin", "professor"]:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver cursos",
        )

    # Obtener cursos únicos con estudiantes
    query = (
        select(distinct(Course.name))
        .join(CourseEnrollment, CourseEnrollment.course_id == Course.id)
        .join(Student, Student.id == CourseEnrollment.student_id)
        .join(User, User.id == Student.user_id)
        .where(User.deleted_at.is_(None))
        .order_by(Course.name)
    )
    
    result = await db.execute(query)
    courses = [row[0] for row in result.all()]
    
    return courses
