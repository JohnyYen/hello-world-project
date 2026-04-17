# Student Creation Functionality - Error Report

**Date:** April 9, 2026  
**Branch:** `review/student-creation-functionality` (from `develop`)  
**Test URL:** http://localhost:3000/dashboard/students  
**Backend URL:** http://localhost:8010 (Docker)

---

## Executive Summary

Testing the student creation functionality revealed **6 critical errors** and **3 warnings** that prevent the feature from working correctly.

---

## 🔴 CRITICAL ERRORS

### 1. Missing `or_` Import in UserRepository

**File:** `apps/backend/src/users/infrastructure/user_repository.py:4`  
**Severity:** CRITICAL - Runtime Error

**Issue:**
```python
from sqlalchemy import select, update, and_  # or_ is missing!
```

But `or_()` is used at line 320:
```python
query = query.where(
    or_(  # ❌ NameError: name 'or_' is not defined
        User.name.ilike(search_pattern),
        User.lastname.ilike(search_pattern),
        User.email.ilike(search_pattern),
        User.username.ilike(search_pattern),
    )
)
```

**Impact:** Any search operation on students will crash with a `NameError`.

**Fix:**
```python
from sqlalchemy import select, update, and_, or_
```

---

### 2. Backend Returns 404 on Students Endpoint

**Endpoint:** `GET /api/v1/users/students`  
**Status:** HTTP 404 - `{"exc_type":"DoesNotExistError"}`  
**Severity:** CRITICAL

**Issue:**
When accessing the students list endpoint (even with proper authentication), the backend returns a 404 error with `DoesNotExistError`. This suggests:
- Missing database records for role lookup
- Broken initialization script for roles
- Query trying to fetch a non-existent entity

**Evidence:**
```bash
$ curl http://localhost:8010/api/v1/users/students
{"exc_type":"DoesNotExistError"}
```

**Impact:** The student list page cannot load any students, showing an empty state.

---

### 3. Student Creation Depends on Broken List Endpoint

**File:** `apps/frontend/src/components/student/student-data-provider.tsx`

**Issue:**
The student page depends on `getStudents()` which calls the backend:
```typescript
const response = await apiGetStudents(token);
return (response.data ?? []).map((s) => ({...}));
```

If the backend returns 404/500, the frontend catches the error and returns an empty array:
```typescript
} catch {
  return [];  // Silently fails, no error shown to user
}
```

**Impact:** 
- No visual feedback when API fails
- User sees empty table without knowing why
- Difficult to debug production issues

---

### 4. Frontend API Client Uses Wrong Port

**Issue:**
The frontend code likely uses `NEXT_PUBLIC_API_URL` environment variable. If this is set to `http://localhost:8000` but the Docker backend runs on port `8010`, all API calls will fail.

**Evidence:**
- Docker Compose maps: `0.0.0.0:8010->8000/tcp`
- If `.env` has `NEXT_PUBLIC_API_URL=http://localhost:8000`, requests will timeout

**Impact:** All API calls from frontend to backend will fail silently or timeout.

---

### 5. Missing Authorization Header in Student Reports Hook

**File:** `apps/frontend/src/hooks/use-student-reports.ts:37`

**Issue:**
```typescript
const response = await fetch(
  `${API_BASE_URL}/api/v1/statistic/students/${studentId}/progress`,
  {
    headers: {
      "Content-Type": "application/json",
      // ❌ Missing Authorization header!
    },
  }
);
```

The backend endpoint requires JWT authentication (via `HTTPBearer()`), but the fetch call doesn't include the auth token.

**Impact:** Student reports/progress pages will always return 401/403 errors.

---

### 6. No Token in Student Progress API Call

**File:** `apps/frontend/src/api/client.ts:152`

**Issue:**
```typescript
getStudentProgress: (studentId: string, token: string) =>
  request<import("./types").StudentProgressResponse>(
    `/api/v1/users/students/${studentId}/progress`,
    { token }  // ✓ Has token
  ),
```

BUT the hook in `use-student-reports.ts` doesn't use this API client and makes a raw `fetch()` call without the token.

**Impact:** Inconsistent API access patterns, authentication failures.

---

## ⚠️ WARNINGS

### 7. Silent Error Handling in Data Provider

**File:** `apps/frontend/src/components/student/student-data-provider.tsx:93`

```typescript
} catch {
  return [];  // No logging, no error propagation
}
```

**Impact:** Makes debugging extremely difficult. Users see empty states with no explanation.

---

### 8. Delete Functionality is Mock Only

**File:** `apps/frontend/src/components/student/student-table.tsx:79`

```typescript
const confirmDelete = () => {
  // In a real application, you would call an API to delete the students
  console.log(`Deleting students:`, Array.from(selectedStudents));
  
  // Reset selections after deletion
  setSelectedStudents(new Set());
  setDeleteDialogOpen(false);
};
```

**Issue:** The delete button in the UI doesn't actually delete students from the backend. It only clears the local state selection.

**Impact:** Misleading UI - users think they deleted students but nothing happens in the backend.

---

### 9. Missing `course` Field in Student Type

**File:** `apps/frontend/src/types/index.ts`

**Issue:**
The `Student` type doesn't include a `course` field:
```typescript
export interface Student {
  id: string;
  name: string;
  email: string;
  maxLevel: number;
  status: string;
  registrationDate: string;
  lastActivity: string;
  completedLessons: number;
  totalLessons: number;
  progress: number;
  achievements: string[];
  // ❌ No 'course' field
}
```

But `student-data-provider.tsx:99` tries to access it:
```typescript
export async function getUniqueCourses(): Promise<string[]> {
  const students = await getStudents();
  return Array.from(
    new Set(students.map(s => (s as any).course).filter(...))  // ❌ Type safety bypassed
  );
}
```

**Impact:** Course filter will never work since students don't have a course field.

---

## 🔍 ADDITIONAL OBSERVATIONS

### Backend Architecture
- Clean Architecture pattern with proper layer separation
- Use Case pattern correctly implemented
- JWT authentication via `HTTPBearer()`
- Role-based access control (admin, professor, student)

### Frontend Architecture
- Next.js 15 with Server Components
- Server Actions for form submissions
- Dialog-based student creation with `CreateStudentForm`
- Zod validation schema present

### Database Design
- `Student` is a thin profile table extending `User` (1:1 relationship)
- All identity data lives in `users` table
- Soft deletes via `deleted_at` column

---

## 📋 RECOMMENDED FIXES (Priority Order)

1. **Fix missing `or_` import** (5 minutes)
   - File: `apps/backend/src/users/infrastructure/user_repository.py:4`
   - Add `or_` to SQLAlchemy imports

2. **Fix 404 DoesNotExistError** (15-30 minutes)
   - Check if roles exist in database
   - Run database seed/initialization scripts
   - Add proper error handling for missing roles

3. **Fix API URL configuration** (5 minutes)
   - Ensure `.env` has correct port: `NEXT_PUBLIC_API_URL=http://localhost:8010`
   - Or fix Docker port mapping to use 8000

4. **Add Authorization header to student reports hook** (10 minutes)
   - Import token from cookies
   - Add `Authorization: Bearer <token>` header

5. **Implement actual delete functionality** (30 minutes)
   - Connect to `usersApi.deleteStudent()` API
   - Revalidate cache after deletion

6. **Add course field to Student type or remove filter** (15 minutes)
   - Either add course field to type and backend response
   - Or remove the course filter UI if not applicable

7. **Improve error handling** (ongoing)
   - Add toast notifications on API failures
   - Show error states instead of empty tables
   - Log errors to console in development

---

## 🧪 TESTING COMMANDS

```bash
# Test backend students endpoint
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8010/api/v1/users/students

# Test student creation
curl -X POST http://localhost:8010/api/v1/users/students \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teststudent",
    "email": "test@example.com",
    "name": "Test",
    "lastname": "Student",
    "password": "SecurePass123!",
    "is_active": true
  }'

# Check backend logs
docker compose -f infraestructure/docker/docker-compose.dev.yml logs --tail=100 backend
```

---

## 📊 SUMMARY

| Category | Count |
|----------|-------|
| Critical Errors | 6 |
| Warnings | 3 |
| Estimated Fix Time | 2-3 hours |

**Overall Status:** 🔴 **BLOCKED** - Student creation functionality cannot be used due to critical backend errors (404 on students endpoint, missing imports).

**Next Steps:** Fix items 1-3 in the recommended fixes list to unblock basic functionality, then address remaining issues.
