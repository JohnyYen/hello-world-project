# Fix Student Reports Authentication

## Problem
The student reports page (`/dashboard/students/{id}/reports`) shows "Error al cargar los datos del reporte" because the frontend hook `useStudentReports` does not send the authentication token to the backend API.

## Root Cause Analysis

### Backend
- The `/api/v1/statistic` router has `dependencies=[Depends(HTTPBearer())]` at the router level
- ALL endpoints under `/statistic` require Bearer token authentication
- `GET /statistic/students/{id}/progress` returns 403 when no token is provided

### Frontend
- `useStudentReports` hook calls `fetch()` without `Authorization` header
- The hook has no access to the user's auth token
- Error message is generic: "Error al cargar los datos del reporte"

### Secondary Issue
- `API_BASE_URL` defaults to `http://localhost:8000` but the Docker backend runs on port `8010`
- This is configured via `NEXT_PUBLIC_API_URL` env var

## Solution

### 1. Frontend: Add auth token to useStudentReports hook
- Import and use the same auth token mechanism as other hooks
- Add `Authorization: Bearer <token>` header to the fetch call
- Use cookies (httpOnly) or localStorage depending on project auth strategy

### 2. Backend: Verify StudentProgressResponse schema handles None values
- The Pydantic error `Input should be a valid string` suggests some field could be None
- Review `_calculate_level_performance` and `_calculate_activity_distribution` methods
- Ensure `level_name` and `game_name` never return None

## Affected Files
- `apps/frontend/src/hooks/use-student-reports.ts`
- `apps/backend/src/statistic/application/usecase/get_student_progress_usecase.py`
- `apps/backend/src/statistic/api/v1/schemas/student_progress.py` (if schema changes needed)

## Rollback Plan
- Revert the hook changes if auth mechanism conflicts arise
- The backend schema change is backward compatible (making fields Optional)
