# Agent Guidelines for Hello World Backend

See PROJECT_SPEC.md for full specifications.

Always changed a important part of the codebase (dependency or bussines rules) update PROJECT_SPEC.md

Always finish a task committed

## Environment Configuration

The application supports two environment configurations:

### Local Development (uvicorn)
Use `.env.local` when running the app locally with uvicorn:
```bash
# DATABASE_URL points to localhost (Docker DB exposed on host)
DATABASE_URL=postgresql+asyncpg://value:password@localhost:5432/hello-world-db
```

**Note:** The application automatically detects `.env.local` if it exists and uses it instead of `.env`.

### Docker Development
Use `.env` when running everything in Docker Compose:
```bash
# DATABASE_URL points to Docker service name
DATABASE_URL=postgresql+asyncpg://value:password@postgresql_db:5432/hello-world-db
```

### Priority
1. If `.env.local` exists → use it (local development)
2. Otherwise → use `.env` (Docker environment)

## Build/Run Commands

```bash
# Development server
uvicorn main:app --reload

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000

# Database
alembic upgrade head              # Run migrations
alembic revision --autogenerate -m "msg"  # Create
alembic downgrade -1              # Rollback

# Testing
pytest                           # All
pytest tests/test_user.py           # Single file
pytest tests/test_user.py::test_create_user  # Single test
pytest --cov=src --cov-report=html  # Coverage
```

## Code Style Guidelines

### Import Organization
Order: stdlib → third-party → local, separated by blank lines.
```python
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.config import settings
from src.shared.application.usecase.base_service import BaseService
from src.users.application.service.user_service import UserService
from src.users.api.v1.schemas.user import UserCreate
```

### Architecture Structure
```
src/{domain}/application/
├── service/        # CRUD + simple validations
└── usecase/       # Business logic workflows
src/{domain}/api/v1/endpoints/{action}.py  # One endpoint per file
```

### Naming Conventions
- Classes: PascalCase (UserService, CreateUserUseCase)
- Functions: snake_case (get_by_id, execute)
- Variables: snake_case (user_id, user_data)
- Constants: UPPER_CASE (DATABASE_URL, SECRET_KEY)
- Endpoint files: {action}.py (create_user.py, login.py)

### Services (src/{domain}/application/service/)
- Inherit from BaseService
- Only CRUD + simple validations
- Use DI: `service: Service = Depends()`
```python
class UserService(BaseService):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        super().__init__(UserRepository(db), User)
```

### UseCases (src/{domain}/application/usecase/)
- Business logic + workflow orchestration
- Orchestrate multiple services
- Method named: `execute()`
```python
class AuthenticateUseCase:
    def __init__(self, user_service: UserService = Depends()):
        self.user_service = user_service
    async def execute(self, email: str, password: str) -> Token:
        # Business logic
```

### Endpoints (src/{domain}/api/v1/endpoints/{action}.py)
- One endpoint per file
- Use APIRouter with prefix
- Inject UseCases for business logic
```python
router = APIRouter(prefix="/auth")
@router.post("/login")
async def login(form_data: LoginData, auth_uc: AuthenticateUseCase = Depends()):
    return await auth_uc.execute(...)
```

### Error Handling
- Custom: NotFoundException, DuplicateEntryException, InvalidCredentialsException
- In endpoints: catch and raise HTTPException
```python
try:
    result = await usecase.execute(...)
except NotFoundException as e:
    raise HTTPException(status_code=404, detail=str(e))
```

### Router Structure
- `{domain}/api/router.py`: Domain central
- `{domain}/api/v1/router.py`: V1 domain (aggregates endpoints)
- `src/api/v1/router.py`: V1 central (aggregates domain routers)
- `src/api/router.py`: API central

### Database
- Always async/await with AsyncSession
- Use select() (SQLAlchemy 2.0)
- No direct queries in endpoints
