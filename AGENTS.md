# Repository Guidelines

## How to Use This Guide

- Start here for cross-project norms. This is a monorepo with 3 main applications.
- Each component has an `AGENTS.md` file with specific guidelines (e.g., `apps/backend/AGENTS.md`, `apps/frontend/AGENTS.md`, `apps/game/AGENTS.md`).
- Component docs override this file when guidance conflicts.

## Available Skills

Use these skills for detailed patterns on-demand:

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

## Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| App Router / Server Actions | `nextjs-15` |
| Committing changes | `prowler-commit` (Simulated) |
| Creating FastAPI endpoints | `fastapi` |
| Creating Zod schemas | `zod-4` |
| Creating/modifying React components | `react-19` |
| Fixing bug | `tdd` |
| Implementing feature | `tdd` |
| Refactoring code | `tdd` |
| Working on Task | `tdd` |
| Working with Tailwind classes | `tailwind-4` |
| Writing Python tests with pytest | `pytest` |
| Writing TypeScript types/interfaces | `typescript` |

---

## Project Overview

Hello World Project is a multi-platform educational ecosystem.

| Component | Location | Tech Stack |
|-----------|----------|------------|
| Backend | `apps/backend/` | FastAPI, SQLAlchemy (Async), Alembic, PostgreSQL |
| Frontend | `apps/frontend/` | Next.js 15, React 19, Tailwind 4, shadcn/ui |
| Game | `apps/game/` | Godot 4.x, GDScript, SQLite |

---

## Commit & Pull Request Guidelines

Follow conventional-commit style: `<type>[scope]: <description>`

**Types:** `feat`, `fix`, `docs`, `chore`, `perf`, `refactor`, `style`, `test`

Before creating a PR:
1. Run all relevant tests and linters for the modified component.
2. Ensure no hardcoded secrets are committed.
3. Verify cross-component compatibility (e.g., API changes vs Frontend/Game).

---

## Infrastructure

The project uses Docker Compose for local development:
- Location: `infraestructure/docker/docker-compose.dev.yml`
- Services: `postgresql_db`, `backend`, `frontend`, `game` (as needed).