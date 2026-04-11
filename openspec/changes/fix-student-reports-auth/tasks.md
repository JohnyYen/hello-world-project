# Tasks: Fix Student Reports Auth

## Phase 1: Infrastructure

### 1.1 Verify API URL configuration
- Check `apps/frontend/.env` for `NEXT_PUBLIC_API_URL`
- Ensure it matches the Docker backend port (8010)

### 1.2 Identify auth token mechanism
- Review how other hooks get auth tokens
- Check if httpOnly cookies or localStorage is used
- Find the shared auth utility (if any)

## Phase 2: Implementation

### 2.1 Update useStudentReports hook
- File: `apps/frontend/src/hooks/use-student-reports.ts`
- Add `credentials: "include"` to fetch options
- Add `Authorization` header with Bearer token
- Handle 401 redirect case

### 2.2 Fix backend usecase null safety
- File: `apps/backend/src/statistic/application/usecase/get_student_progress_usecase.py`
- Add null check for `p.created_at` in `_calculate_progress_over_time`
- Add null check for `p.segment_level_id` in `_calculate_activity_distribution`
- Ensure `level_name` always produces a valid string

### 2.3 Update Pydantic schemas if needed
- File: `apps/backend/src/statistic/api/v1/schemas/student_progress.py`
- Make `date` field Optional in `ProgressOverTimeItem` if created_at can be null
- Add default fallback values

## Phase 3: Testing

### 3.1 Test with Playwright
- Login as testprofessor2026
- Navigate to a student reports page
- Verify KPIs, charts, and data load successfully

### 3.2 Test error cases
- Navigate to reports with non-existent student ID
- Verify proper error message is shown
