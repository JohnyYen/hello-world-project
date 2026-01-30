# AGENTS.md - Guide for Coding Agents

## Project Overview
Monorepo with 3 applications:
- **hello-world-backend**: FastAPI async backend with SQLAlchemy, Alembic, JWT auth
- **hello-world-nextjs**: Next.js 15 frontend with TypeScript, Tailwind CSS, Radix UI
- **hello-world!!**: Godot 4.x educational game with GDScript, SQLite, adaptive agent

## Build/Dev/Test Commands

### Backend (FastAPI)
```bash
cd apps/hello-world-backend

# Development
uvicorn main:app --reload

# Database Migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Lint/Format (not configured, but would use:)
# black src/
# flake8 src/
# isort src/

# Testing (dependencies commented out in requirements.txt)
# pytest                           # Run all tests
# pytest tests/test_file.py::test_name  # Run single test
# pytest -k "test_specific"        # Run tests matching pattern
# pytest -x                        # Stop on first failure
# pytest --cov=src tests/          # With coverage
```

### Frontend (Next.js)
```bash
cd apps/hello-world-nextjs

# Development
npm run dev                       # Turbopack enabled
npm run build                     # Production build
npm start                         # Start production server

# Linting
npm run lint                      # ESLint (many rules disabled)

# No test scripts configured
# Tests would use: npm test, npm run test:unit, etc.
```

### Game (Godot)
```bash
cd apps/hello-world!!

# Open in Godot Editor (Godot 4.x required)
# Tests run through GUT plugin: Scene -> GUT -> Run All Tests
# Single test: Select test scene in GUT UI
```

### Docker Compose
```bash
cd infraestructure/docker
docker-compose -f docker-compose.dev.yml up -d
```

## Code Style Guidelines

### Backend (Python/FastAPI)

**Imports**: Standard library → third-party → local (src.*)
```python
from datetime import timedelta
from fastapi import APIRouter, Depends
from src.core.config import settings
from src.db.session import get_db
```

**Type Hints**: Use strict typing with Optional, List, Dict
```python
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> Optional[User]:
    return await user_repo.get_by_id(user_id)
```

**Naming Conventions**:
- Classes: `PascalCase` (`UserService`, `BaseSettings`)
- Functions/variables: `snake_case` (`get_user`, `user_id`)
- Constants: `UPPER_SNAKE_CASE` (`DATABASE_URL`)
- Private: `_leading_underscore` (`_create_tables`)

**Error Handling**: Custom exceptions in `src/core/exceptions.py`
```python
from src.core.exceptions import NotFoundException
raise HTTPException(status_code=404, detail="Not found")
```

**Async Patterns**: Always use async/await for database operations
```python
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_repo.create(user)
```

**Documentation**: Docstrings for classes and complex functions

**Repository Pattern**: Separate repositories in `src/db/repositories/`
**Service Layer**: Business logic in `src/services/`

### Frontend (Next.js/TypeScript)

**Imports**: React → third-party → local (@/*)
```typescript
import { useState } from "react"
import { Button } from "@/components/ui/button"
```

**Components**: Functional components with TypeScript interfaces
```typescript
interface ButtonProps {
  variant?: "default" | "destructive"
  size?: "default" | "sm" | "lg"
}
export function Button({ variant, size, ...props }: ButtonProps) {
  return <button {...props} />
}
```

**Naming Conventions**:
- Components: `PascalCase` (`Button`, `DataTable`)
- Functions/variables: `camelCase` (`getUser`, `userId`)
- Files: `kebab-case.tsx` (`button.tsx`, `data-table.tsx`)

**Styling**: Tailwind CSS with class utility helper `cn()`
```typescript
import { cn } from "@/lib/utils"
<div className={cn("base-class", condition && "conditional-class")} />
```

**State Management**: React hooks (useState, useEffect), no explicit Redux

**API Calls**: Service functions in `src/services/`, use async/await

**UI Components**: Radix UI primitives in `src/components/ui/`

### Game (Godot/GDScript)

**Class Definitions**: `class_name` for global registration
```gdscript
class_name ExecutionEngine
extends Node
```

**Naming Conventions**:
- Classes: `PascalCase` (`ExecutionEngine`, `BaseBlock`)
- Functions: `snake_case` (`execute`, `get_block`)
- Variables: `snake_case` (`block_id`, `student_queue`)
- Constants: `UPPER_SNAKE_CASE` (`MAX_BLOCKS`)

**Type Hints**: Explicit typing with `: Type`
```gdscript
func execute(blocks: Array, context: BaseProblemContext) -> BaseProblemContext:
    return context
```

**Control Flow**: 4-space indentation (not tabs)
```gdscript
if blocks.size() == 0:
    print("Error: No blocks")
    return context
```

**Comments**: Use `#` for single-line, block comments for multi-line

**Structure**: MVC pattern - Models/, Scripts/controllers/, Scenes/

**Database**: SQLite with repository pattern in `scripts/database/repositories/`

**Testing**: Custom GDScript tests in `test/unit/` and `test/integrations/`

## General Principles

- **No comments in code** unless explicitly requested (per system instructions)
- **Follow existing patterns** in each app before introducing new ones
- **Keep functions small and focused** (single responsibility)
- **Use existing dependencies** - don't add new libraries without checking
- **Async operations** in backend, sync in game (GDScript)
- **Strict typing** in Python and TypeScript, explicit in GDScript
- **Error boundaries** in React, try/catch in Python
- **No hardcoded values** - use config/environment variables
- **Test-driven** when adding new features (though tests are limited currently)

## Key Files Reference

- Backend config: `apps/hello-world-backend/src/core/config.py`
- Frontend config: `apps/hello-world-nextjs/package.json`
- Game config: `apps/hello-world!!/config/game_config.gd`
- Docker compose: `infraestructure/docker/docker-compose.dev.yml`
