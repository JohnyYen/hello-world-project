# Design: Fix Login Error Handling

## Technical Approach

Add exception handling at two layers in the backend:
1. **UseCase layer**: Catch any exception from the repository (including `DoesNotExistError`/`NoResultFound`) and convert to `InvalidCredentialsException`
2. **Endpoint layer**: Add a catch-all exception handler as a safety net for any unexpected errors

The frontend `loginAction` already correctly parses ResponseError with a `detail` field, so once the backend returns a proper HTTP 401 with `detail`, the UI will display the error.

## Architecture Decisions

### Decision: Handle at UseCase level, not just endpoint

**Choice**: Wrap the repository call in `AuthenticateUseCase.execute` with a try/except that catches all exceptions and raises `InvalidCredentialsException`
**Alternatives considered**: 
- Handle only at the endpoint level
- Let the repository return `None` and check in the usecase
**Rationale**: The UseCase is the right place to translate infrastructure-level exceptions (like "user not found") into domain-level exceptions ("invalid credentials"). This keeps the endpoint clean and ensures any code path through the usecase produces consistent errors. The repository currently raises an unhandled exception when the user doesn't exist, which should be normalized at the application layer.

### Decision: Keep generic error message for all auth failures

**Choice**: Return "Credenciales incorrectas" for both user-not-found and wrong-password scenarios
**Alternatives considered**: 
- Return "Usuario no encontrado" for non-existent users
- Return "Contraseña incorrecta" for wrong passwords
**Rationale**: Security best practice — revealing whether an email exists in the system enables email enumeration attacks. A generic message is the OWASP-recommended approach.

## Data Flow

### Current (Broken)

```
Frontend: loginAction
    │
    ▼
Backend: POST /api/v1/auth/login
    │
    ▼
AuthenticateUseCase.execute()
    │
    ▼
UserRepository.authenticate_by_username_or_email()
    │
    ├── User not found → raises DoesNotExistError (unhandled)
    │       │
    │       ▼
    │   Global exception handler → 500 {"exc_type": "DoesNotExistError"}
    │
    └── Wrong password → raises InvalidCredentialsException
            │
            ▼
        Endpoint catches it → 401 {"detail": "Credenciales incorrectas"}
```

### Fixed

```
Frontend: loginAction
    │
    ▼
Backend: POST /api/v1/auth/login
    │
    ▼
AuthenticateUseCase.execute()
    │
    ▼
try: UserRepository.authenticate_by_username_or_email()
    │
    ├── User not found → raises any exception
    │       │
    │       ▼
    │   except → raise InvalidCredentialsException("Credenciales incorrectas")
    │
    └── Wrong password → raises InvalidCredentialsException
            │
            ▼
    Endpoint catches InvalidCredentialsException → 401 {"detail": "Credenciales incorrectas"}
    │
    ▼
Frontend: loginAction catches ResponseError
    │
    ▼
Extracts detail → state.errors._form = ["Credenciales incorrectas"]
    │
    ▼
UI displays error message in red below form
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `apps/backend/src/auth/application/usecase/authenticate_usecase.py` | Modify | Add try/except around repository call to catch all exceptions and raise `InvalidCredentialsException` |
| `apps/backend/src/auth/api/v1/endpoints/login.py` | Modify | Add catch-all exception handler as safety net |

## Interfaces / Contracts

No new interfaces. The response contract remains:

```python
# Success (200)
UserLoginResponse(
    access_token: str,
    token_type: str,
    expires_in: int,
    user: UserResponse
)

# Error (401)
{"detail": "Credenciales incorrectas"}
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `AuthenticateUseCase` converts user-not-found to `InvalidCredentialsException` | Mock repository to raise exception, assert usecase raises `InvalidCredentialsException` |
| Integration | POST `/api/v1/auth/login` with non-existent email returns 401 | Direct curl or httpx test |
| Integration | POST `/api/v1/auth/login` with wrong password returns 401 | Direct curl or httpx test |
| E2E | Login UI shows error message after failed login | playwright-cli fill + click + verify error displayed |

## Migration / Rollout

No migration required. This is a pure code fix with no database changes or feature flags.

## Open Questions

- [ ] None
