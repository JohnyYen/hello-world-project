# Spec: Student Reports Authentication

## Requirement
The student reports page MUST load data successfully when accessed by an authenticated professor or admin user.

## Scenarios

### Scenario 1: Authenticated professor views student reports
- **Given** A professor is logged in with valid credentials
- **And** The professor navigates to `/dashboard/students/{student_id}/reports`
- **When** The page loads
- **Then** The `useStudentReports` hook SHALL send the auth token with the API request
- **And** The backend SHALL return 200 OK with student progress data
- **And** The frontend SHALL display KPIs, charts, and activity distribution

### Scenario 2: Unauthenticated user attempts to view reports
- **Given** No user is logged in (no auth token)
- **When** A request is made to `/api/v1/statistic/students/{id}/progress`
- **Then** The backend SHALL return 401 Unauthorized
- **And** The frontend SHALL redirect to login or show "No autorizado"

### Scenario 3: Student has no progress data
- **Given** A student exists in the database
- **And** The student has no progress records
- **When** The reports page is loaded
- **Then** The backend SHALL return 200 OK with empty arrays
- **And** `progress_over_time`, `level_performance`, and `activity_distribution` SHALL be empty lists
- **And** `kpis` SHALL have zero values

### Scenario 4: Invalid student ID
- **Given** An invalid UUID is used as student_id
- **When** A request is made to `/api/v1/statistic/students/{invalid_id}/progress`
- **Then** The backend SHALL return 400 Bad Request or 404 Not Found
- **And** The frontend SHALL show "No se encontró progreso para este estudiante"

## Non-Functional Requirements
- The auth token MUST be sent via the same mechanism used by other frontend hooks
- The API URL MUST be configurable via `NEXT_PUBLIC_API_URL` environment variable
- Schema fields that could be None MUST be marked as `Optional` in Pydantic
