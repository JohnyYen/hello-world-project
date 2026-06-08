import pytest
from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

from src.course.domain.course import Course
from src.course.domain.course_enrollment import CourseEnrollment
from src.course.domain.course_professor import CourseProfessor
from src.course.infrastructure.course_repository import CourseRepository
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    return db


@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=CourseRepository)
    repo.get_by_id = AsyncMock()
    repo.get_by_id_with_relations = AsyncMock()
    repo.get_one_by_filters = AsyncMock()
    repo.bulk_create_enrollments = AsyncMock()
    repo.bulk_create_professors = AsyncMock()
    repo.soft_delete_enrollments_for_course = AsyncMock()
    repo.soft_delete_professors_for_course = AsyncMock()
    repo.soft_delete_course = AsyncMock()
    repo.get_students_for_course = AsyncMock()
    repo.get_professors_for_course = AsyncMock()
    repo.get_existing_enrollment_ids = AsyncMock()
    repo.get_existing_professor_ids = AsyncMock()
    repo.sync_students = AsyncMock()
    repo.sync_professors = AsyncMock()
    repo.list_with_counts = AsyncMock()
    repo.get_all = AsyncMock()
    repo.count = AsyncMock()
    return repo


@pytest.fixture
def sample_course_id():
    return uuid4()


@pytest.fixture
def sample_course(sample_course_id):
    course = MagicMock(spec=Course)
    course.id = sample_course_id
    course.name = "Matemáticas"
    course.description = "Curso de matemáticas básicas"
    course.school_year = "2025-2026"
    course.period_label = "Semestre 1"
    course.start_date = date(2025, 3, 1)
    course.end_date = date(2025, 7, 15)
    course.is_active = True
    course.is_deleted = False
    course.deleted_at = None
    course.created_at = datetime.utcnow()
    course.updated_at = None
    course.enrollments = []
    course.course_professors = []
    return course


@pytest.fixture
def sample_student_id():
    return uuid4()


@pytest.fixture
def sample_student_data(sample_student_id):
    return {
        "student_id": sample_student_id,
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "enrolled_at": "2025-03-01T00:00:00",
    }


@pytest.fixture
def sample_professor_id():
    return uuid4()


@pytest.fixture
def sample_professor_data(sample_professor_id):
    return {
        "professor_id": sample_professor_id,
        "name": "María García",
        "email": "maria@example.com",
    }
