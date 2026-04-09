# Repository Guidelines

## How to Use This Guide

- Start here for cross-project norms. This is a monorepo with 3 main applications.
- Each component has an `AGENTS.md` file with specific guidelines (e.g., `apps/backend/AGENTS.md`, `apps/frontend/AGENTS.md`, `apps/game/AGENTS.md`).
- Component docs override this file when guidance conflicts.

## Available Skills

All skills are located in `.agents/skills/`. Invoke them using the Skill tool when working with specific technologies.

### Generic Skills (Any Project)
| Skill | Description |
|-------|-------------|
| `typescript` | Const types, flat interfaces, utility types |
| `react-19` | No useMemo/useCallback, React Compiler |
| `nextjs-15` | App Router, Server Actions, streaming |
| `tailwind-4` | cn() utility, no var() in className |
| `fastapi` | Async patterns, JWT auth, Pydantic v2 |
| `architecture-patterns` | Clean Architecture, Service/UseCase patterns |
| `tdd` | Test-Driven Development workflow |
| `pytest` | Python testing with fixtures and mocking |
| `playwright` | E2E testing patterns |
| `zod-4` | Schema validation |
| `zustand-5` | State management |
| `ai-sdk-5` | Vercel AI SDK for chat features |
| `django-drf` | Django REST Framework patterns |

### SDD (Spec-Driven Development)
| Skill | Description |
|-------|-------------|
| `sdd-init` | Initialize SDD context |
| `sdd-explore` | Explore and investigate ideas |
| `sdd-propose` | Create change proposal |
| `sdd-spec` | Write specifications |
| `sdd-design` | Technical design document |
| `sdd-tasks` | Task breakdown |
| `sdd-apply` | Implement code |
| `sdd-verify` | Validate implementation |
| `sdd-archive` | Archive completed change |

### Additional Skills
| Skill | Description |
|-------|-------------|
| `frontend-design` | Production-grade UI design |
| `prowler-commit` | Conventional commit workflow |
| `skill-creator` | Create new skills |
| `skill-lookup` | Discover available skills |
| `jira-task` | Create Jira tasks |
| `jira-epic` | Create Jira epics |
| `pr-review` | Review GitHub PRs |
| `monorepo-management` | Turborepo, Nx, pnpm workspaces |
| `architecture-decision-records` | ADRs documentation |
| `api-design-principles` | REST/GraphQL design |
| `github-actions-templates` | CI/CD workflows |
| `openapi-spec-generation` | OpenAPI 3.1 specs |
| `fastapi-templates` | Project templates |
| `tailwind-patterns` | UI component patterns |
| `e2e-testing-patterns` | Playwright/Cypress patterns |
| `dotnet-backend-patterns` | C#/.NET patterns |

## Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| App Router / Server Actions | `nextjs-15` |
| Committing changes | `prowler-commit` |
| Creating FastAPI endpoints | `fastapi` |
| Creating Zod schemas | `zod-4` |
| Creating/modifying React components | `react-19` |
| Design UI | `frontend-design` |
| Fixing bug | `tdd` |
| Implementing feature | `tdd` |
| Refactoring code | `tdd` |
| Working on Task | `tdd` |
| Working with Tailwind classes | `tailwind-4` |
| Writing Python tests with pytest | `pytest` |
| Writing TypeScript types/interfaces | `typescript` |

---

## Project Overview

Hello World Project is a multi-platform educational ecosystem that combines:

1. **Visual Programming Game** - An adaptive Godot 4.4 game where students solve real-world problems using visual programming blocks
2. **Intelligent Backend API** - A FastAPI async server managing users, courses, progress tracking, xAPI statements, and LMS integration
3. **Modern Web Dashboard** - A Next.js 15 application for professors to create content, track student progress, and generate detailed analytics

| Component | Location | Tech Stack | Purpose |
|-----------|----------|------------|---------|
| Backend | `apps/backend/` | FastAPI 0.115+, SQLAlchemy 2.0 (Async), Alembic, Pydantic v2, PostgreSQL 16, uv | REST API with JWT auth, user management, game/level CRUD, progress tracking, xAPI, LMS sync |
| Frontend | `apps/frontend/` | Next.js 15.5, React 19, TypeScript 5, Tailwind 4, shadcn/ui, Zod 4, Zustand 5, Recharts | Admin dashboard for professors (course management, student tracking, analytics, reports) |
| Game | `apps/game/` | Godot 4.4, GDScript 2.0, SQLite, GUT, Dialogue Manager | Educational visual programming game with adaptive difficulty and xAPI tracking |
| API Client | `packages/api-client-ts/` | TypeScript, auto-generated from OpenAPI | Shared TypeScript client for backend API |
| API Contract | `packages/api-contract/` | OpenAPI JSON/YAML | API specification contract |

### User Roles

| Role | Description | Auto-assigned? |
|------|-------------|----------------|
| `admin` | System administrator with full access | No (via seed) |
| `professor` | Teacher who creates content and monitors students | Yes (on register) |
| `student` | Learner who plays games and solves puzzles | No (created by professor) |

---

## Commit & Pull Request Guidelines

Follow conventional-commit style: `<type>[scope]: <description>`

**Types:** `feat`, `fix`, `docs`, `chore`, `perf`, `refactor`, `style`, `test`

**Examples:**
```
feat(auth): add LMS credential registration endpoint
fix(sync): resolve session timeout on reconnect
docs(api): update xAPI statement schema
refactor(users): extract service from usecase
test(game): add GUT tests for adaptive agent
```

Before creating a PR:
1. Run all relevant tests and linters for the modified component.
2. Ensure no hardcoded secrets are committed.
3. Verify cross-component compatibility (e.g., API changes vs Frontend/Game).
4. Update OpenAPI spec if backend endpoints changed.
5. Regenerate API client if spec changed: `pnpm run generate:api-client`

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Unit tests pass
- [ ] E2E tests pass (if applicable)
- [ ] Manual testing completed

## Screenshots (if UI changes)
[Add screenshots here]
```

---

## Infrastructure

The project uses Docker Compose for local development:
- Location: `infraestructure/docker/docker-compose.dev.yml`
- Services: `postgresql_db`, `backend`, `frontend`, `adminer` (database UI)

### Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| `postgresql_db` | 5432 | PostgreSQL 16 database |
| `backend` | 8000 | FastAPI REST API |
| `frontend` | 3000 | Next.js 15 web app |
| `adminer` | 8081 | Database management UI |

### Environment Variables

Backend requires these variables in `.env` file:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/hello_world
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

Frontend requires:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Monorepo Management

This project uses pnpm workspaces for package management:

```bash
# Install all dependencies
pnpm install

# Run command in specific workspace
pnpm --filter @workspace/frontend run dev

# List all workspaces
pnpm list -r --depth=-1
```

### Workspace Packages
- `apps/frontend` - Next.js application
- `packages/api-client-ts` - TypeScript API client
- `packages/api-contract` - OpenAPI specification

---

## Development Workflow

### Feature Development
1. Create feature branch: `git checkout -b feature/feature-name`
2. Implement changes following component-specific guidelines
3. Run tests and linters
4. Commit with conventional commits
5. Push and create PR

### API Changes
1. Update backend endpoints
2. Update OpenAPI spec (`packages/api-contract/openapi.json`)
3. Regenerate TypeScript client: `pnpm run generate:api-client`
4. Update frontend to use new client methods
5. Update game if new endpoints affect it

### Database Changes
1. Modify SQLAlchemy models in backend
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Test migration: `alembic upgrade head`
4. Verify data integrity
5. Commit migration file

---

## Code Quality Standards

### Python (Backend)
- PEP 8 compliant
- Type hints required on all functions
- Async/await for all I/O operations
- Service/UseCase pattern enforced
- UUIDv4 for all primary keys
- One endpoint per file
- Pydantic v2 for validation

### TypeScript (Frontend)
- ESLint configuration enforced
- Server Components by default
- Server Actions for mutations
- Zod validation for all forms
- Spanish UI text
- Explicit return types
- `interface` over `type`
- No `useMemo`/`useCallback`

### GDScript (Game)
- `snake_case` for functions and variables
- `PascalCase` for classes
- 4-space indentation
- Explicit type hints required
- Signal-based communication
- Repository pattern for database
- Spanish UI text

---

## Testing Strategy

| Component | Framework | Location | Coverage Target |
|-----------|-----------|----------|-----------------|
| Backend | pytest | `apps/backend/tests/` | 70%+ |
| Frontend | Vitest + Playwright | `apps/frontend/tests/` | 60%+ |
| Game | GUT | `apps/game/test/` | 50%+ |

### Running Tests

```bash
# Backend
cd apps/backend && uv run pytest --cov=src

# Frontend (unit)
cd apps/frontend && pnpm run test

# Frontend (E2E)
cd apps/frontend && pnpm run test:e2e

# Game
# Open Godot → GUT Panel → Run All
```

---

## Component-Specific Guidelines

Refer to individual AGENTS.md files for detailed rules:

- **Backend**: [apps/backend/AGENTS.md](./apps/backend/AGENTS.md)
- **Frontend**: [apps/frontend/AGENTS.md](./apps/frontend/AGENTS.md)
- **Game**: [apps/game/AGENTS.md](./apps/game/AGENTS.md)

### Quick Reference

| Component | Key Pattern | Critical Rule |
|-----------|-------------|---------------|
| Backend | Service + UseCase | Never put business logic in endpoints |
| Frontend | Server Components + Server Actions | Never use `useMemo`/`useCallback` |
| Game | MVC + Signals | Never hardcode config values |

---

## Documentation Structure

```
hello-world-project/
├── README.md                    # This file - project overview
├── AGENTS.md                    # This file - cross-project guidelines
├── apps/
│   ├── backend/
│   │   ├── README.md            # Backend architecture, API docs
│   │   ├── AGENTS.md            # Backend AI rules
│   │   └── docs/
│   │       ├── database-design.md
│   │       └── user_stories.md
│   ├── frontend/
│   │   ├── README.md            # Frontend architecture, conventions
│   │   ├── AGENTS.md            # Frontend AI rules
│   │   └── PERFORMANCE_OPTIMIZATION.md
│   └── game/
│       ├── README.md            # Game architecture, GDScript guide
│       ├── AGENTS.md            # Game AI rules
│       └── LEVEL_1_DEVELOPMENT_ROADMAP.md
└── packages/
    ├── api-client-ts/           # TypeScript client
    └── api-contract/            # OpenAPI spec
```

---

## Useful Links

- **Repository**: [GitHub](https://github.com/JohnyYen/hello-world-project)
- **Issues**: [GitHub Issues](https://github.com/JohnyYen/hello-world-project/issues)
- **FastAPI Docs**: [Official Documentation](https://fastapi.tiangolo.com/)
- **Next.js Docs**: [Official Documentation](https://nextjs.org/docs)
- **Godot Docs**: [Official Documentation](https://docs.godotengine.org/)
- **xAPI Spec**: [xAPI Specification](https://xapi.com/)
