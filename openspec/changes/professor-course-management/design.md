# Design: Gestión de Cursos para Profesores

## Technical Approach

Backend-first, frontend-second, siguiendo Clean Architecture existente en el proyecto.

**Backend**: Se crea un nuevo `course_management` sub-router bajo `course/api/v1/`, paralelo al `course_reports` existente. Ambos comparten el prefijo `/courses` pero resuelven rutas sin conflicto gracias a sub-routers separados. La capa de negocio sigue el patrón Service + UseCase: `CourseService` extiende `BaseService` para CRUD simple, y `CreateCourseUseCase`, `UpdateCourseUseCase`, `ManageEnrollmentUseCase` orquestan operaciones multi-entidad. El `CourseRepository` se extiende con métodos transaccionales. El filtrado `?role=student|professor` se agrega al endpoint `GET /users` existente.

**Frontend**: Ruta `/dashboard/cursos/` con Server Component para listado, Client Component para formularios interactivos. Server Actions para mutaciones. API consumida via `api/client.ts` (native fetch pattern existente).

## Architecture Decisions

### Decision 1: Sub-router separation (reports vs management)

**Choice**: Dos sub-routers independientes bajo un mismo namespace `/courses`
**Alternatives considered**: Un solo router con todo mezclado; prefix separado como `/courses-admin`
**Rationale**: El router `course/api/v1/router.py` actual solo incluye `course_reports_router`. Se refactoriza para que incluya ambos sub-routers (reports + management) usando `prefix="/courses"` a nivel del sub-router actual y creando management con `prefix=""`. Esto evita conflictos de ruta porque FastAPI resuelve por orden de inclusión y los paths NO se solapan:
- Reports: `GET /courses/`, `GET /courses/reports/kpis`, `GET /courses/metrics`, `GET /courses/{course_id}/metrics`, etc.
- Management: `POST /courses/`, `PUT /courses/{id}`, `DELETE /courses/{id}`, `POST /courses/{id}/students`, `DELETE /courses/{id}/students/{student_id}`, etc.

### Decision 2: Transaction handling via UseCases, not Service

**Choice**: Operaciones multi-entidad (create course + assignments, update course + sync, soft delete cascade) en UseCases con transacciones SQLAlchemy explícitas via `async with db.begin()`
**Alternatives considered**: Manejo en Service usando hooks post-save; callback pattern en el Service
**Rationale**: El patrón existente dicta Service para CRUD simple y UseCase para orquestación multi-entidad (ver `Backend AGENTS.md`). Las transacciones explícitas evitan estados inconsistentes. El `BaseRepository.create()` ya hace commit individual, por lo que para operaciones atómicas se debe usar `db.begin()` a nivel UseCase.

### Decision 3: Soft delete cascade en UseCase, no en DB constraint

**Choice**: El `DeleteCourseUseCase` marca `deleted_at` en Course, luego manualmente en CourseEnrollment y CourseProfessor relacionados
**Alternatives considered**: Cascade SQL a nivel DB (ON DELETE CASCADE); trigger de BD
**Rationale**: Soft delete ya está implementado via `Base.deleted_at`/`is_deleted`. No hay CASCADE configurado en las FKs. Hacer cascade en el UseCase mantiene consistencia con el patrón existente y permite lógica adicional (logging, eventos). No se requiere migración.

### Decision 4: Role filtering via new endpoint instead of modifying existing GET /users

**Choice**: Nuevo endpoint `GET /api/v1/users/by-role?role=student` y `GET /api/v1/users/by-role?role=professor` en vez de modificar `GET /users/`
**Alternatives considered**: Agregar `role` query param a `GET /users/` existente
**Rationale**: El endpoint `GET /users/` existente usa `ListUsersUseCase` que carga todas las relaciones (eager loading pesado). Para filtrado por rol necesitamos un query optimizado. Un nuevo endpoint más específico es cleaner y no arriesga romper el listado existente. Además, separar preocupaciones: users list ≠ filtered role queries.

### Decision 5: Frontend — Server Component for list page, Client Component for form

**Choice**: `page.tsx` es Server Component que obtiene datos y renderiza `CourseTable` (Client) que maneja interactividad (filtros, paginación, acciones). Formulario crear/editar es Client Component con `useActionState`.
**Alternatives considered**: Todo Server Component con form nativo HTML; todo Client Component
**Rationale**: Alinea con el patrón existente en `students/page.tsx` (Server Component → Client Table). Server Actions para mutaciones siguen Next.js 15 best practices. `useActionState` maneja pending states sin boilerplate.

### Decision 6: Multi-select estudiantes/profesores con shadcn Command + Popover

**Choice**: Usar `@/components/ui/command` + `@/components/ui/popover` (ya instalados) para un combo-box multi-select con búsqueda
**Alternatives considered**: Select nativo múltiple; react-select
**Rationale**: shadcn/ui ya está en el proyecto, consistente con el resto del frontend. Command + Popover son los bloques que shadcn recomienda para multi-select. Se puede construir un `MultiSelect` component reutilizable.

## Data Flow

### Create Course Flow

```
Browser                       Frontend                          Backend
  │                              │                                │
  │  POST /dashboard/cursos      │                                │
  │  (Server Action)             │                                │
  │ ──────────────────────────►  │                                │
  │                              │  GET /api/v1/courses/management │
  │                              │  POST {course, student_ids,    │
  │                              │        professor_ids}          │
  │                              │ ────────────────────────────►  │
  │                              │                                │  CourseRepository
  │                              │                                │  ├── get_by_id (validate)
  │                              │                                │  ├── create (course)
  │                              │                                │  ├── bulk_create_enrollments
  │                              │                                │  └── bulk_create_professors
  │                              │                                │
  │                              │  ← 201 {course, students,      │
  │                              │        professors}             │
  │                              │                                │
  │  ← revalidatePath + redirect │                                │
  │    /dashboard/cursos         │                                │
```

### Enroll Student Flow

```
Browser                       Frontend                            Backend
  │                              │                                  │
  │  POST /dashboard/cursos/{id} │                                  │
  │  (Server Action: addStudent) │                                  │
  │ ──────────────────────────►  │                                  │
  │                              │  POST /api/v1/courses/{id}/      │
  │                              │  students {student_ids: [...]}   │
  │                              │ ──────────────────────────────►  │
  │                              │                                  │
  │                              │                                  │  ManageEnrollmentUseCase
  │                              │                                  │  ├── validate students exist
  │                              │                                  │  ├── validate not already enrolled
  │                              │                                  │  ├── create CourseEnrollment
  │                              │                                  │  └── return updated list
  │                              │                                  │
  │                              │  ← 200 {students: [...]}         │
  │                              │                                  │
  │  ← revalidatePath            │                                  │
```

### Soft Delete Course Cascade

```
ManageEnrollmentUseCase.delete_course(course_id)
  │
  ├── Step 1: Get Course by ID (404 if not found)
  ├── Step 2: Soft delete all CourseEnrollment records
  │           UPDATE course_enrollments SET deleted_at = NOW()
  │           WHERE course_id = :course_id AND deleted_at IS NULL
  ├── Step 3: Soft delete all CourseProfessor records
  │           UPDATE course_professors SET deleted_at = NOW()
  │           WHERE course_id = :course_id AND deleted_at IS NULL
  ├── Step 4: Soft delete Course
  │           UPDATE courses SET deleted_at = NOW(), is_deleted = True
  │           WHERE id = :course_id
  └── Step 5: Commit transaction
```

## File Changes

### Backend (8 new, 4 modified)

| File | Action | Description |
|------|--------|-------------|
| `apps/backend/src/course/api/v1/router.py` | **Modify** | Add management sub-router alongside existing reports sub-router |
| `apps/backend/src/course/api/v1/endpoints/course_management.py` | **Create** | All CRUD + enrollment endpoints for course management |
| `apps/backend/src/course/api/v1/schemas/course_management.py` | **Create** | Pydantic v2 schemas for request/response |
| `apps/backend/src/course/application/service/course_service.py` | **Create** | CourseService extending BaseService |
| `apps/backend/src/course/application/usecase/create_course_usecase.py` | **Create** | Orchestrate course + assignments creation |
| `apps/backend/src/course/application/usecase/update_course_usecase.py` | **Create** | Update course + sync student/professor assignments |
| `apps/backend/src/course/application/usecase/manage_enrollment_usecase.py` | **Create** | Enroll/unenroll + soft delete cascade |
| `apps/backend/src/course/infrastructure/course_repository.py` | **Modify** | Add `create_with_assignments()`, `get_by_id_with_relations()`, `bulk_create_enrollments()`, `bulk_create_professors()`, `soft_delete_relations()` |
| `apps/backend/src/users/api/v1/endpoints/get_users_by_role.py` | **Create** | New endpoint for `GET /users/by-role?role=student\|professor` |
| `apps/backend/src/users/api/v1/router.py` | **Modify** | Include new `get_users_by_role` router |
| `apps/backend/src/users/application/usecase/list_users_by_role_usecase.py` | **Create** | UseCase for filtered user listing by role |
| `packages/api-contract/openapi.json` | **Modify** | Add new endpoints |

### Frontend (6 new, 1 modified)

| File | Action | Description |
|------|--------|-------------|
| `apps/frontend/src/components/dashboard/app-sidebar.tsx` | **Modify** | Add "Cursos" nav item with `BookOpen` icon |
| `apps/frontend/src/app/dashboard/cursos/page.tsx` | **Create** | Server Component: loads courses, renders CourseTable |
| `apps/frontend/src/app/dashboard/cursos/[id]/page.tsx` | **Create** | Server Component: course detail with student list |
| `apps/frontend/src/components/cursos/course-table.tsx` | **Create** | Client Component: table with search, pagination, actions |
| `apps/frontend/src/components/cursos/course-form.tsx` | **Create** | Client Component: create/edit form with multi-select |
| `apps/frontend/src/components/cursos/multi-select.tsx` | **Create** | Reusable multi-select combobox (Command + Popover) |
| `apps/frontend/src/services/courses.ts` | **Create** | Service layer: wraps `coursesApi` calls |
| `apps/frontend/src/api/client.ts` | **Modify** | Add `coursesApi` object with all course management endpoints |

## Interfaces / Contracts

### Backend Schemas

```python
# apps/backend/src/course/api/v1/schemas/course_management.py

from pydantic import BaseModel, Field, UUID4, field_validator
from typing import Optional
from datetime import date


class CourseCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    school_year: str = Field(..., alias="schoolYear")
    period_label: str = Field(..., alias="periodLabel")
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")
    student_ids: list[UUID4] = Field(default=[], alias="studentIds")
    professor_ids: list[UUID4] = Field(default=[], alias="professorIds")

    model_config = {"populate_by_name": True}


class CourseUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    school_year: Optional[str] = Field(None, alias="schoolYear")
    period_label: Optional[str] = Field(None, alias="periodLabel")
    start_date: Optional[date] = Field(None, alias="startDate")
    end_date: Optional[date] = Field(None, alias="endDate")
    student_ids: Optional[list[UUID4]] = Field(None, alias="studentIds")
    professor_ids: Optional[list[UUID4]] = Field(None, alias="professorIds")
    is_active: Optional[bool] = Field(None, alias="isActive")

    model_config = {"populate_by_name": True}


class EnrollmentRequest(BaseModel):
    student_ids: list[UUID4] = Field(..., alias="studentIds")

    model_config = {"populate_by_name": True}


class CourseResponse(BaseModel):
    id: UUID4
    name: str
    description: Optional[str] = None
    school_year: str = Field(alias="schoolYear")
    period_label: str = Field(alias="periodLabel")
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    is_active: bool = Field(alias="isActive")
    student_count: int = 0
    professor_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class CourseDetailResponse(CourseResponse):
    students: list[StudentEnrollmentResponse] = []
    professors: list[ProfessorAssignmentResponse] = []


class StudentEnrollmentResponse(BaseModel):
    student_id: UUID4 = Field(alias="studentId")
    name: str
    email: str
    enrolled_at: str = Field(alias="enrolledAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class ProfessorAssignmentResponse(BaseModel):
    professor_id: UUID4 = Field(alias="professorId")
    name: str
    email: str

    model_config = {"from_attributes": True, "populate_by_name": True}


class PaginatedCourseListResponse(BaseModel):
    items: list[CourseResponse]
    total: int
    skip: int
    limit: int
```

### Frontend Types

```typescript
// apps/frontend/src/types/course.interface.ts

interface Course {
  id: string;
  name: string;
  description: string | null;
  schoolYear: string;
  periodLabel: string;
  startDate: string;
  endDate: string;
  isActive: boolean;
  studentCount: number;
  professorCount: number;
  createdAt: string | null;
  updatedAt: string | null;
}

interface CourseDetail extends Course {
  students: StudentEnrollment[];
  professors: ProfessorAssignment[];
}

interface StudentEnrollment {
  studentId: string;
  name: string;
  email: string;
  enrolledAt: string;
}

interface ProfessorAssignment {
  professorId: string;
  name: string;
  email: string;
}

interface CourseCreate {
  name: string;
  description?: string;
  schoolYear: string;
  periodLabel: string;
  startDate: string;
  endDate: string;
  studentIds: string[];
  professorIds: string[];
}

interface CourseUpdate {
  name?: string;
  description?: string;
  schoolYear?: string;
  periodLabel?: string;
  startDate?: string;
  endDate?: string;
  studentIds?: string[];
  professorIds?: string[];
  isActive?: boolean;
}

interface EnrollmentRequest {
  studentIds: string[];
}

interface PaginatedCourseList {
  items: Course[];
  total: number;
  skip: number;
  limit: number;
}
```

### API Client

```typescript
// apps/frontend/src/api/client.ts — add coursesApi

export const coursesApi = {
  list: (token: string, skip = 0, limit = 100) =>
    request<PaginatedCourseList>(
      `/api/v1/courses/management?skip=${skip}&limit=${limit}`,
      { token }
    ),

  getById: (courseId: string, token: string) =>
    request<CourseDetail>(
      `/api/v1/courses/${courseId}`,
      { token }
    ),

  create: (body: CourseCreate, token: string) =>
    request<CourseDetail>(
      "/api/v1/courses/management",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  update: (courseId: string, body: CourseUpdate, token: string) =>
    request<CourseDetail>(
      `/api/v1/courses/${courseId}`,
      { method: "PUT", body: JSON.stringify(body), token }
    ),

  delete: (courseId: string, token: string) =>
    request<{ success: boolean }>(
      `/api/v1/courses/${courseId}`,
      { method: "DELETE", token }
    ),

  getStudents: (courseId: string, token: string) =>
    request<StudentEnrollment[]>(
      `/api/v1/courses/${courseId}/students`,
      { token }
    ),

  enrollStudents: (courseId: string, body: EnrollmentRequest, token: string) =>
    request<StudentEnrollment[]>(
      `/api/v1/courses/${courseId}/students`,
      { method: "POST", body: JSON.stringify(body), token }
    ),

  unenrollStudent: (courseId: string, studentId: string, token: string) =>
    request<{ success: boolean }>(
      `/api/v1/courses/${courseId}/students/${studentId}`,
      { method: "DELETE", token }
    ),

  listByRole: (role: "student" | "professor", token: string) =>
    request<UserResponse[]>(
      `/api/v1/users/by-role?role=${role}`,
      { token }
    ),
};
```

## Backend Architecture Detail

### Router Structure

```
course/api/v1/router.py
├── reports_router (prefix="/courses")
│   ├── GET /courses/
│   ├── GET /courses/reports/kpis
│   ├── GET /courses/metrics
│   ├── GET /courses/{course_id}/metrics
│   ├── GET /courses/{course_id}/progress-over-time
│   └── GET /courses/{course_id}/activity-summary
│
└── management_router (prefix="/courses")
    ├── POST /courses/management
    ├── GET /courses/management
    ├── GET /courses/{course_id}
    ├── PUT /courses/{course_id}
    ├── DELETE /courses/{course_id}
    ├── GET /courses/{course_id}/students
    ├── POST /courses/{course_id}/students
    └── DELETE /courses/{course_id}/students/{student_id}
```

**Implementation:**
```python
# course/api/v1/router.py (modified)
from fastapi import APIRouter
from src.course.api.v1.endpoints.course_reports import router as course_reports_router
from src.course.api.v1.endpoints.course_management import router as course_management_router

router = APIRouter()
router.include_router(course_reports_router)      # prefix="/courses" defined in sub-router
router.include_router(course_management_router)    # prefix="/courses" defined in sub-router
```

**Importante**: Incluir `management_router` DESPUÉS de `reports_router` para que las rutas específicas (`POST /courses/{course_id}/students`) tengan prioridad sobre las genéricas (`GET /courses/{course_id}/metrics`).

### Endpoint Organization — course_management.py

Sigue el patrón "one file per domain" pero con múltiples endpoints (como `course_reports.py`), no "one file per endpoint" (como users), porque los endpoints de management están fuertemente acoplados y comparten dependencias.

```python
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.shared.infrastructure.session import get_db
from src.course.infrastructure.course_repository import CourseRepository
from src.course.application.service.course_service import CourseService
from src.course.application.usecase.create_course_usecase import CreateCourseUseCase
from src.course.application.usecase.update_course_usecase import UpdateCourseUseCase
from src.course.application.usecase.manage_enrollment_usecase import ManageEnrollmentUseCase
from src.course.api.v1.schemas.course_management import (
    CourseCreateRequest, CourseUpdateRequest, CourseResponse,
    CourseDetailResponse, PaginatedCourseListResponse,
    EnrollmentRequest, StudentEnrollmentResponse,
)

router = APIRouter(
    prefix="/courses",
    tags=["Course Management"],
    dependencies=[Depends(HTTPBearer())],
)
```

### CourseService

```python
# course/application/service/course_service.py
from src.shared.application.usecase.base_service import BaseService
from src.course.domain.course import Course
from src.course.infrastructure.course_repository import CourseRepository


class CourseService(BaseService[Course]):
    """
    CRUD básico de cursos, validaciones de dominio simples.
    Delega al UseCase operaciones multi-entidad.
    """

    def __init__(self, repository: CourseRepository):
        super().__init__(repository, Course)

    async def get_course_by_id(self, course_id: UUID) -> Optional[Course]:
        return await self.get_by_id(course_id)

    async def list_courses(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[Course], int]:
        courses = await self.get_all(skip=skip, limit=limit, order_by="school_year", descending=True)
        total = await self.count()
        return courses, total
```

### CreateCourseUseCase

```python
# course/application/usecase/create_course_usecase.py
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.course.infrastructure.course_repository import CourseRepository
from src.course.api.v1.schemas.course_management import (
    CourseCreateRequest, CourseDetailResponse,
    StudentEnrollmentResponse, ProfessorAssignmentResponse,
)
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


class CreateCourseUseCase:
    """
    Orquesta: crear curso + asignar estudiantes + asignar profesores.
    TODO operación en una sola transacción.
    """

    def __init__(self, db: AsyncSession, course_repo: CourseRepository):
        self.db = db
        self.course_repo = course_repo

    async def execute(self, request: CourseCreateRequest) -> CourseDetailResponse:
        # 1. Validar unicidad de school_year + period_label
        existing = await self.course_repo.get_one_by_filters({
            "school_year": request.school_year,
            "period_label": request.period_label,
        })
        if existing:
            raise DuplicateEntryException(
                f"Ya existe un curso para el período {request.school_year} - {request.period_label}"
            )

        # 2. Transacción: crear curso + enrollments + professors
        async with self.db.begin():
            course = await self.course_repo.create(request.model_dump(exclude={"student_ids", "professor_ids"}))
            await self.course_repo.bulk_create_enrollments(course.id, request.student_ids)
            await self.course_repo.bulk_create_professors(course.id, request.professor_ids)

        await self.db.refresh(course)
        # 3. Retornar con relaciones cargadas
        return await self._build_detail_response(course.id)

    async def _build_detail_response(self, course_id: UUID) -> CourseDetailResponse:
        # fetch course + enrollments + professors
        ...
```

### ManageEnrollmentUseCase

```python
# course/application/usecase/manage_enrollment_usecase.py

class ManageEnrollmentUseCase:
    """
    Inscribir/desinscribir estudiantes + soft delete cascade.
    """

    def __init__(self, db: AsyncSession, course_repo: CourseRepository):
        self.db = db
        self.course_repo = course_repo

    async def enroll_students(self, course_id: UUID, student_ids: list[UUID]) -> list[StudentEnrollmentResponse]:
        # Validar que course existe
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException("Curso no encontrado")

        # Validar que no estén ya inscritos
        existing_ids = await self.course_repo.get_student_ids_for_course(course_id)
        new_ids = [sid for sid in student_ids if sid not in existing_ids]

        async with self.db.begin():
            await self.course_repo.bulk_create_enrollments(course_id, new_ids)

        # Retornar lista actualizada
        return await self.course_repo.get_students_for_course(course_id)

    async def unenroll_student(self, course_id: UUID, student_id: UUID) -> bool:
        async with self.db.begin():
            result = await self.course_repo.soft_delete_enrollment(course_id, student_id)
        return result

    async def delete_course(self, course_id: UUID) -> bool:
        """Soft delete cascade: enrollments → professors → course"""
        async with self.db.begin():
            await self.course_repo.soft_delete_enrollments_for_course(course_id)
            await self.course_repo.soft_delete_professors_for_course(course_id)
            result = await self.course_repo.soft_delete_course(course_id)
        return result
```

### Repository Extensions

```python
# course/infrastructure/course_repository.py — new methods

class CourseRepository(BaseRepository[Course]):

    # ── Existing ──
    async def get_all_with_enrollment_counts(self, ...): ...
    async def get_student_ids_for_course(self, course_id: UUID) -> list[UUID]: ...
    async def get_all_student_ids_batch(self, ...): ...
    async def get_courses_by_ids(self, course_ids: list[UUID]) -> list[Course]: ...

    # ── New for Management ──
    async def get_by_id_with_relations(self, course_id: UUID) -> Optional[Course]:
        """
        Eager load enrollments + course_professors.
        """
        query = (
            select(Course)
            .options(
                selectinload(Course.enrollments).selectinload(CourseEnrollment.student),
                selectinload(Course.course_professors).selectinload(CourseProfessor.professor),
            )
            .where(Course.id == course_id, Course.deleted_at.is_(None))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def bulk_create_enrollments(
        self, course_id: UUID, student_ids: list[UUID]
    ) -> list[CourseEnrollment]:
        enrollments = [
            CourseEnrollment(course_id=course_id, student_id=sid)
            for sid in student_ids
        ]
        self.db.add_all(enrollments)
        await self.db.flush()
        return enrollments

    async def bulk_create_professors(
        self, course_id: UUID, professor_ids: list[UUID]
    ) -> list[CourseProfessor]:
        professors = [
            CourseProfessor(course_id=course_id, professor_id=pid)
            for pid in professor_ids
        ]
        self.db.add_all(professors)
        await self.db.flush()
        return professors

    async def soft_delete_enrollments_for_course(self, course_id: UUID) -> int:
        result = await self.db.execute(
            update(CourseEnrollment)
            .where(CourseEnrollment.course_id == course_id, CourseEnrollment.deleted_at.is_(None))
            .values(deleted_at=datetime.utcnow(), is_deleted=True)
        )
        return result.rowcount

    async def soft_delete_professors_for_course(self, course_id: UUID) -> int:
        result = await self.db.execute(
            update(CourseProfessor)
            .where(CourseProfessor.course_id == course_id, CourseProfessor.deleted_at.is_(None))
            .values(deleted_at=datetime.utcnow(), is_deleted=True)
        )
        return result.rowcount

    async def soft_delete_course(self, course_id: UUID) -> bool:
        result = await self.db.execute(
            update(Course)
            .where(Course.id == course_id, Course.deleted_at.is_(None))
            .values(deleted_at=datetime.utcnow(), is_deleted=True)
        )
        return result.rowcount > 0

    async def get_students_for_course(
        self, course_id: UUID
    ) -> list[StudentEnrollmentResponse]:
        # join User + CourseEnrollment for student name/email
        ...

    async def get_professors_for_course(
        self, course_id: UUID
    ) -> list[ProfessorAssignmentResponse]:
        # join User + CourseProfessor for professor name/email
        ...
```

### Role-based User Filtering

```python
# users/api/v1/endpoints/get_users_by_role.py
@router.get("/by-role", response_model=UserListResponse)
async def get_users_by_role(
    role: str = Query(..., description="Filter by role: 'student' or 'professor'"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    usecase: ListUsersByRoleUseCase = Depends(),
):
    return await usecase.execute(role=role, skip=skip, limit=limit)
```

## Frontend Architecture

### Route Structure

```
apps/frontend/src/app/dashboard/cursos/
├── page.tsx                    # Server Component — listado de cursos
├── [id]/page.tsx               # Server Component — detalle de curso
├── loading.tsx                 # Loading UI
└── error.tsx                   # Error boundary
```

### Component Tree

```
Server Components (page.tsx)
└── CourseTable (Client Component)
    ├── Search + Filters bar
    ├── DataTable (shadcn Table)
    │   ├── Row actions: Ver, Editar, Eliminar
    │   └── Pagination
    └── CreateCourseDialog
        └── CourseForm (Client Component)
            ├── Text inputs (name, description, dates, etc.)
            ├── MultiSelect (estudiantes)
            └── MultiSelect (profesores)

Server Components ([id]/page.tsx)
└── CourseDetail (Client Component)
    ├── Course info card
    ├── StudentsTable (shadcn Table)
    │   ├── Row: Nombre, Email, Fecha inscripción, Acción (Desinscribir)
    │   └── EnrollStudentDialog
    │       └── MultiSelect (estudiantes)
    └── Professors section
```

### Server/Client Component Split

| Component | Type | Why |
|-----------|------|-----|
| `page.tsx` | Server | Fetch data, SEO, initial render |
| `CourseTable` | Client | Interactivity (filters, pagination, modal) |
| `CourseForm` | Client | Form state, useActionState |
| `MultiSelect` | Client | Search, selection state |
| `CourseDetail` | Client | Interactive enrollment actions |
| `detail/page.tsx` | Server | Fetch course detail |

### Server Actions

```typescript
// apps/frontend/src/app/dashboard/cursos/actions.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { coursesApi } from "@/api/client";

export async function createCourse(formData: FormData) {
  const token = (await cookies()).get("auth_token")?.value;
  if (!token) throw new Error("No autenticado");

  const body = {
    name: formData.get("name") as string,
    description: formData.get("description") as string,
    schoolYear: formData.get("schoolYear") as string,
    periodLabel: formData.get("periodLabel") as string,
    startDate: formData.get("startDate") as string,
    endDate: formData.get("endDate") as string,
    studentIds: JSON.parse(formData.get("studentIds") as string),
    professorIds: JSON.parse(formData.get("professorIds") as string),
  };

  await coursesApi.create(body, token);
  revalidatePath("/dashboard/cursos");
  redirect("/dashboard/cursos");
}

export async function deleteCourse(courseId: string) {
  const token = (await cookies()).get("auth_token")?.value;
  if (!token) throw new Error("No autenticado");

  await coursesApi.delete(courseId, token);
  revalidatePath("/dashboard/cursos");
}

export async function enrollStudents(courseId: string, studentIds: string[]) {
  const token = (await cookies()).get("auth_token")?.value;
  if (!token) throw new Error("No autenticado");

  await coursesApi.enrollStudents(courseId, { studentIds }, token);
  revalidatePath(`/dashboard/cursos/${courseId}`);
}

export async function unenrollStudent(courseId: string, studentId: string) {
  const token = (await cookies()).get("auth_token")?.value;
  if (!token) throw new Error("No autenticado");

  await coursesApi.unenrollStudent(courseId, studentId, token);
  revalidatePath(`/dashboard/cursos/${courseId}`);
}
```

### Course List Page Pattern (StudentTable-like)

```typescript
// apps/frontend/src/app/dashboard/cursos/page.tsx
import CourseTable from "@/components/cursos/course-table";
import { coursesApi } from "@/api/client";
import { cookies } from "next/headers";

export const dynamic = "force-dynamic";

export default async function CursosPage() {
  const token = (await cookies()).get("auth_token")?.value;
  if (!token) return <div>No autenticado</div>;

  const courses = await coursesApi.list(token);

  return <CourseTable initialCourses={courses.items} total={courses.total} />;
}
```

## Testing Strategy

### Backend (pytest)

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `CreateCourseUseCase` — validation errors, duplicate check | Mock `CourseRepository`, assert exceptions |
| Unit | `ManageEnrollmentUseCase.enroll_students` — dedup logic | Mock repo, verify only new IDs are created |
| Unit | `ManageEnrollmentUseCase.delete_course` — cascade | Mock repo, verify 3 soft delete calls |
| Integration | Course CRUD endpoints | TestClient + test DB, full request/response cycle |
| Integration | Enrollment endpoints | Create course → enroll → verify → unenroll → verify |
| Integration | `?role=student\|professor` filter | Seed roles, create users, assert filtered response |
| Integration | Duplicate school_year + period | POST same combo twice, assert 400 |

### Frontend (Vitest + Playwright)

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `CourseTable` rendering | Render with mock data, assert table rows |
| Unit | `CourseForm` validation | Form states, required fields |
| Unit | `MultiSelect` search/filter | Type in search, assert filtered options |
| Integration | Server Actions | Mock API calls, assert revalidatePath/redirect |
| E2E | Full create course flow | Playwright: navigate to cursos → create → assert in list |
| E2E | Enroll/unenroll student | Playwright: detail page → enroll → assert → unenroll |

## Migration / Rollout

No migration required. Todos los modelos (`Course`, `CourseEnrollment`, `CourseProfessor`) ya existen en la base de datos con `deleted_at`/`is_deleted` heredados de `Base`.

### Rollout Order

1. **Backend**: Deploy nuevos archivos (no rompe nada existente porque son nuevos endpoints)
2. **API Client**: Regenerar o actualizar manualmente `api/client.ts` con `coursesApi`
3. **Frontend**: Deploy sidebar + páginas nuevas
4. **OpenAPI Spec**: Actualizar `packages/api-contract/openapi.json`

### Rollback

- Remover imports de `course_management_router` en `course/api/v1/router.py`
- Eliminar archivos nuevos de management
- Revertir `app-sidebar.tsx`
- Eliminar rutas `cursos/` del frontend

## Open Questions

- [ ] El `CourseEnrollment.student_id` apunta a `students.id` (tabla students) — confirmar que `Student.id` es UUID y mapea 1:1 con `User.id` para poder traer nombre/email desde el User
- [ ] El `CourseProfessor.professor_id` apunta a `professors.id` — misma pregunta sobre el mapping con User
- [ ] Confirmar que los endpoints de reports existentes (`GET /courses/{course_id}/metrics`) no entren en conflicto con los nuevos (`GET /courses/{course_id}`) — revisar orden de inclusión en router.py
