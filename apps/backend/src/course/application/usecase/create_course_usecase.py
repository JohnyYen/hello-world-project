from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.course.domain.course import Course
from src.course.infrastructure.course_repository import CourseRepository
from src.course.api.v1.schemas.course_management import (
    CourseCreateRequest,
    CourseDetailResponse,
    CourseResponse,
    StudentEnrollmentResponse,
    ProfessorAssignmentResponse,
)
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


class CreateCourseUseCase:
    """
    Orquesta: crear curso + asignar estudiantes + asignar profesores.
    Todo en una sola transacción.
    """

    def __init__(self, db: AsyncSession, course_repo: CourseRepository):
        self.db = db
        self.course_repo = course_repo

    async def execute(self, request: CourseCreateRequest) -> CourseDetailResponse:
        """
        Crea un curso con estudiantes y profesores en una sola transacción.
        El SELECT de validación de duplicados se ejecuta DENTRO de begin()
        para que autobegin no abra una transacción previa y no se produzca el
        error 'A transaction is already begun on this Session'.
        """
        async with self.db.begin():
            existing = await self.course_repo.get_one_by_filters({
                "school_year": request.school_year,
                "period_label": request.period_label,
            })
            if existing:
                raise DuplicateEntryException(
                    f"Ya existe un curso para el período {request.school_year} - {request.period_label}"
                )

            course_data = request.model_dump(
                exclude={"student_ids", "professor_ids"},
                by_alias=False,
            )
            course = Course(**course_data)
            self.db.add(course)
            await self.db.flush()

            if request.student_ids:
                # Convertir User.id → Student.id antes de insertar en course_enrollments
                student_id_map = (
                    await self.course_repo.get_student_profile_ids(
                        request.student_ids
                    )
                )
                valid_student_ids = [
                    student_id_map[uid]
                    for uid in request.student_ids
                    if uid in student_id_map
                ]
                if valid_student_ids:
                    await self.course_repo.bulk_create_enrollments(
                        course.id, valid_student_ids
                    )

            if request.professor_ids:
                # Convertir User.id → Professor.id antes de insertar en course_professors
                professor_id_map = (
                    await self.course_repo.get_professor_profile_ids(
                        request.professor_ids
                    )
                )
                valid_professor_ids = [
                    professor_id_map[uid]
                    for uid in request.professor_ids
                    if uid in professor_id_map
                ]
                if valid_professor_ids:
                    await self.course_repo.bulk_create_professors(
                        course.id, valid_professor_ids
                    )

        await self.db.refresh(course)
        return await self._build_detail_response(course.id)

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
