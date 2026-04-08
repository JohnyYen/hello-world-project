# Fix Login Error Handling and User Not Found

## Problem

The login flow has two critical bugs:

1. **Backend `DoesNotExistError` not handled**: When a user attempts to login with a non-existent email, the `AuthenticateUseCase` throws an unhandled exception that returns `{"exc_type":"DoesNotExistError"}` instead of a proper 401 response with a user-friendly error message.

2. **Frontend error not displayed**: The `loginAction` in the frontend expects a `detail` field in error responses but the backend returns `exc_type`. When login fails, the form silently reloads without showing any error message to the user.

## Impact

- Users cannot determine if login failed due to wrong credentials or system error
- Non-existent users return obscure `DoesNotExistError` instead of "Credenciales incorrectas"
- Error handling in `loginAction` catches exceptions but cannot extract meaningful message from backend response format

## Goals

1. Backend MUST return proper HTTP 401 with `detail` field for all authentication failures (user not found, wrong password)
2. Frontend MUST display error messages from the backend to the user
3. Both issues should be fixed with minimal changes to existing architecture

## Non-Goals

- Changing the redirect destination (currently `/dashboard`)
- Modifying the signup flow
- Adding rate limiting or account lockout

## Affected Modules

| Module | File | Change Type |
|--------|------|-------------|
| Backend - Auth Endpoint | `apps/backend/src/auth/api/v1/endpoints/login.py` | Add exception handler |
| Backend - UseCase | `apps/backend/src/auth/application/usecase/authenticate_usecase.py` | Add exception handler |
| Frontend - Login Action | `apps/frontend/src/lib/actions.ts` | Review error parsing (likely no change needed if backend is fixed) |

## Rollback Plan

Both fixes are additive (adding try/catch blocks and exception handlers). Rollback is simply reverting the commit. No database migrations or config changes are involved.

## Success Criteria

1. Login with non-existent user returns HTTP 401 with `{"detail": "Credenciales incorrectas"}`
2. Login with wrong password returns HTTP 401 with `{"detail": "Credenciales incorrectas"}`
3. Frontend displays the error message below the login form
4. Successful login still redirects to `/dashboard`
