# Tasks: Professor Course Management

## Phase 1: Backend Infrastructure

### 1.1 Repository — Add `get_by_id_with_relations` — ✅ DONE

Extend `apps/backend/src/course/infrastructure/course_repository.py` with method that eager-loads `Course.enrollments` (with `CourseEnrollment.student`) and `Course.course_professors` (with `CourseProfessor.professor`) using `selectinload`, filtering by `Course.deleted_at.is_(None)`.

### 1.2 Repository — Add `bulk_create_enrollments` and `bulk_create_professors` — ✅ DONE

Add batch insert methods to `course_repository.py`:
- `bulk_create_enrollments(course_id, student_ids)` — creates `CourseEnrollment` objects, `db.add_all()`, `await db.flush()`
- `bulk_create_professors(course_id, professor_ids)` — creates `CourseProfessor` objects, `db.add_all()`, `await db.flush()`

### 1.3 Repository — Add soft delete cascade methods — ✅ DONE

Add to `course_repository.py`:
- `soft_delete_enrollments_for_course(course_id)` — bulk `UPDATE course_enrollments SET deleted_at=now(), is_deleted=True`
- `soft_delete_professors_for_course(course_id)` — bulk `UPDATE course_professors SET deleted_at=now(), is_deleted=True`
- `soft_delete_course(course_id)` — single `UPDATE courses SET deleted_at=now(), is_deleted=True` (can use existing `BaseRepository.delete()`)

### 1.4 Repository — Add assignment query methods — ✅ DONE

Add to `course_repository.py`:
- `get_students_for_course(course_id)` — join `CourseEnrollment` + `User` via `Student.user_id`, return list of dicts with student_id, name, email, enrolled_at
- `get_professors_for_course(course_id)` — join `CourseProfessor` + `User` via `Professor.user_id`, return list of dicts with professor_id, name, email
- `get_existing_enrollment_ids(course_id)` — returns set of student_ids currently enrolled (for dedup/sync)

### 1.5 Repository — Add assignment sync methods — ✅ DONE

Add to `course_repository.py`:
- `sync_students(course_id, student_ids)` — diff current enrollments vs provided list: bulk create new, bulk soft-delete removed
- `sync_professors(course_id, professor_ids)` — diff current assignments vs provided list: bulk create new, bulk soft-delete removed

### 1.6 Pydantic Schemas — Create `course_management.py` — ✅ DONE

Create `apps/backend/src/course/api/v1/schemas/course_management.py` with:
- `CourseCreateRequest` — name (required), description (opt), schoolYear (required), periodLabel (required), startDate (required), endDate (required), studentIds (opt list UUID), professorIds (opt list UUID). `model_config = {"populate_by_name": True}`
- `CourseUpdateRequest` — all fields optional, isActive optional
- `EnrollmentRequest` — studentIds (list UUID, required)
- `CourseResponse` — id, name, description, schoolYear, periodLabel, startDate, endDate, isActive, studentCount, professorCount, createdAt, updatedAt. `model_config = {"from_attributes": True, "populate_by_name": True}`
- `CourseDetailResponse(CourseResponse)` — adds students `list[StudentEnrollmentResponse]`, professors `list[ProfessorAssignmentResponse]`
- `StudentEnrollmentResponse` — studentId, name, email, enrolledAt
- `ProfessorAssignmentResponse` — professorId, name, email
- `PaginatedCourseListResponse` — items, total, skip, limit

### 1.7 Service — Create `CourseService` — ✅ DONE

Create `apps/backend/src/course/application/service/course_service.py` extending `BaseService[Course]`:
- `__init__(self, repository: CourseRepository)` calling `super().__init__(repository, Course)`
- `list_courses(skip, limit)` using `self.get_all()` with `order_by="school_year"` + descending
- `get_course_with_relations(course_id)` → delegates to repo `get_by_id_with_relations`

### 1.8 UseCase — Create `CreateCourseUseCase` — ✅ DONE

Create `apps/backend/src/course/application/usecase/create_course_usecase.py`:
- Constructor accepts `db: AsyncSession`, `course_repo: CourseRepository`
- `execute(request: CourseCreateRequest)` → validate duplicate `school_year` + `period_label`, then `async with db.begin():` create course, bulk enroll students, bulk assign professors. Return `CourseDetailResponse` with populated relations

### 1.9 UseCase — Create `UpdateCourseUseCase` — ✅ DONE

Create `apps/backend/src/course/application/usecase/update_course_usecase.py`:
- Constructor accepts `db: AsyncSession`, `course_repo: CourseRepository`
- `execute(course_id, request: CourseUpdateRequest)` → validate course exists, validate no duplicate period conflict (if school_year/period_label changed), then `async with db.begin():` update course fields, sync students if provided, sync professors if provided. Return `CourseDetailResponse`

### 1.10 UseCase — Create `ManageEnrollmentUseCase` — ✅ DONE

Create `apps/backend/src/course/application/usecase/manage_enrollment_usecase.py`:
- Constructor accepts `db: AsyncSession`, `course_repo: CourseRepository`
- `enroll_students(course_id, student_ids)` → validate course exists, filter already-enrolled IDs, `async with db.begin():` bulk_create_enrollments for new IDs. Return updated student list
- `unenroll_student(course_id, student_id)` → soft_delete_enrollment. Return success bool
- `delete_course(course_id)` → soft delete cascade: enrollments → professors → course in single transaction. Return success bool

### 1.11 UseCase — Create `ListUsersByRoleUseCase` — ✅ DONE

Create `apps/backend/src/users/application/usecase/list_users_by_role_usecase.py`:
- Constructor accepts `db: AsyncSession`, `user_repo: UserRepository` (or use generic)
- `execute(role, skip, limit)` → query `User` filtered by `User.role_name == role`, with proper eager loading, excluding soft-deleted. Return `UserListResponse` (reuse existing schema)

## Phase 2: Backend Endpoints

### 2.1 Endpoint — Create `course_management.py` router — ✅ DONE

Create `apps/backend/src/course/api/v1/endpoints/course_management.py` with:
- `APIRouter(prefix="/courses", tags=["Course Management"], dependencies=[Depends(HTTPBearer())])`
- `GET /courses/management` (list) → `CourseService.list_courses_with_counts()` → `PaginatedCourseListResponse`
- `POST /courses/management` (create) → `CreateCourseUseCase.execute()` → `CourseDetailResponse`, status 201
- `GET /courses/{course_id}` (detail) → `CreateCourseUseCase._build_detail_response()` → `CourseDetailResponse`
- `PUT /courses/{course_id}` (update) → `UpdateCourseUseCase.execute()` → `CourseDetailResponse`
- `DELETE /courses/{course_id}` (delete) → `ManageEnrollmentUseCase.delete_course()` → 204
- `GET /courses/{course_id}/students` (list enrolled) → `ManageEnrollmentUseCase.get_students()`
- `POST /courses/{course_id}/students` (enroll) → `ManageEnrollmentUseCase.enroll_students()`
- `DELETE /courses/{course_id}/students/{student_id}` (unenroll) → `ManageEnrollmentUseCase.unenroll_student()` → 204

### 2.2 Endpoint — Create `get_users_by_role.py` — ✅ DONE

Create `apps/backend/src/users/api/v1/endpoints/get_users_by_role.py`:
- `APIRouter()` (no prefix, sub-router will be mounted under `/users`)
- `GET /by-role` with query param `role: str = Query(..., pattern="^(student|professor)$")` → delegates to `ListUsersByRoleUseCase`

### 2.3 Router — Integrate course management sub-router — ✅ DONE

Modify `apps/backend/src/course/api/v1/router.py` to include `course_management_router` AFTER `course_reports_router`:
```python
from src.course.api.v1.endpoints.course_management import router as course_management_router
router.include_router(course_management_router)
```

### 2.4 Router — Integrate users by-role endpoint — ✅ DONE

Modify `apps/backend/src/users/api/v1/router.py` to include `get_users_by_role_router`:
```python
from src.users.api.v1.endpoints.get_users_by_role import router as get_users_by_role_router
router.include_router(get_users_by_role_router)
```

## Phase 3: Frontend Infrastructure — ✅ DONE

### 3.1 Types — Create `course.interface.ts` — ✅ DONE

Create `apps/frontend/src/types/course.interface.ts` with interfaces:
- `Course` — id, name, description, schoolYear, periodLabel, startDate, endDate, isActive, studentCount, professorCount, createdAt, updatedAt
- `CourseDetail extends Course` — students (StudentEnrollment[]), professors (ProfessorAssignment[])
- `StudentEnrollment` — studentId, name, email, enrolledAt
- `ProfessorAssignment` — professorId, name, email
- `CourseCreate`, `CourseUpdate`, `EnrollmentRequest`, `PaginatedCourseList`

### 3.2 API Client — Add `coursesApi` to `client.ts` — ✅ DONE

Extend `apps/frontend/src/api/client.ts` with `coursesApi` object containing methods:
- `list(token, skip, limit)` → `GET /api/v1/courses/`
- `getById(courseId, token)` → `GET /api/v1/courses/{courseId}`
- `create(body, token)` → `POST /api/v1/courses/`
- `update(courseId, body, token)` → `PUT /api/v1/courses/{courseId}`
- `delete(courseId, token)` → `DELETE /api/v1/courses/{courseId}`
- `getStudents(courseId, token)` → `GET /api/v1/courses/{courseId}/students`
- `enrollStudents(courseId, body, token)` → `POST /api/v1/courses/{courseId}/students`
- `unenrollStudent(courseId, studentId, token)` → `DELETE /api/v1/courses/{courseId}/students/{studentId}`
- `listByRole(role, token)` → `GET /api/v1/users/by-role?role={role}`

### 3.3 Service — Create `courses.ts` service — ✅ DONE

Create `apps/frontend/src/services/courses.ts` following the existing service pattern (e.g., `services/games.ts`):
- `getCourses(token, skip?, limit?)` → wraps `coursesApi.list()`
- `getCourse(courseId, token)` → wraps `coursesApi.getById()`
- `createCourse(body, token)` → wraps `coursesApi.create()`
- `updateCourse(courseId, body, token)` → wraps `coursesApi.update()`
- `deleteCourse(courseId, token)` → wraps `coursesApi.delete()`
- `getStudentsByRole(role, token)` → wraps `coursesApi.listByRole()`

### 3.4 Server Actions — Create `actions.ts` — ✅ DONE

Create `apps/frontend/src/app/dashboard/cursos/actions.ts` with:
- `createCourse(formData: FormData)` — reads fields from FormData, builds body with parsed studentIds/professorIds, calls `coursesApi.create()`, revalidates path, redirects
- `deleteCourse(courseId: string)` — calls `coursesApi.delete()`, revalidates path
- `updateCourse(courseId: string, formData: FormData)` — reads fields, calls `coursesApi.update()`, revalidates, redirects
- `enrollStudents(courseId: string, studentIds: string[])` — calls `coursesApi.enrollStudents()`, revalidates
- `unenrollStudent(courseId: string, studentId: string)` — calls `coursesApi.unenrollStudent()`, revalidates
- All actions: `"use server"`, get token from `cookies()`, error handling with `try/catch`

### 3.5 Sidebar — Add "Cursos" nav item — ✅ DONE

Modify `apps/frontend/src/components/dashboard/app-sidebar.tsx`:
- Import `IconBookOpen` from `@tabler/icons-react`
- Add item `{ title: "Cursos", url: "/dashboard/cursos", icon: IconBookOpen }` in `navMain` array between "Estudiantes" and "Métricas"

### 3.6 Component — Create `UserMultiSelect` — ✅ DONE

Create `apps/frontend/src/components/cursos/user-multi-select.tsx`:
- Client Component using shadcn `Command` + `Popover`
- Props: `options: { id: string; label: string; subtitle?: string }[]`, `selected: string[]`, `onChange: (ids: string[]) => void`, `placeholder`, `searchPlaceholder`, `emptyMessage`
- Search input filters options, checkboxes for multi-selection, selected items shown as badges

### 3.7 Component — Create `CourseTable` — ✅ DONE

Create `apps/frontend/src/components/cursos/course-table.tsx`:
- Client Component
- Props: `initialCourses: Course[]`, `total: number`
- Renders shadcn `Table` with columns: Nombre, Año Escolar, Período, Estudiantes, Profesores, Acciones
- Acciones column: "Ver detalle" (Link), "Editar" (opens CourseForm in Dialog), "Eliminar" (confirm dialog → calls delete Server Action)
- "Crear Curso" button opens CourseForm in Dialog mode
- Empty state: "No hay cursos registrados" with prominent "Crear Curso" button
- Success/error toasts for all actions

### 3.8 Component — Create `CourseForm` — ✅ DONE

Create `apps/frontend/src/components/cursos/course-form.tsx`:
- Client Component using `useActionState`
- Props: `course?: CourseDetail` (for edit mode), `onSuccess?: () => void`
- Fields: Nombre del curso (text), Descripción (textarea), Año Escolar (text, YYYY-YYYY validation), Período (select: Semestre 1, Semestre 2, Anual, Trimestre 1-3), Fecha de inicio (date), Fecha de fin (date), Estudiantes (MultiSelect), Profesores (MultiSelect)
- Loads available students/professors via `coursesApi.listByRole()`
- Pre-populates fields when editing
- Zod validation: required fields, year format, end > start
- Submits via Server Action, displays field-level errors, success toast

### 3.9 Page — Create course list page — ✅ DONE

Create `apps/frontend/src/app/dashboard/cursos/page.tsx`:
- Server Component, `export const dynamic = 'force-dynamic'`
- Gets token from cookies, calls `coursesApi.list()`
- Renders `<CourseTable initialCourses={courses.items} total={courses.total} />`
- Follows same pattern as `students/page.tsx`

### 3.10 Page — Create course detail page — ✅ DONE

Create `apps/frontend/src/app/dashboard/cursos/[id]/page.tsx`:
- Server Component with `params: { id: string }`
- Gets token, calls `coursesApi.getById(id)`
- Renders course header (name, school year, period, dates, description)
- Renders enrolled students table (Nombre, Email, Fecha de inscripción, Desasignar button)
- "Asignar Estudiantes" button opens MultiSelect dialog
- "Volver" link to `/dashboard/cursos`
- 404 state: "Curso no encontrado" with "Volver a cursos" link

### 3.11 Page — Add `loading.tsx` and `error.tsx` — ✅ DONE

Create `apps/frontend/src/app/dashboard/cursos/loading.tsx` with skeleton UI — ✅ DONE
Create `apps/frontend/src/app/dashboard/cursos/error.tsx` with error boundary — ✅ DONE
Create `apps/frontend/src/app/dashboard/cursos/[id]/loading.tsx` with skeleton UI — ✅ DONE
Create `apps/frontend/src/app/dashboard/cursos/[id]/error.tsx` with error boundary — ✅ DONE

## Phase 4: Testing & Polish

### 4.1 Tests — CourseRepository unit tests

Create `apps/backend/tests/course/test_course_repository.py`:
- Test `get_by_id_with_relations` returns course with enrollments and professors loaded
- Test `bulk_create_enrollments` inserts N records
- Test `soft_delete_enrollments_for_course` sets deleted_at on all enrollments
- Test `sync_students` adds new, removes old, keeps existing

### 4.2 Tests — CreateCourseUseCase unit tests

Create `apps/backend/tests/course/test_create_course_usecase.py`:
- Test happy path: creates course + enrollments + professors
- Test duplicate school_year + period_label raises `DuplicateEntryException`
- Test empty student_ids creates course with 0 enrollments

### 4.3 Tests — ManageEnrollmentUseCase unit tests

Create `apps/backend/tests/course/test_manage_enrollment_usecase.py`:
- Test `enroll_students` deduplicates already-enrolled students
- Test `unenroll_student` soft-deletes enrollment
- Test `delete_course` cascade: enrollments + professors + course all soft-deleted
- Test `enroll_students` on non-existent course raises 404
- Test `delete_course` on already-deleted course raises 404

### 4.4 Tests — Course CRUD integration tests

Create `apps/backend/tests/course/test_course_management_api.py`:
- Test `POST /courses/` creates course successfully, returns 201
- Test `POST /courses/` with duplicate period returns 409
- Test `GET /courses/` returns paginated list with student/professor counts
- Test `GET /courses/{id}` returns full detail
- Test `PUT /courses/{id}` updates fields and syncs students
- Test `DELETE /courses/{id}` returns 204 and cascades soft delete
- Test `POST /courses/{id}/students` enrolls students
- Test `DELETE /courses/{id}/students/{sid}` unenrolls student
- Test `GET /courses/` (reports) still works unchanged (backward compat)

### 4.5 Tests — Users by-role endpoint tests

Create `apps/backend/tests/users/test_get_users_by_role.py`:
- Test `GET /users/by-role?role=student` returns only students
- Test `GET /users/by-role?role=professor` returns only professors
- Test `GET /users/by-role?role=invalid` returns 422

### 4.6 Frontend — Course list page rendering (Vitest)

Create `apps/frontend/tests/components/cursos/course-table.test.tsx`:
- Test renders table with course rows
- Test empty state shows "No hay cursos registrados"
- Test delete confirmation dialog opens

### 4.7 Frontend — CourseForm validation (Vitest)

Create `apps/frontend/tests/components/cursos/course-form.test.tsx`:
- Test required field validation errors
- Test school year format validation
- Test end date > start date validation

### 4.8 OpenAPI — Update contract spec

Modify `packages/api-contract/openapi.json` to include all new endpoints from Phase 2.
