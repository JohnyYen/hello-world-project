# Hello World Backend - AI Agent Ruleset

> **Skills Reference**: For detailed patterns, use these skills:
> - [`fastapi`](https://fastapi.tiangolo.com/) - Async patterns, JWT auth, Pydantic v2
> - [`architecture-patterns`](#) - Clean Architecture (Service/UseCase)
> - [`pytest`](https://docs.pytest.org/) - Generic pytest patterns
> - [`tdd`](#) - Test-Driven Development workflow

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| Committing changes | `prowler-commit` |
| Creating FastAPI endpoints | `fastapi` |
| Fixing bug | `tdd` |
| Implementing feature | `tdd` |
| Refactoring code | `tdd` |
| Working on task | `tdd` |
| Writing Python tests with pytest | `pytest` |

---

## CRITICAL RULES - NON-NEGOTIABLE

### Models
- ALWAYS: UUIDv4 PKs, `created_at`/`updated_at` timestamps.
- ALWAYS: Use `AsyncSession` for all database operations.
- NEVER: Synchronous database calls or auto-increment integer PKs.

### Architecture (Service/UseCase Pattern)
- ALWAYS: Separate logic into `Service` (CRUD) and `UseCase` (Business Logic).
- ALWAYS: Use `Depends()` for dependency injection of services and usecases.
- NEVER: Business logic in endpoints or raw SQL queries in services.

### Endpoints
- ALWAYS: One endpoint per file in `src/{domain}/api/v1/endpoints/{action}.py`.
- ALWAYS: Catch custom exceptions and raise `HTTPException` with appropriate status codes.
- NEVER: Logic directly in the endpoint function; delegate to UseCases.

---

## DECISION TREES

### Service vs UseCase
```
CRUD / Simple Validation → Service
Business Workflow / Multi-service orchestration → UseCase
```

---

## TECH STACK

FastAPI | SQLAlchemy 2.0 (Async) | Alembic | Pydantic v2 | PostgreSQL 16 | pytest

---

## PROJECT STRUCTURE

```
apps/backend/src/
├── {domain}/
│   ├── api/v1/endpoints/   # One file per action
│   ├── application/
│   │   ├── service/        # CRUD logic
│   │   └── usecase/       # Business workflows
│   └── models.py          # SQLAlchemy models
├── shared/                # Cross-domain utilities
└── main.py                # Application entry point
```

---

## COMMANDS

```bash
# Development
uvicorn main:app --reload

# Database
alembic revision --autogenerate -m "description"
alembic upgrade head

# Testing
pytest
pytest --cov=src tests/
```

---

## QA CHECKLIST

- [ ] `pytest` passes
- [ ] Async/Await used correctly in all DB calls
- [ ] Endpoint delegated to UseCase
- [ ] Migrations created for model changes
- [ ] UUIDs used for all primary keys
