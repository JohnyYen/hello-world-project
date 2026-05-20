from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.course.infrastructure.course_repository import CourseRepository
from src.course.api.v1.schemas.course_management import (
    CourseUpdateRequest,
    CourseDetailResponse,
    CourseResponse,
    StudentEnrollmentResponse,
    ProfessorAssignmentResponse,
)
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


class UpdateCourseUseCase:
    """
    Orquesta: actualizar curso + sincronizar estudiantes/profesores.
    """

    def __init__(self, db: AsyncSession, course_repo: CourseRepository):
        self.db = db
        self.course_repo = course_repo

    async def execute(
        self, course_id: UUID, request: CourseUpdateRequest
    ) -> CourseDetailResponse:
        """
        Actualiza un curso y sincroniza estudiantes/profesores en una sola transacción.
        Todo el flujo se ejecuta dentro de un único begin() para evitar que autobegin
        abra una transacción implícita previa y se produzca el error de doble-begin.
        """
        async with self.db.begin():
            course = await self.course_repo.get_by_id(course_id)
            if not course:
                raise NotFoundException("Curso no encontrado")

            update_data = request.model_dump(
                exclude_unset=True,
                exclude={"student_ids", "professor_ids"},
                by_alias=False,
            )

            if update_data:
                if "school_year" in update_data or "period_label" in update_data:
                    filters = {}
                    if "school_year" in update_data:
                        filters["school_year"] = update_data["school_year"]
                    else:
                        filters["school_year"] = course.school_year
                    if "period_label" in update_data:
                        filters["period_label"] = update_data["period_label"]
                    else:
                        filters["period_label"] = course.period_label

                    existing = await self.course_repo.get_one_by_filters(filters)
                    if existing and existing.id != course_id:
                        raise DuplicateEntryException(
                            f"Ya existe otro curso para el período {filters['school_year']} - {filters['period_label']}"
                        )

                for field, value in update_data.items():
                    setattr(course, field, value)

            if request.student_ids is not None:
                await self.course_repo.sync_students(course_id, request.student_ids)

            if request.professor_ids is not None:
                await self.course_repo.sync_professors(
                    course_id, request.professor_ids
                )

        await self.db.refresh(course)
        return await self._build_detail_response(course_id)

    async def _build_detail_response(
        self, course_id: UUID
    ) -> CourseDetailResponse:
        course = await self.course_repo.get_by_id_with_relations(course_id)
        if not course:
            raise NotFoundException("Curso no encontrado")

        students_data = await self.course_repo.get_students_for_course(course_id)
        professors_data = await self.course_repo.get_professors_for_course(course_id)

        course_resp = CourseResponse.model_validate(course)
        course_resp.student_count = len(students_data)
        course_resp.professor_count = len(professors_data)

        return CourseDetailResponse(
            **course_resp.model_dump(by_alias=True),
            students=[
                StudentEnrollmentResponse.model_validate(s) for s in students_data
            ],
            professors=[
                ProfessorAssignmentResponse.model_validate(p)
                for p in professors_data
            ],
        )
