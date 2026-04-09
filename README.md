# 🎮 Hello World Project

> An **intelligent, game-based learning platform** for teaching programming fundamentals through interactive visual programming, adaptive educational narratives, and real-time performance tracking.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Next.js 15](https://img.shields.io/badge/Next.js-15.5-black.svg)](https://nextjs.org)
[![Godot 4.4](https://img.shields.io/badge/Godot-4.4-blue.svg)](https://godotengine.org)
[![Package Manager](https://img.shields.io/badge/pnpm-10.4-orange.svg)](https://pnpm.io)
[![Package Manager](https://img.shields.io/badge/uv-FAST-brightgreen)](https://github.com/astral-sh/uv)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Development Guide](#-development-guide)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Hello World Project** is a comprehensive educational platform that combines:

1. **Visual Programming Game** - An adaptive Godot 4.4 game where students solve real-world problems using visual programming blocks
2. **Intelligent Backend API** - A FastAPI async server managing users, courses, progress tracking, xAPI statements, and LMS integration
3. **Modern Web Dashboard** - A Next.js 15 application for professors to create content, track student progress, and generate detailed analytics

The platform employs **adaptive learning algorithms** that dynamically adjust game difficulty based on student performance, ensuring an optimal challenge level for each learner.

### 🎓 Educational Philosophy

- **Learning by Doing**: Students learn programming concepts through interactive problem-solving
- **Personalized Paths**: AI adapts content difficulty in real-time based on performance
- **Immediate Feedback**: Automated code evaluation with constructive suggestions
- **Progress Visibility**: Teachers get detailed analytics on student engagement and achievement
- **Open Source**: Built transparently for educational institutions worldwide

### 👥 User Roles

| Role | Description | Access |
|------|-------------|--------|
| **Admin** | System administrator with full access | Dashboard, user management, system config |
| **Professor** | Teacher who creates content and monitors students | Course creation, student tracking, analytics |
| **Student** | Learner who plays games and solves puzzles | Game access, progress viewing, feedback |

---

## ✨ Features

### 🎮 Game Features
- **Visual Programming**: Block-based coding with drag-and-drop interface (if, while, execute, variables)
- **Adaptive Difficulty**: AI-driven difficulty scaling that learns from student performance
- **Interactive Narratives**: Story-driven contexts set in a magic & technology academy
- **Real-time Feedback**: Instant execution feedback with error detection
- **Offline Support**: Full game experience with local SQLite database
- **xAPI Tracking**: Comprehensive learning experience statements sent to backend
- **Multi-chapter Support**: Progressive level design with tutorial guidance

### 📊 Platform Features
- **User Management**: Role-based access control (admin, professor, student)
- **Course Management**: Create, organize, and publish learning content
- **Game Management**: Configure games, levels, and segments for professors
- **Progress Tracking**: Real-time monitoring of student activity and completion
- **Analytics Dashboard**: Comprehensive metrics on completion, time spent, and performance
- **Reports**: Export student progress and course analytics
- **LMS Integration**: Seamless integration with external learning management systems (Moodle, Canvas)
- **Teacher Settings**: Customizable configurations per professor

### 🔐 Backend Features
- **Async Architecture**: Full async/await support with SQLAlchemy 2.0
- **Database Migrations**: Alembic-managed schema versioning
- **Repository Pattern**: Clean separation of data access and business logic
- **Service/UseCase Pattern**: Clear separation between CRUD operations and business workflows
- **Error Handling**: Custom exception framework with proper HTTP status codes
- **OpenAPI Docs**: Auto-generated interactive API documentation (Swagger UI & ReDoc)
- **JWT Authentication**: Secure token-based auth with bcrypt password hashing
- **xAPI Support**: Full xAPI 1.0 implementation for learning analytics

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                        HELLO WORLD PLATFORM                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────┐          ┌──────────────────────┐       │
│  │  Frontend (Web)      │          │   Game (Godot 4.4)   │       │
│  │  Next.js 15.5        │          │   GDScript 2.0       │       │
│  │  React 19            │          │   Visual Blocks      │       │
│  │  TypeScript 5        │          │   SQLite (local)     │       │
│  └──────────┬───────────┘          └──────────┬───────────┘       │
│             │                                  │                   │
│             └──────────────┬───────────────────┘                   │
│                            │                                       │
│                       REST API (OpenAPI)                           │
│                   FastAPI + Async/Await                            │
│                            │                                       │
│  ┌─────────────────────────┼────────────────────────────┐          │
│  │                         ▼                            │          │
│  │  ┌──────────────────────────────────────────────┐   │           │
│  │  │   Backend Services (FastAPI)                 │   │           │
│  │  │  ──────────────────────────────────────────  │   │           │
│  │  │  • Auth (JWT, bcrypt, LMS credentials)       │   │           │
│  │  │  • Users (CRUD, roles, profiles)             │   │           │
│  │  │  • Games & Levels (content management)        │   │           │
│  │  │  • Statistics & Progress (analytics)          │   │           │
│  │  │  • Sync (offline/online synchronization)      │   │           │
│  │  │  • xAPI (learning experience statements)      │   │           │
│  │  └──────────────────────────────────────────────┘   │           │
│  │                         │                           │           │
│  │  ┌──────────────────────┼──────────────────────┐   │           │
│  │  │                      ▼                      │   │           │
│  │  │  ┌───────────────────────────────────┐      │   │           │
│  │  │  │  PostgreSQL 16 Database           │      │   │           │
│  │  │  │  (SQLAlchemy 2.0 Async + Alembic) │      │   │           │
│  │  │  │                                   │      │   │           │
│  │  │  │  • Users & Roles                  │      │   │           │
│  │  │  │  • Games & Levels                 │      │   │           │
│  │  │  │  • Progress & Feedback            │      │   │           │
│  │  │  │  • Sync Sessions & Events         │      │   │           │
│  │  │  │  • xAPI Statements                │      │   │           │
│  │  │  │  • LMS Credentials                │      │   │           │
│  │  │  └───────────────────────────────────┘      │   │           │
│  │  └─────────────────────────────────────────────┘   │           │
│  │                                                    │           │
│  └────────────────────────────────────────────────────┘           │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Key Components

#### Backend Services (`apps/backend/`)
- **Authentication Module**: JWT token generation, bcrypt password hashing, LMS credential management
- **User Service**: Account CRUD, role management, professor/student profile updates, teacher settings
- **Game Module**: Game and level management, segment configuration
- **Statistics Engine**: Progress aggregation, analytics computation, metric types
- **Sync Service**: Offline/online synchronization sessions and events
- **xAPI Implementation**: Full xAPI 1.0 statement tracking for learning experiences

#### Frontend Application (`apps/frontend/`)
- **Authentication**: Login/register pages with JWT cookie storage
- **Dashboard**: Real-time student progress monitoring
- **Course Management**: Intuitive UI for building courses and configuring games
- **Analytics Views**: Detailed performance metrics with Recharts visualizations
- **User Management**: Student enrollment and profile management
- **Settings**: Professor-specific configurations
- **Reports**: Export functionality for student progress data

#### Game Engine (`apps/game/`)
- **Execution Engine**: Interprets visual programming blocks (if, while, execute, variables)
- **Problem Context System**: Extensible domain-specific problem definitions
- **Block Library**: Pre-built and custom programming blocks
- **Adaptive Agent**: AI-driven difficulty adjustment based on student performance
- **Database Interface**: Local SQLite with sync to backend
- **Dialogue System**: Interactive narrative with Dialogue Manager plugin
- **Event Bus**: Signal-based communication between game components

#### Shared Packages
- **API Client** (`packages/api-client-ts/`): Auto-generated TypeScript client from OpenAPI spec
- **API Contract** (`packages/api-contract/`): OpenAPI JSON/YAML specification

---

## 💻 Tech Stack

### Backend
| Technology | Purpose | Version |
|-----------|---------|---------|
| **FastAPI** | Web framework | 0.115+ |
| **SQLAlchemy** | ORM (Async) | 2.0+ |
| **Alembic** | Schema migrations | 1.12+ |
| **PostgreSQL** | Primary database | 16 |
| **Pydantic** | Data validation | 2.0+ |
| **PyJWT** | Authentication | 2.8+ |
| **Passlib + Bcrypt** | Password hashing | Latest |
| **uv** | Package manager | Latest |
| **pytest** | Testing framework | Latest |

### Frontend
| Technology | Purpose | Version |
|-----------|---------|---------|
| **Next.js** | React framework (App Router) | 15.5.4 |
| **React** | UI library | 19.1.0 |
| **TypeScript** | Type safety | 5 |
| **Tailwind CSS** | Styling | 4 |
| **shadcn/ui** | Component library | Latest |
| **Zod** | Schema validation | 4 |
| **Zustand** | State management | 5 |
| **Recharts** | Charts & graphs | 2.15.4 |
| **@dnd-kit** | Drag & Drop | Latest |
| **Vitest** | Unit testing | Latest |
| **Playwright** | E2E testing | Latest |
| **pnpm** | Package manager | 10.4.1 |

### Game
| Technology | Purpose | Version |
|-----------|---------|---------|
| **Godot Engine** | Game engine | 4.4 |
| **GDScript 2.0** | Game scripting | 4.x |
| **SQLite** | Local storage | 3.x |
| **GUT Plugin** | Testing framework | Latest |
| **Dialogue Manager** | Narrative system | Latest |
| **godot-sqlite** | SQLite integration | Latest |

### Infrastructure
| Technology | Purpose |
|-----------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Local orchestration |
| **Turborepo** | Monorepo task running |
| **OpenAPI Generator** | API client generation |

---

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** 20.10+
- **Git** 2.30+
- **Node.js 18+ & pnpm 10+** (for local frontend development)
- **Python 3.12+ & uv** (for local backend development)
- **Godot 4.4** (for game development only)

### 1. Clone the Repository

```bash
git clone https://github.com/JohnyYen/hello-world-project.git
cd hello-world-project
```

### 2. Start with Docker Compose (Recommended)

```bash
# Start all services (backend, frontend, database)
pnpm run docker:up

# Or directly with docker compose
docker compose -f infraestructure/docker/docker-compose.dev.yml up -d --build

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Adminer (DB management): http://localhost:8081
```

### 3. Initial Setup

```bash
# Create first admin user and seed roles (backend container)
docker exec hello-world-backend uv run python -m src.shared.seed.run_seed

# Access backend shell if needed
docker compose -f infraestructure/docker/docker-compose.dev.yml \
  exec hello-world-backend bash
```

### 4. Login to Dashboard

Visit **http://localhost:3000** and login with admin credentials:
- **Email**: admin@example.com
- **Password**: adminpass123

### 5. Stop Services

```bash
pnpm run docker:down

# Or directly with docker compose
docker compose -f infraestructure/docker/docker-compose.dev.yml down
```

---

## 🛠️ Development Guide

### Root-Level Commands

```bash
# Start all services (Docker)
pnpm run dev

# Start backend only (local)
pnpm run dev:backend

# Start frontend only (local)
pnpm run dev:frontend

# Build frontend for production
pnpm run dev:frontend:prod

# View Docker logs
pnpm run docker:logs

# Generate API client from OpenAPI spec
pnpm run generate:api-client
```

### Backend Development

```bash
cd apps/backend

# Install dependencies
uv sync

# Run development server
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
uv run pytest

# Run specific test
uv run pytest tests/auth/test_login.py -v

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Database migrations
uv run alembic revision --autogenerate -m "Add user table"
uv run alembic upgrade head
uv run alembic downgrade -1

# Seed data (roles + admin user)
uv run python -m src.shared.seed.run_seed

# Lint code (if configured)
uv run black src/
uv run ruff check src/
```

**Backend API Structure:**
- All routes follow RESTful conventions
- Pattern: Service (CRUD) + UseCase (Business Logic)
- One endpoint per file in `src/{domain}/api/v1/endpoints/`
- Response format: Standardized with Pydantic models
- Error format: `{ "detail": "error message", "code": "ERROR_CODE" }`
- Full API docs available at `/docs` (Swagger UI) and `/redoc`

**Key Endpoints:**
```
POST   /api/v1/auth/register       # Register (professor auto-assigned)
POST   /api/v1/auth/login          # Login (returns JWT)
POST   /api/v1/auth/change-password # Change password
GET    /api/v1/users/              # List users (paginated)
GET/PUT/DELETE /api/v1/users/{id}  # User CRUD
GET/POST/PUT/DELETE /api/v1/games/ # Game management
GET/POST/PUT/DELETE /api/v1/levels/ # Level management
POST   /api/v1/sync/sessions       # Create sync session
POST   /api/v1/sync/events         # Register sync event
POST   /api/v1/statements/xapi     # Send xAPI statement
```

### Frontend Development

```bash
cd apps/frontend

# Install dependencies
pnpm install

# Run development server (with Turbopack)
pnpm run dev

# Build for production
pnpm run build

# Start production server
pnpm run start

# Run linter
pnpm run lint

# Type checking
pnpm run typecheck

# Run unit tests
pnpm run test

# Run tests in watch mode
pnpm run test:watch

# Run tests with coverage
pnpm run test:coverage

# Run E2E tests
pnpm run test:e2e
```

**Frontend Conventions:**
- Server Components by default, `"use client"` only when needed
- Tailwind CSS with `cn()` utility for conditional classes
- Server Actions for all mutations
- Zod validation for all forms
- Spanish UI text
- No `useMemo`/`useCallback` (React Compiler)
- Explicit return types on all functions
- `interface` over `type` for objects
- API calls via `@workspace/api-client-ts` package

**Key Routes:**
```
/                       # Landing page
/login                  # User login
/register               # Professor registration
/dashboard              # Main dashboard
/admin                  # Admin panel
/docs                   # Documentation
/settings               # Professor settings
/reports                # Student progress reports
```

### Game Development

1. **Open in Godot Editor**
   ```bash
   cd apps/game
   godot -e .  # Opens editor (requires Godot 4.4)
   ```

2. **Run Game**
   - Press F5 or click "Play" in editor
   - Select `main.tscn` as main scene

3. **Run Tests**
   - In editor: Project → Project Tools → GUT Panel → Run All
   - Or CLI: `godot --headless -s addons/gut/gut_cmdline.gd -gdir=res://test/`

4. **Build Executable**
   ```bash
   # In Godot editor:
   # Project → Export → Select profile → Export
   ```

5. **Code Conventions**
   - Explicit type hints on all variables and functions
   - `class_name` to register global classes
   - 4-space indentation
   - Signal-based communication between nodes
   - Repository pattern for SQLite operations
   - Spanish UI text

---

## 🔄 Running Complete Development Environment

### Using Docker Compose (Recommended)

```bash
# Start everything
pnpm run docker:up

# View logs
pnpm run docker:logs

# Stop services
pnpm run docker:down

# Rebuild specific service
docker compose -f infraestructure/docker/docker-compose.dev.yml up -d --build hello-world-backend
```

### Services Overview

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | Next.js 15 web application |
| Backend | 8000 | FastAPI REST API |
| PostgreSQL | 5432 | Primary database |
| Adminer | 8081 | Database management UI (phpMyAdmin alternative) |

---

## 📦 Monorepo Structure

```
hello-world-project/
├── apps/
│   ├── backend/              # FastAPI REST API (Python)
│   ├── frontend/             # Next.js 15 dashboard (TypeScript)
│   └── game/                 # Godot 4.4 educational game (GDScript)
├── packages/
│   ├── api-client-ts/        # Auto-generated TypeScript client
│   └── api-contract/         # OpenAPI specification
├── infraestructure/
│   └── docker/               # Docker Compose configurations
├── docs/                     # Documentation (ADR, SDD, etc.)
├── .agents/skills/           # AI skills for development
├── scripts/                  # Utility scripts
└── package.json              # Root package (pnpm workspace)
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how to get started:

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/hello-world-project.git
cd hello-world-project
```

### 2. Create Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 3. Follow Code Guidelines

**Python (Backend):**
- PEP 8 compliant
- Type hints required
- Async/await for I/O operations
- Service/UseCase pattern enforced
- UUIDv4 for all primary keys
- One endpoint per file

**TypeScript (Frontend):**
- ESLint configuration enforced
- Server Components by default
- Server Actions for mutations
- Zod validation for forms
- Spanish UI text
- Explicit return types
- `interface` over `type`

**GDScript (Game):**
- `snake_case` for functions and variables
- `PascalCase` for classes
- 4-space indentation
- Explicit type hints required
- Signal-based communication
- Repository pattern for database

### 4. Make Changes and Test

```bash
# Backend tests
cd apps/backend && uv run pytest

# Frontend tests
cd apps/frontend && pnpm run test

# Game tests (GUT)
# Open in Godot and run GUT tests
```

### 5. Commit with Conventional Commits

```bash
git commit -m "feat: add new adaptive algorithm for difficulty scaling"
git commit -m "fix: resolve JWT token expiration issue"
git commit -m "docs: update API documentation"
git commit -m "refactor: extract service from usecase"
git commit -m "test: add integration tests for sync module"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/amazing-feature
```

Then open a Pull Request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots (if UI changes)
- Test results

### Development Workflow

1. Read [AGENTS.md](./AGENTS.md) for detailed guidelines
2. Check existing issues for duplicates
3. Test locally before submitting PR
4. Ensure all CI checks pass
5. Request review from maintainers

---

## 📖 Documentation

### Component Documentation
- [Backend README](./apps/backend/README.md) - API documentation, architecture, database design
- [Frontend README](./apps/frontend/README.md) - UI development guide, conventions, testing
- [Game README](./apps/game/README.md) - Game architecture, GDScript conventions, GUT testing

### Technical Documentation
- [Backend Database Design](./apps/backend/docs/database-design.md) - ER diagrams, table schemas
- [Backend User Stories](./apps/backend/docs/user_stories.md) - User requirements
- [Backend Glossary](./apps/backend/GP.md) - Terminology reference
- [Game Level 1 Roadmap](./apps/game/LEVEL_1_DEVELOPMENT_ROADMAP.md) - Development plan
- [Game Adaptive Agent](./apps/game/docs/adaptive_agent.md) - AI difficulty adjustment
- [Frontend Performance](./apps/frontend/PERFORMANCE_OPTIMIZATION.md) - Optimization guide

### API Documentation
- [API Contract](./packages/api-contract/openapi.json) - OpenAPI specification
- [API Client Docs](./packages/api-client-ts/) - TypeScript client documentation
- [Live Swagger UI](http://localhost:8000/docs) - Available when backend is running

### Development Guidelines
- [Root AGENTS.md](./AGENTS.md) - Cross-project AI agent guidelines
- [Backend AGENTS.md](./apps/backend/AGENTS.md) - Backend-specific rules
- [Frontend AGENTS.md](./apps/frontend/AGENTS.md) - Frontend-specific rules
- [Game AGENTS.md](./apps/game/AGENTS.md) - Game-specific rules

---

## 🐛 Bug Reports and Features

### Report a Bug

Open an issue with:
- Clear title describing the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/logs (if applicable)
- Environment details

### Request a Feature

Open an issue with:
- Clear title
- Problem statement (what problem does this solve?)
- Proposed solution
- Alternative approaches considered
- Any relevant mockups or examples

---

## 📊 Project Statistics

- **Languages**: Python 3.12, TypeScript 5, GDScript 2.0
- **Backend**: 50+ API endpoints, Clean Architecture with Service/UseCase pattern
- **Frontend**: 40+ React components, App Router with Server Actions
- **Game**: 20+ scenes, visual programming engine with adaptive difficulty
- **Database**: 15+ tables for complete education platform
- **Testing**: pytest (backend), Vitest + Playwright (frontend), GUT (game)
- **Packages**: Auto-generated TypeScript client from OpenAPI spec

---

## 🎓 Learning Resources

### For Contributors
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Next.js 15 App Router](https://nextjs.org/docs/app)
- [React 19](https://react.dev/)
- [Godot 4 Documentation](https://docs.godotengine.org/en/stable/)
- [xAPI Specification](https://xapi.com/)

### For Users
- [Backend User Stories](./apps/backend/docs/user_stories.md)
- [Game Tutorial Dialogues](./apps/game/dialogue/Tutorial/)
- [Frontend Documentation](http://localhost:3000/docs) (when running)

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](./LICENSE) file for details.

Permissions:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

Limitations:
- ❌ Liability
- ❌ Warranty

---

## 👥 Contributors

### Contributors
See [CONTRIBUTORS.md](./CONTRIBUTORS.md) for the full list of amazing people who have contributed to this project.

---

## 🤔 FAQ

**Q: Can I use this in production?**
A: Yes! The platform is designed for production use. Configure environment variables and follow deployment best practices.

**Q: Is the game available standalone?**
A: Yes, the Godot game can run independently with local SQLite, but syncing with backend enables progress tracking and analytics.

**Q: What's the minimum database version?**
A: PostgreSQL 16 with ~500MB initial storage; grows with user data.

**Q: Can I customize the game content?**
A: Absolutely! The game is fully extensible - modify scenes, add new problem contexts, and define custom blocks.

**Q: How do I self-host this?**
A: Use Docker Compose with the provided configuration. See `infraestructure/docker/docker-compose.dev.yml`.

**Q: How are API changes synchronized?**
A: The TypeScript client is auto-generated from the OpenAPI spec. Run `pnpm run generate:api-client` after backend changes.

**Q: What's the adaptive difficulty algorithm?**
A: The game uses an Adaptive Agent that analyzes student performance (completion time, errors, hints used) to adjust puzzle complexity in real-time.

---

## 📞 Support and Community

- **Issues**: [GitHub Issues](https://github.com/JohnyYen/hello-world-project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JohnyYen/hello-world-project/discussions)

---

## 🌟 Show Your Support

Give us a ⭐ if this project helped you! We'd love to see what you're building.

---

**Made with ❤️ for educators and learners everywhere.**
