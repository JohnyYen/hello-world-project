from fastapi import APIRouter, Query, Depends

from src.users.application.usecase.list_students_usecase import ListStudentsUseCase
from src.users.api.v1.schemas.student import StudentListResponse


router = APIRouter(prefix="/students")


@router.get("", response_model=StudentListResponse)
async def list_students(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a devolver"),
    search: str = Query(None, description="Búsqueda por nombre o email"),
    list_students_uc: ListStudentsUseCase = Depends(),
):
    """
    Listar estudiantes (con filtros y paginación).

    Requiere autenticación y rol de professor o admin.
    """
    return await list_students_uc.execute(skip=skip, limit=limit, search=search)
