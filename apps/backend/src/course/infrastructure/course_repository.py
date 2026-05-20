from typing import List, Optional, Dict, Any, Set
from uuid import UUID as UUIDType
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.sql.selectable import Select
from sqlalchemy.orm import selectinload
from src.shared.infrastructure.repositories.base_repository import BaseRepository
from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment
from src.course.domain.course_professor import CourseProfessor
from src.users.domain.student import Student
from src.users.domain.professor import Professor
from src.users.domain.user import User
from src.game.infrastructure.game_instance_repository import GameInstanceRepository
from src.game.domain.game_instance import GameInstance
from src.shared.domain.enums import GameStatus


class CourseRepository(BaseRepository[Course]):
    """Repositorio para el modelo Course con soporte de enrollments."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Course)

    async def get_all_with_enrollment_counts(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[tuple[Course, int]]:
        """
        Obtiene todos los cursos con la cantidad de estudiantes inscritos.

        Returns:
            Lista de tuplas (Course, student_count)
        """
        query = (
            select(Course, func.count(CourseEnrollment.student_id).label("student_count"))
            .outerjoin(CourseEnrollment, Course.id == CourseEnrollment.course_id)
            .where(Course.is_deleted == False)
            .group_by(Course.id)
            .order_by(Course.school_year.desc(), Course.period_label)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.all()

    async def get_student_ids_for_course(self, course_id: UUIDType) -> List[UUIDType]:
        """
        Obtiene los IDs de estudiantes inscritos en un curso.
        """
        query = (
            select(CourseEnrollment.student_id)
            .where(CourseEnrollment.course_id == course_id)
        )
        result = await self.db.execute(query)
        return [row[0] for row in result.all()]

    async def get_all_student_ids_batch(
        self,
        course_ids: Optional[List[UUIDType]] = None,
    ) -> Dict[UUIDType, List[UUIDType]]:
        """
        Obtiene IDs de estudiantes para múltiples cursos en una sola query.
        """
        query = select(CourseEnrollment.course_id, CourseEnrollment.student_id)
        if course_ids:
            query = query.where(CourseEnrollment.course_id.in_(course_ids))

        result = await self.db.execute(query)
        rows = result.all()

        mapping: Dict[UUIDType, List[UUIDType]] = {}
        for course_id, student_id in rows:
            if course_id not in mapping:
                mapping[course_id] = []
            mapping[course_id].append(student_id)

        return mapping

    async def get_courses_by_ids(self, course_ids: List[UUIDType]) -> List[Course]:
        """
        Obtiene múltiples objetos Course por ID en una sola query.
        """
        query = select(Course).where(
            Course.id.in_(course_ids),
            Course.is_deleted == False,
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    # ── New for Management ──

    async def get_by_id_with_relations(
        self, course_id: UUIDType
    ) -> Optional[Course]:
        """
        Eager load enrollments + course_professors with their related users.
        """
        query = (
            select(Course)
            .options(
                selectinload(Course.enrollments).selectinload(
                    CourseEnrollment.student
                ).selectinload(Student.user),
                selectinload(Course.course_professors).selectinload(
                    CourseProfessor.professor
                ).selectinload(Professor.user),
            )
            .where(Course.id == course_id, Course.deleted_at.is_(None))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_student_profile_ids(
        self, user_ids: list[UUIDType]
    ) -> dict[UUIDType, UUIDType]:
        """
        Convierte User.id (cuenta de usuario) → Student.id (perfil de estudiante).
        Retorna un dict {user_id: student_id} para convertir los IDs que envía el frontend.
        """
        if not user_ids:
            return {}
        query = select(Student.id, Student.user_id).where(
            Student.user_id.in_(user_ids), Student.deleted_at.is_(None)
        )
        result = await self.db.execute(query)
        rows = result.all()
        return {row.user_id: row.id for row in rows}

    async def get_professor_profile_ids(
        self, user_ids: list[UUIDType]
    ) -> dict[UUIDType, UUIDType]:
        """
        Convierte User.id (cuenta de usuario) → Professor.id (perfil de profesor).
        Retorna un dict {user_id: professor_id} para convertir los IDs que envía el frontend.
        """
        if not user_ids:
            return {}
        query = select(Professor.id, Professor.user_id).where(
            Professor.user_id.in_(user_ids), Professor.deleted_at.is_(None)
        )
        result = await self.db.execute(query)
        rows = result.all()
        return {row.user_id: row.id for row in rows}

    async def bulk_create_enrollments(
        self, course_id: UUIDType, student_ids: list[UUIDType]
    ) -> list[CourseEnrollment]:
        """
        Crea múltiples inscripciones en batch.
        IMPORTANTE: `student_ids` debe ser Student.id (perfil de estudiante),
        NO User.id (cuenta de usuario). Usar get_student_profile_ids() para convertir.
        """
        enrollments = [
            CourseEnrollment(course_id=course_id, student_id=sid)
            for sid in student_ids
        ]
        self.db.add_all(enrollments)
        await self.db.flush()
        return enrollments

    async def bulk_create_professors(
        self, course_id: UUIDType, professor_ids: list[UUIDType]
    ) -> list[CourseProfessor]:
        """
        Crea múltiples asignaciones de profesores en batch.
        """
        professors = [
            CourseProfessor(course_id=course_id, professor_id=pid)
            for pid in professor_ids
        ]
        self.db.add_all(professors)
        await self.db.flush()
        return professors

    async def soft_delete_enrollments_for_course(
        self, course_id: UUIDType
    ) -> int:
        """
        Soft delete of all active enrollments for a course.
        """
        now = datetime.utcnow()
        result = await self.db.execute(
            update(CourseEnrollment)
            .where(
                CourseEnrollment.course_id == course_id,
                CourseEnrollment.deleted_at.is_(None),
            )
            .values(deleted_at=now, is_deleted=True)
        )
        await self.db.commit()
        return result.rowcount

    async def soft_delete_professors_for_course(
        self, course_id: UUIDType
    ) -> int:
        """
        Soft delete of all active professor assignments for a course.
        """
        now = datetime.utcnow()
        result = await self.db.execute(
            update(CourseProfessor)
            .where(
                CourseProfessor.course_id == course_id,
                CourseProfessor.deleted_at.is_(None),
            )
            .values(deleted_at=now, is_deleted=True)
        )
        await self.db.commit()
        return result.rowcount

    async def soft_delete_course(self, course_id: UUIDType) -> bool:
        """
        Soft delete of a course.
        """
        now = datetime.utcnow()
        result = await self.db.execute(
            update(Course)
            .where(Course.id == course_id, Course.deleted_at.is_(None))
            .values(deleted_at=now, is_deleted=True)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def get_students_for_course(
        self, course_id: UUIDType
    ) -> list[dict[str, Any]]:
        """
        Obtiene estudiantes inscritos con nombre, email y fecha de inscripción.
        Join: CourseEnrollment → Student → User
        """
        query = (
            select(
                CourseEnrollment.student_id,
                User.name,
                User.lastname,
                User.email,
                CourseEnrollment.enrolled_at,
            )
            .join(Student, Student.id == CourseEnrollment.student_id)
            .join(User, User.id == Student.user_id)
            .where(
                CourseEnrollment.course_id == course_id,
                CourseEnrollment.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(query)
        rows = result.all()
        return [
            {
                "student_id": row.student_id,
                "name": row.name,
                "lastname": row.lastname,
                "email": row.email,
                "enrolled_at": row.enrolled_at.isoformat() if row.enrolled_at else None,
            }
            for row in rows
        ]

    async def get_professors_for_course(
        self, course_id: UUIDType
    ) -> list[dict[str, Any]]:
        """
        Obtiene profesores asignados con nombre y email.
        Join: CourseProfessor → Professor → User
        """
        query = (
            select(
                CourseProfessor.professor_id,
                User.name,
                User.email,
            )
            .join(Professor, Professor.id == CourseProfessor.professor_id)
            .join(User, User.id == Professor.user_id)
            .where(
                CourseProfessor.course_id == course_id,
                CourseProfessor.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(query)
        rows = result.all()
        return [
            {
                "professor_id": row.professor_id,
                "name": row.name,
                "email": row.email,
            }
            for row in rows
        ]

    async def get_existing_enrollment_ids(
        self, course_id: UUIDType
    ) -> Set[UUIDType]:
        """
        Obtiene los IDs de estudiantes actualmente inscritos (para dedup/sync).
        """
        query = select(CourseEnrollment.student_id).where(
            CourseEnrollment.course_id == course_id,
            CourseEnrollment.deleted_at.is_(None),
        )
        result = await self.db.execute(query)
        return {row[0] for row in result.all()}

    async def get_existing_professor_ids(
        self, course_id: UUIDType
    ) -> Set[UUIDType]:
        """
        Obtiene los IDs de profesores actualmente asignados (para sync).
        """
        query = select(CourseProfessor.professor_id).where(
            CourseProfessor.course_id == course_id,
            CourseProfessor.deleted_at.is_(None),
        )
        result = await self.db.execute(query)
        return {row[0] for row in result.all()}

    async def sync_students(
        self, course_id: UUIDType, student_ids: list[UUIDType]
    ) -> None:
        """
        Sincroniza estudiantes: crea nuevos, elimina los removidos.

        IMPORTANTE: `student_ids` se espera como User.id (lo que envía el frontend).
        Se convierte internamente a Student.id antes de escribir en course_enrollments.
        """
        # Convertir User.id → Student.id
        student_id_map = await self.get_student_profile_ids(student_ids)
        valid_student_ids = [
            student_id_map[uid]
            for uid in student_ids
            if uid in student_id_map
        ]

        current_ids = await self.get_existing_enrollment_ids(course_id)
        target_ids = set(valid_student_ids)

        to_add = target_ids - current_ids
        to_remove = current_ids - target_ids

        if to_add:
            await self.bulk_create_enrollments(course_id, list(to_add))

        if to_remove:
            now = datetime.utcnow()
            await self.db.execute(
                update(CourseEnrollment)
                .where(
                    CourseEnrollment.course_id == course_id,
                    CourseEnrollment.student_id.in_(list(to_remove)),
                    CourseEnrollment.deleted_at.is_(None),
                )
                .values(deleted_at=now, is_deleted=True)
            )

    async def sync_professors(
        self, course_id: UUIDType, professor_ids: list[UUIDType]
    ) -> None:
        """
        Sincroniza profesores: crea nuevos, elimina los removidos.

        IMPORTANTE: `professor_ids` se espera como User.id (lo que envía el frontend).
        Se convierte internamente a Professor.id antes de escribir en course_professors.
        """
        # Convertir User.id → Professor.id
        professor_id_map = await self.get_professor_profile_ids(professor_ids)
        valid_professor_ids = [
            professor_id_map[uid]
            for uid in professor_ids
            if uid in professor_id_map
        ]

        current_ids = await self.get_existing_professor_ids(course_id)
        target_ids = set(valid_professor_ids)

        to_add = target_ids - current_ids
        to_remove = current_ids - target_ids

        if to_add:
            await self.bulk_create_professors(course_id, list(to_add))

        if to_remove:
            now = datetime.utcnow()
            await self.db.execute(
                update(CourseProfessor)
                .where(
                    CourseProfessor.course_id == course_id,
                    CourseProfessor.professor_id.in_(list(to_remove)),
                    CourseProfessor.deleted_at.is_(None),
                )
                .values(deleted_at=now, is_deleted=True)
            )

    async def list_with_counts(
        self,
        professor_id: Optional[UUIDType] = None,
        school_year: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[tuple[Course, int, int]], int]:
        """
        Lista cursos con conteo de estudiantes y profesores, paginado y filtrado.

        Usa subqueries correlacionadas en el SELECT principal para evitar el efecto
        multiplicador que aparece al hacer JOIN encadenado de CourseEnrollment +
        CourseProfessor (cada combinación estudiante × profesor infla los COUNT).
        """
        # Subquery correlacionada: estudiantes activos por curso (sin JOIN)
        student_count_subq = (
            select(func.count(CourseEnrollment.student_id))
            .where(
                CourseEnrollment.course_id == Course.id,
                CourseEnrollment.deleted_at.is_(None),
            )
            .scalar_subquery()
        )

        # Subquery correlacionada: profesores activos por curso (sin JOIN)
        professor_count_subq = (
            select(func.count(CourseProfessor.professor_id))
            .where(
                CourseProfessor.course_id == Course.id,
                CourseProfessor.deleted_at.is_(None),
            )
            .scalar_subquery()
        )

        base_query = (
            select(
                Course,
                student_count_subq.label("student_count"),
                professor_count_subq.label("professor_count"),
            )
            .where(Course.deleted_at.is_(None))
        )

        if school_year:
            base_query = base_query.where(Course.school_year == school_year)

        if professor_id:
            base_query = base_query.where(
                Course.id.in_(
                    select(CourseProfessor.course_id).where(
                        CourseProfessor.professor_id == professor_id,
                        CourseProfessor.deleted_at.is_(None),
                    )
                )
            )

        count_query = select(func.count()).select_from(base_query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        query = (
            base_query
            .group_by(Course.id)
            .order_by(Course.school_year.desc(), Course.period_label)
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)
        rows = result.all()
        return list(rows), total

    async def is_professor_assigned_to_course(
        self, professor_user_id: UUIDType, course_id: UUIDType
    ) -> bool:
        """
        Verifica si un profesor (por su user.id) está asignado a un curso.

        Hace JOIN contra CourseProfessor → Professor para obtenerlo en un solo query.
        """
        query = (
            select(func.count())
            .select_from(CourseProfessor)
            .join(Professor, Professor.id == CourseProfessor.professor_id)
            .where(
                CourseProfessor.course_id == course_id,
                Professor.user_id == professor_user_id,
                CourseProfessor.deleted_at.is_(None),
            )
        )
        result = await self.db.execute(query)
        return (result.scalar() or 0) > 0

    async def get_course_with_game(
        self, course_id: UUIDType
    ) -> Course | None:
        """
        Obtiene un curso con su juego asociado cargado.
        """
        query = (
            select(Course)
            .options(selectinload(Course.game))
            .where(Course.id == course_id, Course.deleted_at.is_(None))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def has_active_game_instances(self, course_id: UUIDType) -> bool:
        """
        Verifica si un curso tiene instancias de juego activas o en pausa.

        Delega la consulta a GameInstanceRepository para mantener la
        responsabilidad de cada dominio en su propio repositorio.
        """
        instance_repo = GameInstanceRepository(self.db)
        return await instance_repo.has_active_instances_for_course(
            course_id, include_deleted=False
        )

    async def get_profile_id_by_user_id(
        self, user_id: UUIDType, profile_type: str
    ) -> UUIDType | None:
