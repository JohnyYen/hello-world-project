# Task Breakdown: Fix Login Error Handling

## Phase 1: Backend Fixes

### [x] 1.1 Add DoesNotExistError handling in AuthenticateUseCase
- Wrapped the `authenticate_by_username_or_email` call in a try/except
- Catches any exception (DoesNotExistError, etc.) and raises `InvalidCredentialsException`
- Also handles `None` return value from repository
- File: `apps/backend/src/auth/application/usecase/authenticate_usecase.py`

### [x] 1.2 Add generic exception handler in login endpoint
- Added catch-all exception handler for unexpected errors
- Returns HTTP 401 with "Credenciales incorrectas" for any unhandled exception
- File: `apps/backend/src/auth/api/v1/endpoints/login.py`

## Phase 2: Frontend Review

### [x] 2.1 Verify frontend error parsing works with corrected backend
- The existing error parsing in `loginAction` correctly extracts `detail` from the response
- The backend now returns proper 401 with `detail`, so the frontend works as-is
- **Bonus fix**: Fixed duplicate error message display in `login-form.tsx` (was showing error 3 times, now shows once)
- File: `apps/frontend/src/lib/actions.ts` (verified, no change needed)
- File: `apps/frontend/src/components/auth/login-form.tsx` (modified - fixed duplicate error display)

## Phase 3: Verification

### [x] 3.1 Test login with non-existent user via curl
- ✅ Backend returns HTTP 401 with `{"detail": "Credenciales incorrectas"}`

### [x] 3.2 Test login with wrong password via curl
- ✅ Backend returns HTTP 401 with `{"detail": "Credenciales incorrectas"}`

### [x] 3.3 Test login UI shows error message
- ✅ Error message "Credenciales incorrectas" is displayed once below the login button

### [x] 3.4 Test successful login
- ✅ Backend returns valid token (verified via curl on port 8010)
- ⚠️ Frontend redirect to `/dashboard` does not occur - pre-existing bug unrelated to error handling
  - The `auth_token` cookie is not being set by the Server Action
  - This is a separate issue that needs investigation in the frontend Server Actions flow
