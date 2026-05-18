## Exploration: Professor Course Management

### Current State

The project has a **partial course domain** with gaps. Backend has Course, CourseEnrollment, and CourseProfessor models with UUID PKs, along with a CourseRepository and a reports-focused usecase. Frontend has course-related code only for **reports** (multi-selector, KPIs, metrics) and a school_year filter in the students table.

**Critical gap: no CRUD API for courses and no enrollment endpoint.** Courses and enrollments are only created via seed scripts. No UI exists to create courses, edit them, or assign students to them.

### Affected Areas

- `apps/backend/src/course/domain/course.py` — Course model (exists, needs no changes)
- `apps/backend/src/course/domain/course_enrollment.py` — Enrollment model (exists)
- `apps/backend/src/course/domain/course_professor.py` — Professor-course model (exists, unused)
- `apps/backend/src/course/infrastructure/course_repository.py` — Repository (exists, needs CRUD methods)
- `apps/backend/src/course/application/usecase/` — **MISSING**: course CRUD usecases
- `apps/backend/src/course/api/v1/endpoints/` — Only course_reports.py exists; **MISSING**: course CRUD + enrollment endpoints
- `apps/backend/src/course/api/v1/schemas/` — Only course_report.py exists; **MISSING**: course create/update schemas
- `apps/backend/src/users/api/v1/endpoints/list_students.py` — List students with course filter (exists)
- `apps/frontend/src/components/student/` — Student table has course (school_year) filter
- `apps/frontend/src/components/reports/` — Course reports UI exists
- `apps/frontend/src/app/dashboard/` — **MISSING**: course management pages
- `apps/frontend/src/types/course-report.interface.ts` — Course types exist (report-focused)

### Approaches

1. **Full course CRUD + enrollment + UI** — Build everything: backend CRUD endpoints for courses, enrollment/unenrollment endpoint, and full frontend pages for course listing, creation, editing, and student assignment.
   - Pros: Complete feature, covers real professor workflow
   - Cons: Larger effort, more risk
   - Effort: High

2. **Backend CRUD + bare enrollment endpoint, frontend only course list + student assignment via existing student page** — Backend: POST/PUT/DELETE courses, POST enrollment. Frontend: minimal course management page, integrate enrollment into existing student detail page.
   - Pros: Faster delivery, leverages existing UI patterns
   - Cons: Less polished UX, might need refinement
   - Effort: Medium

3. **Minimal — only backend API, no frontend** — Build all API endpoints for courses and enrollment, defer UI to subsequent change.
   - Pros: Fastest to ship API, enables mobile/game integration
   - Cons: No professor-facing UI, incomplete user story
   - Effort: Low

### Recommendation

**Approach 2** — Backend CRUD + enrollment endpoint + minimal frontend. The student list page already has a course filter and create-student flow. Extend the student creation dialog and student detail page to support course assignment. Create a dedicated course management page for listing/creating/editing courses. This aligns with the existing UI patterns (dashboard layout, shadcn components) and the existing architecture (Service/UseCase pattern).

### Risks

- **Database migration needed**: The Course model already exists but may need schema adjustments (UUID FK references must be consistent with existing tables)
- **CourseProfessor model is unused**: Need to decide if we expose professor-course assignment or defer it
- **Seed data dependency**: Existing seed scripts create courses and enrollments — they must be updated/validated after changes
- **List students endpoint** already filters by course_id and school_year — good sign, but need to verify it works correctly with the enrollment flow
- **No existing test coverage** for course endpoints

### Ready for Proposal

Yes. The scope is well understood. Recommend proceeding to proposal with approach 2.
