# Courses API Specification

## Purpose

This specification defines the Course Management REST API — a full CRUD layer plus enrollment management on top of existing `Course`, `CourseEnrollment`, and `CourseProfessor` domain models. The API follows Clean Architecture (Service + UseCase pattern), uses soft delete with cascade, and integrates with the existing reports router under a shared prefix.

## Requirements

### Requirement: Course CRUD — List Courses

The system MUST provide a `GET /api/v1/courses/` endpoint that returns a paginated list of courses with student count and assigned professor IDs.

The response SHOULD include pagination metadata (`skip`, `limit`, `total`).

The system MUST exclude soft-deleted courses from the list.

#### Scenario: List all active courses

- GIVEN there are 5 courses in the database (none deleted)
- WHEN a GET request is sent to `/api/v1/courses/`
- THEN the response status is 200
- AND the response body contains a list of courses
- AND each course includes `id`, `name`, `schoolYear`, `periodLabel`, `studentCount`, `professorIds`
- AND soft-deleted courses are NOT included

#### Scenario: List courses with pagination

- GIVEN there are 25 courses in the database
- WHEN a GET request is sent to `/api/v1/courses/?skip=0&limit=10`
- THEN the response status is 200
- AND exactly 10 courses are returned
- AND pagination metadata `total` equals 25

#### Scenario: Empty course list

- GIVEN there are no courses in the database
- WHEN a GET request is sent to `/api/v1/courses/`
- THEN the response status is 200
- AND the response body contains an empty list

---

### Requirement: Course CRUD — Create Course

The system MUST provide a `POST /api/v1/courses/` endpoint that creates a course with optional student and professor assignments in a single transactional operation.

The request body MUST accept: `name`, `description`, `schoolYear`, `periodLabel`, `startDate`, `endDate`, `studentIds` (optional), `professorIds` (optional).

The system MUST validate that all provided `studentIds` and `professorIds` reference existing users.

The system MUST reject creation if a course with the same `schoolYear` and `periodLabel` already exists (not soft-deleted).

#### Scenario: Create course with assignments

- GIVEN valid course data and 3 existing student IDs and 2 existing professor IDs
- WHEN a POST request is sent to `/api/v1/courses/` with the course data, `studentIds`, and `professorIds`
- THEN the response status is 201
- AND a `Course` record is created in the database
- AND 3 `CourseEnrollment` records are created for the student IDs
- AND 2 `CourseProfessor` records are created for the professor IDs
- AND the response body includes the created course with `studentCount` = 3 and `professorIds` with 2 entries

#### Scenario: Create course without assignments

- GIVEN valid course data
- WHEN a POST request is sent to `/api/v1/courses/` without `studentIds` and `professorIds`
- THEN the response status is 201
- AND the course is created
- AND `studentCount` is 0
- AND `professorIds` is an empty list

#### Scenario: Reject duplicate schoolYear + periodLabel

- GIVEN a course with `schoolYear="2025-2026"` and `periodLabel="Semestre 1"` already exists
- WHEN a POST request is sent with the same `schoolYear` and `periodLabel`
- THEN the response status is 409
- AND the error message indicates the course already exists for that period

#### Scenario: Reject non-existent student IDs

- GIVEN a valid course payload with `studentIds: ["non-existent-uuid"]`
- WHEN a POST request is sent
- THEN the response status is 422
- AND the error message lists the invalid student IDs

#### Scenario: Reject invalid input data

- GIVEN course data with `name` exceeding 100 characters
- WHEN a POST request is sent
- THEN the response status is 422
- AND the validation error indicates the field violation

---

### Requirement: Course CRUD — Get Course Detail

The system MUST provide a `GET /api/v1/courses/{course_id}` endpoint that returns full course detail including assigned students and professors.

#### Scenario: Get existing course

- GIVEN a course with 2 enrolled students and 1 professor
- WHEN a GET request is sent to `/api/v1/courses/{course_id}`
- THEN the response status is 200
- AND the response includes the course fields plus `students` (array of `{id, name}`) and `professors` (array of `{id, name}`)

#### Scenario: Get non-existent course

- GIVEN a course ID that does not exist
- WHEN a GET request is sent to `/api/v1/courses/{non-existent-id}`
- THEN the response status is 404
- AND the error message indicates the course was not found

#### Scenario: Get soft-deleted course

- GIVEN a course that has been soft-deleted
- WHEN a GET request is sent to `/api/v1/courses/{course_id}`
- THEN the response status is 404
- AND the course is not returned

---

### Requirement: Course CRUD — Update Course

The system MUST provide a `PUT /api/v1/courses/{course_id}` endpoint that updates course fields and synchronizes student/professor assignments.

When `studentIds` or `professorIds` are provided, the system MUST perform a full sync: add new assignments, remove assignments not in the list.

The system MUST reject update if the new `schoolYear` + `periodLabel` combination conflicts with another existing course.

#### Scenario: Update course fields and assignments

- GIVEN a course with 3 students and 1 professor
- WHEN a PUT request is sent with updated `name` and `studentIds: [only 2 of the 3]`
- THEN the response status is 200
- AND the course `name` is updated
- AND only 2 students remain enrolled (the third is unenrolled)
- AND professor assignments are unchanged

#### Scenario: Update with empty assignments

- GIVEN a course with 3 enrolled students
- WHEN a PUT request is sent with `studentIds: []`
- THEN the response status is 200
- AND all students are unenrolled
- AND `studentCount` is 0

#### Scenario: Update non-existent course

- GIVEN a course ID that does not exist
- WHEN a PUT request is sent to `/api/v1/courses/{non-existent-id}`
- THEN the response status is 404

---

### Requirement: Course CRUD — Delete Course (Soft Delete)

The system MUST provide a `DELETE /api/v1/courses/{course_id}` endpoint that performs soft delete by setting `is_deleted = True`.

The system MUST cascade the soft delete to all related `CourseEnrollment` and `CourseProfessor` records.

#### Scenario: Soft delete course with enrollments

- GIVEN a course with 3 enrolled students and 2 professors
- WHEN a DELETE request is sent to `/api/v1/courses/{course_id}`
- THEN the response status is 204
- AND `Course.is_deleted` is `True`
- AND all related `CourseEnrollment` records are soft-deleted
- AND all related `CourseProfessor` records are soft-deleted

#### Scenario: Delete non-existent course

- GIVEN a course ID that does not exist
- WHEN a DELETE request is sent
- THEN the response status is 404

#### Scenario: Delete already deleted course

- GIVEN a course that is already soft-deleted
- WHEN a DELETE request is sent
- THEN the response status is 404

---

### Requirement: Enrollment Management — List Enrolled Students

The system MUST provide a `GET /api/v1/courses/{course_id}/students` endpoint that returns the list of enrolled students for a course.

#### Scenario: List enrolled students

- GIVEN a course with 3 enrolled students
- WHEN a GET request is sent to `/api/v1/courses/{course_id}/students`
- THEN the response status is 200
- AND the response body contains 3 student objects with `id`, `firstName`, `lastName`, `email`, `enrolledAt`

#### Scenario: List students for non-existent course

- GIVEN a course ID that does not exist
- WHEN a GET request is sent to `/api/v1/courses/{non-existent-id}/students`
- THEN the response status is 404

---

### Requirement: Enrollment Management — Enroll Student(s)

The system MUST provide a `POST /api/v1/courses/{course_id}/students` endpoint that enrolls one or more students to a course.

The endpoint MUST accept `studentIds` (array of UUIDs).

The system MUST reject enrollment if the student is already enrolled.

The system MUST reject enrollment if the student ID does not exist.

The system MUST reject enrollment if the course is soft-deleted.

#### Scenario: Enroll single student

- GIVEN a course with 0 students and a valid student ID
- WHEN a POST request is sent to `/api/v1/courses/{course_id}/students` with `studentIds: [valid-student-id]`
- THEN the response status is 200
- AND a `CourseEnrollment` record is created
- AND the response includes the updated list of enrolled students (count = 1)

#### Scenario: Enroll multiple students

- GIVEN a course with 0 students and 3 valid student IDs
- WHEN a POST request is sent with 3 student IDs
- THEN the response status is 200
- AND 3 `CourseEnrollment` records are created

#### Scenario: Reject duplicate enrollment

- GIVEN a course with student A already enrolled
- WHEN a POST request is sent with `studentIds: [student-A-id]`
- THEN the response status is 409
- AND the error indicates the student is already enrolled

#### Scenario: Reject enrollment in deleted course

- GIVEN a soft-deleted course
- WHEN a POST request is sent with a valid student ID
- THEN the response status is 404

---

### Requirement: Enrollment Management — Unenroll Student

The system MUST provide a `DELETE /api/v1/courses/{course_id}/students/{student_id}` endpoint that removes a student's enrollment.

#### Scenario: Unenroll enrolled student

- GIVEN a course with student A enrolled
- WHEN a DELETE request is sent to `/api/v1/courses/{course_id}/students/{student-A-id}`
- THEN the response status is 204
- AND the `CourseEnrollment` record is deleted
- AND the student no longer appears in the enrolled list

#### Scenario: Unenroll non-enrolled student

- GIVEN a course where student A is NOT enrolled
- WHEN a DELETE request is sent
- THEN the response status is 404

#### Scenario: Unenroll from non-existent course

- GIVEN a non-existent course ID
- WHEN a DELETE request is sent
- THEN the response status is 404

---

### Requirement: User Filtering by Role

The system MUST extend the existing users list endpoint (or create a new one) to support `?role=student` and `?role=professor` query parameters.

The result MUST respect the same pagination and auth requirements as the existing endpoint.

#### Scenario: Filter students by role

- GIVEN the database has 10 students and 5 professors
- WHEN a GET request is sent to `/api/v1/users/?role=student`
- THEN the response status is 200
- AND exactly 10 users are returned
- AND all returned users have the role `student`

#### Scenario: Filter professors by role

- GIVEN the database has 10 students and 5 professors
- WHEN a GET request is sent to `/api/v1/users/?role=professor`
- THEN the response status is 200
- AND exactly 5 users are returned
- AND all returned users have the role `professor`

#### Scenario: Invalid role parameter

- GIVEN a GET request to `/api/v1/users/?role=invalid`
- WHEN the request is processed
- THEN the response status is 422
- AND the error indicates the role value is invalid

#### Scenario: No role filter (return all)

- GIVEN the existing users endpoint returns all users
- WHEN a GET request is sent to `/api/v1/users/` without `role`
- THEN the response status is 200
- AND all users are returned (backward compatible)

---

### Requirement: Clean Architecture — Service Layer

The system MUST implement a `CourseService` class that encapsulates all CRUD operations on courses.

The `CourseService` MUST extend or compose with `BaseService`.

The `CourseService` MUST handle:
- Validation of duplicate `schoolYear` + `periodLabel`
- Soft delete cascade logic
- Assignment synchronization on create/update

The `CourseService` MUST raise domain-specific exceptions (e.g., `CourseNotFoundError`, `DuplicateCoursePeriodError`, `StudentNotFoundError`).

#### Scenario: Service validates duplicate period

- GIVEN an existing course with `schoolYear="2025-2026"` and `periodLabel="Semestre 1"`
- WHEN `CourseService.create()` is called with the same combination
- THEN a `DuplicateCoursePeriodError` is raised
- AND no course is created in the database

#### Scenario: Service cascades soft delete

- GIVEN a course with 3 enrollments and 2 professor assignments
- WHEN `CourseService.soft_delete()` is called
- THEN `Course.is_deleted` is set to `True`
- AND all related `CourseEnrollment` records have `is_deleted = True`
- AND all related `CourseProfessor` records have `is_deleted = True`

---

### Requirement: Clean Architecture — UseCase Layer

The system MUST implement UseCase classes for operations that involve multi-entity orchestration:
- `CreateCourseUseCase` — orchestrates course creation + assignments in a transaction
- `UpdateCourseUseCase` — orchestrates course update + assignment sync in a transaction
- `ManageEnrollmentUseCase` — handles enroll/unenroll operations with validation

Each UseCase MUST accept necessary repositories/services via dependency injection.

#### Scenario: CreateCourseUseCase creates course with nested assignments

- GIVEN valid course data, student IDs, and professor IDs
- WHEN `CreateCourseUseCase.execute()` is called
- THEN a new Course is created
- AND the course is linked to all provided students and professors
- AND all operations succeed or none succeed (transactional)

#### Scenario: ManageEnrollmentUseCase prevents duplicate enrollment

- GIVEN an existing enrollment for student A in course X
- WHEN `ManageEnrollmentUseCase.enroll()` is called with course X and student A
- THEN an error is raised
- AND no duplicate enrollment record is created

---

### Requirement: Router Structure

The system MUST create a new router module at `src/course/api/v1/routers/course_management.py` (separate from the existing reports router).

The main course router MUST include both sub-routers (reports + management) under the shared prefix `/api/v1/courses`.

All management endpoints MUST require JWT authentication via `HTTPBearer`.

#### Scenario: Management router is isolated from reports router

- GIVEN the course router includes both sub-routers
- WHEN a request hits `GET /api/v1/courses/` (management list)
- THEN it is handled by the management router
- AND the reports router's `GET /api/v1/courses/reports/kpis` still works unchanged

---

### Requirement: Pydantic Schemas

The system MUST define Pydantic v2 schemas for all request/response types in a new file `src/course/api/v1/schemas/course_management.py`.

Request schemas MUST use `model_config = {"from_attributes": True, "populate_by_name": True}`.

Response schemas MUST use camelCase field aliases for API consistency.

#### Scenario: Create course request schema validates required fields

- GIVEN a JSON payload missing `name`
- WHEN Pydantic validation runs
- THEN a validation error is raised for the missing required field `name`

#### Scenario: Response uses camelCase aliases

- GIVEN a course created with `school_year="2025-2026"`
- WHEN the API response is serialized
- THEN the JSON uses `schoolYear` (camelCase) instead of `school_year`

---

### Requirement: Course Repository — Extended Methods

The system MUST extend `CourseRepository` with the following methods:
- `create_with_assignments(data, student_ids, professor_ids)` — transactional creation with enrollments and professor assignments
- `get_by_id_with_relations(id)` — eager loads enrollments and course_professors relationships
- `soft_delete_cascade(id)` — soft-deletes course + all related enrollments and professor assignments
- `sync_students(course_id, student_ids)` — synchronizes student enrollments (add/remove)
- `sync_professors(course_id, professor_ids)` — synchronizes professor assignments (add/remove)

#### Scenario: Repository creates course with assignments transactionally

- GIVEN valid course data, 2 student IDs, and 1 professor ID
- WHEN `create_with_assignments()` is called
- THEN a single database transaction creates the course, 2 enrollments, and 1 professor assignment
- AND if any part fails, the entire operation is rolled back

#### Scenario: Repository syncs students (adds new, removes old)

- GIVEN a course with enrollments for students [A, B]
- WHEN `sync_students()` is called with `student_ids = [B, C]`
- THEN student A is unenrolled
- AND student C is enrolled
- AND student B remains enrolled

---

## Acceptance Criteria

- [ ] `GET /api/v1/courses/` returns paginated course list with student count and professor IDs
- [ ] `POST /api/v1/courses/` creates course with/without student+professor assignments (transactional)
- [ ] `GET /api/v1/courses/{id}` returns full detail with students and professors
- [ ] `PUT /api/v1/courses/{id}` updates fields and synchronizes assignments
- [ ] `DELETE /api/v1/courses/{id}` soft-deletes course and cascades to enrollments and professor assignments
- [ ] `GET /api/v1/courses/{id}/students` lists enrolled students
- [ ] `POST /api/v1/courses/{id}/students` enrolls one or more students (rejects duplicates)
- [ ] `DELETE /api/v1/courses/{id}/students/{student_id}` unenrolls a student
- [ ] `GET /api/v1/users/?role=student` filters by student role
- [ ] `GET /api/v1/users/?role=professor` filters by professor role
- [ ] `?role=invalid` returns 422
- [ ] Duplicate `schoolYear` + `periodLabel` rejected with 409
- [ ] All endpoints require JWT auth
- [ ] Soft delete cascade is verified
- [ ] CourseService and UseCases follow Clean Architecture pattern
- [ ] Pydantic schemas use camelCase aliases in responses
- [ ] Router is separate from reports router (backward compatible)
