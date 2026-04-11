# Technical Design: Fix Student Reports Auth

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│                                                              │
│  useStudentReports(studentId)                                │
│       │                                                      │
│       ├─ Gets auth token from cookie/localStorage            │
│       ├─ fetch(`/api/v1/statistic/students/${id}/progress`,  │
│       │     { headers: { Authorization: Bearer <token> } })  │
│       └─ Maps response to React state                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│                                                              │
│  Router: /statistic (HTTPBearer required)                   │
│       │                                                      │
│       ├─ student_progress.py (no explicit auth needed)       │
│       │    └─ GetStudentProgressUseCase.execute()            │
│       │         ├─ ProgressRepository.get_by_student_id()    │
│       │         ├─ _calculate_kpis()                         │
│       │         ├─ _calculate_progress_over_time()            │
│       │         ├─ _calculate_level_performance()             │
│       │         └─ _calculate_activity_distribution()         │
│       └─ Returns StudentProgressResponse                     │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Details

### 1. Frontend: useStudentReports Hook

**Change**: Add authentication header to fetch call

**Current code**:
```typescript
const response = await fetch(
  `${API_BASE_URL}/api/v1/statistic/students/${studentId}/progress`,
  {
    headers: {
      "Content-Type": "application/json",
    },
  }
);
```

**New code**:
```typescript
// Get token from cookies (httpOnly cookie set by backend)
const token = document.cookie
  .split('; ')
  .find(row => row.startsWith('auth_token='))
  ?.split('=')[1];

const response = await fetch(
  `${API_BASE_URL}/api/v1/statistic/students/${studentId}/progress`,
  {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { "Authorization": `Bearer ${token}` } : {}),
    },
    credentials: "include", // Include cookies in request
  }
);
```

**Rationale**: Uses `credentials: "include"` to send httpOnly cookies, which is the same mechanism used by other authenticated requests in the app.

### 2. Backend: Schema Safety

**Current issue**: The `_calculate_level_performance` method uses `f"Nivel {p.attempt_count}"` which always produces a string. But if `p.segment_level_id` is `None`, the activity distribution still works because `str(None)[:8]` = `"None"`.

**The actual Pydantic error** comes from a different source. Looking at the error log:
```
Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
```

This likely comes from `ProgressOverTimeItem.date` which uses `p.created_at.strftime(...)` — if `p.created_at` is `None`, this would crash before reaching Pydantic.

**Fix**: Add null checks in the usecase methods.

### 3. API URL Configuration

The `API_BASE_URL` in the hook defaults to `http://localhost:8000` but the Docker dev environment uses port `8010`. This is already handled by `NEXT_PUBLIC_API_URL` env var.

**Verify**: Check `apps/frontend/.env` has `NEXT_PUBLIC_API_URL=http://localhost:8010`.

## Sequence Diagram

```
Professor Browser     Frontend               Backend Statistic
      │                   │                        │
      │  Navigate to      │                        │
      ├──────────────────>│                        │
      │  /students/{id}/  │                        │
      │  reports          │                        │
      │                   │  fetch GET             │
      │                   │  /statistic/students/  │
      │                   │  {id}/progress         │
      │                   │  + Auth Header         │
      │                   ├───────────────────────>│
      │                   │                        │
      │                   │                   Validate Token
      │                   │                        │
      │                   │                   Query Progress
      │                   │                        │
      │                   │                   Calculate KPIs
      │                   │                        │
      │                   │  200 OK                │
      │                   │  StudentProgressResp   │
      │                   │<───────────────────────┤
      │                   │                        │
      │  Render Dashboard │                        │
      │<──────────────────│                        │
```

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Cookie not sent (CORS) | High | Ensure backend CORS allows credentials |
| Token expired | Medium | Handle 401 redirect to login |
| No progress data | Low | Return empty arrays with zero KPIs |
| Backend port mismatch | Medium | Verify NEXT_PUBLIC_API_URL env var |
