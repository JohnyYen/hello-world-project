# 🎮 Hello World Project

> An **intelligent, game-based learning platform** for teaching programming fundamentals through interactive visual programming, adaptive educational narratives, and real-time performance tracking.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org)
[![Godot 4.x](https://img.shields.io/badge/Godot-4.x-blue.svg)](https://godotengine.org)
[![Monorepo: Turborepo](https://img.shields.io/badge/Monorepo-Turborepo-brightgreen.svg)](https://turbo.build)

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

1. **Visual Programming Game** - An adaptive Godot 4.x game where students solve real-world problems using visual programming blocks
2. **Intelligent Backend API** - A FastAPI async server managing users, courses, progress tracking, and AI-driven difficulty adaptation
3. **Modern Web Dashboard** - A Next.js 15 application for professors to create content, track student progress, and generate detailed analytics

The platform employs **adaptive learning algorithms** that dynamically adjust game difficulty based on student performance, ensuring an optimal challenge level for each learner.

### 🎓 Educational Philosophy

- **Learning by Doing**: Students learn programming concepts through interactive problem-solving
- **Personalized Paths**: AI adapts content difficulty in real-time based on performance
- **Immediate Feedback**: Automated code evaluation with constructive suggestions
- **Progress Visibility**: Teachers get detailed analytics on student engagement and achievement
- **Open Source**: Built transparently for educational institutions worldwide

---

## ✨ Features

### 🎮 Game Features
- **Visual Programming**: Block-based coding with drag-and-drop interface
- **Adaptive Difficulty**: AI-driven difficulty scaling that learns from student performance
- **Interactive Narratives**: Story-driven contexts that make problems engaging
- **Real-time Feedback**: Instant execution feedback with error detection
- **Offline Support**: Full game experience with local SQLite database
- **Multi-language Support**: Extensible architecture for international content

### 📊 Platform Features
- **User Management**: Role-based access (Professor, Student, Admin)
- **Course Management**: Create, organize, and publish learning content
- **Progress Tracking**: Real-time monitoring of student activity and completion
- **Analytics Dashboard**: Comprehensive metrics on completion, time spent, and performance
- **LMS Integration**: Seamless integration with external learning management systems
- **Authentication**: Secure JWT-based authentication with password hashing

### 🔐 Backend Features
- **Async Architecture**: Full async/await support with SQLAlchemy 2.0
- **Database Migrations**: Alembic-managed schema versioning
- **Repository Pattern**: Clean separation of data access and business logic
- **Error Handling**: Custom exception framework with proper HTTP status codes
- **OpenAPI Docs**: Auto-generated interactive API documentation

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌────────────────────────────────────────────────────────────┐
│                    HELLO WORLD PLATFORM                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Frontend (Web)  │      │   Game (Godot)   │            │
│  │  Next.js 15      │      │   4.x + AI Agent │            │
│  │  TypeScript      │      │   Visual Blocks  │            │
│  └────────┬─────────┘      └────────┬─────────┘            │
│           │                         │                      │
│           └────────────┬────────────┘                      │
│                        │                                   │
│                   REST API                                 │
│              (FastAPI + OpenAPI)                           │
│                        │                                   │
│  ┌─────────────────────┼────────────────────┐              │
│  │                     ▼                    │              │
│  │  ┌──────────────────────────────────┐   │               │
│  │  │   Backend Services (FastAPI)     │   │               │
│  │  │  ─────────────────────────────   │   │               │
│  │  │  • Authentication & Auth         │   │               │
│  │  │  • User Management               │   │               │
│  │  │  • Course Management             │   │               │
│  │  │  • Progress Tracking             │   │               │
│  │  │  • Statistics & Analytics        │   │               │
│  │  │  • Game Sync Service             │   │               │
│  │  └──────────────────────────────────┘   │               │
│  │                     │                   │               │
│  │  ┌──────────────────┼────────────────┐  │               │
│  │  │                  ▼                │  │               │
│  │  │  ┌──────────────────────────┐     │  │               │
│  │  │  │  PostgreSQL Database     │     │  │               │
│  │  │  │  (SQLAlchemy + Alembic)  │     │  │               │
│  │  │  └──────────────────────────┘     │  │               │
│  │  │                                   │  │               │
│  │  └───────────────────────────────────┘  │               │
│  │                                         │               │
│  └─────────────────────────────────────────┘               │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Key Components

#### Backend Services
- **Authentication Module**: JWT token generation, password hashing (bcrypt)
- **User Service**: Account creation, role management, profile updates
- **Game Sync Service**: Real-time game state synchronization
- **Statistics Engine**: Progress aggregation and analytics computation
- **Adaptive Agent**: AI-driven difficulty adjustment algorithm

#### Frontend Application
- **Dashboard**: Real-time student progress monitoring
- **Content Creation**: Intuitive UI for building courses
- **Analytics Views**: Detailed performance metrics and charts
- **User Management**: Student enrollment and profile management

#### Game Engine
- **Execution Engine**: Interprets visual programming blocks
- **Problem Context System**: Extensible domain-specific problem definitions
- **Block Library**: Pre-built and custom programming blocks
- **Database Interface**: Local SQLite with sync to backend

---

## 💻 Tech Stack

### Backend
| Technology | Purpose | Version |
|-----------|---------|---------|
| **FastAPI** | Web framework | 0.100+ |
| **SQLAlchemy** | ORM | 2.0+ |
| **Alembic** | Schema migrations | 1.12+ |
| **PostgreSQL** | Primary database | 13+ |
| **Pydantic** | Data validation | 2.0+ |
| **PyJWT** | Authentication | 2.8+ |
| **Passlib** | Password hashing | 1.7+ |
| **Uvicorn** | ASGI server | 0.23+ |

### Frontend
| Technology | Purpose | Version |
|-----------|---------|---------|
| **Next.js** | React framework | 15+ |
| **React** | UI library | 19+ |
| **TypeScript** | Type safety | 5.3+ |
| **Tailwind CSS** | Styling | 3.3+ |
| **Radix UI** | Component library | Latest |
| **Axios** | HTTP client | 1.6+ |

### Game
| Technology | Purpose | Version |
|-----------|---------|---------|
| **Godot Engine** | Game engine | 4.x |
| **GDScript 2.0** | Game scripting | 4.x |
| **SQLite** | Local storage | 3.x |
| **GUT Plugin** | Testing framework | Latest |

### Infrastructure
| Technology | Purpose |
|-----------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Orchestration |
| **Turborepo** | Monorepo management |
| **pnpm** | Package manager |

---

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** 20.10+
- **Git** 2.30+
- **Node.js & pnpm** (for local frontend development)
- **Python 3.11+** (for local backend development)
- **Godot 4.x** (for game development only)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hello-world-project.git
cd hello-world-project
```

### 2. Start with Docker Compose

```bash
# Start all services (backend, frontend, database)
docker compose -f infraestructure/docker/docker-compose.dev.yml up -d --build

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### 3. Initial Setup

```bash
# Create first admin user (backend container)
docker exec hello-world-backend python -c \
  "from src.core.database import init_admin_user; init_admin_user()"

# Or access backend shell
docker compose -f infraestructure/docker/docker-compose.dev.yml \
  exec hello-world-backend bash
```

### 4. Login to Dashboard

Visit **http://localhost:3000** and login with admin credentials:
- **Email**: admin@example.com
- **Password**: (set during initial setup)

### 5. Stop Services

```bash
docker compose -f infraestructure/docker/docker-compose.dev.yml down
```

---

## 📁 Project Structure

```
hello-world-project/
├── apps/
│   ├── backend/                    # FastAPI backend service
│   │   ├── src/
│   │   │   ├── api/               # API route handlers
│   │   │   ├── auth/              # Authentication logic
│   │   │   ├── core/              # Configuration and constants
│   │   │   ├── db/
│   │   │   │   ├── models/        # SQLAlchemy models
│   │   │   │   ├── repositories/  # Data access layer
│   │   │   │   └── session.py     # DB connection
│   │   │   ├── services/          # Business logic
│   │   │   ├── game/              # Game-related endpoints
│   │   │   ├── statistic/         # Analytics service
│   │   │   ├── users/             # User management
│   │   │   └── shared/            # Shared utilities
│   │   ├── migrations/            # Alembic database migrations
│   │   ├── tests/                 # Test suite
│   │   ├── docs/                  # Documentation
│   │   ├── main.py               # Application entry point
│   │   ├── requirements.txt       # Python dependencies
│   │   └── Dockerfile.dev        # Development container
│   │
│   ├── frontend/                   # Next.js web dashboard
│   │   ├── src/
│   │   │   ├── app/              # Next.js 15 App Router
│   │   │   ├── components/       # React components
│   │   │   ├── hooks/            # Custom React hooks
│   │   │   ├── services/         # API client services
│   │   │   ├── types/            # TypeScript interfaces
│   │   │   ├── adapters/         # External integrations
│   │   │   └── lib/              # Utilities
│   │   ├── public/               # Static assets
│   │   ├── package.json          # Dependencies
│   │   └── Dockerfile.dev        # Development container
│   │
│   └── game/                       # Godot 4.x educational game
│       ├── scripts/               # GDScript files
│       │   ├── engine/           # Game execution engine
│       │   ├── agents/           # AI adaptive agents
│       │   ├── blocks/           # Programming blocks
│       │   ├── controllers/      # Scene controllers
│       │   └── database/         # SQLite interface
│       ├── scenes/               # Godot scenes
│       ├── models/               # Data models
│       ├── assets/               # Art, sounds, fonts
│       ├── dialogue/             # Dialogue scripts
│       ├── config/               # Game configuration
│       ├── test/                 # GUT test suite
│       ├── addons/               # Godot plugins
│       └── project.godot         # Godot project file
│
├── infraestructure/
│   └── docker/
│       └── docker-compose.dev.yml     # Development environment
│
├── docs/                          # Project documentation
├── scripts/                       # Utility scripts
├── package.json                   # Monorepo root
├── pnpm-workspace.yaml           # pnpm workspace config
├── turbo.json                    # Turborepo configuration
└── AGENTS.md                     # CodeAI agent guidelines

```

---

## 🛠️ Development Guide

### Backend Development

```bash
cd apps/backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000

# Run tests
pytest

# Run specific test
pytest tests/auth/test_login.py -v

# Lint code
black src/
flake8 src/

# Database migrations
alembic revision --autogenerate -m "Add user table"
alembic upgrade head
alembic downgrade -1

# Auto-generate OpenAPI schema
python -c "from main import app; import json; print(json.dumps(app.openapi(), indent=2))"
```

**Backend API Structure:**
- All routes follow RESTful conventions
- Response format: `{ "data": {...}, "meta": {...} }`
- Error format: `{ "detail": "error message", "code": "ERROR_CODE" }`
- Full API docs available at `/docs` (Swagger UI)

### Frontend Development

```bash
cd apps/frontend

# Install dependencies
pnpm install

# Run development server (with Turbopack)
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Run linter
pnpm lint

# Type checking
pnpm tsc --noEmit
```

**Frontend Conventions:**
- Use functional components with TypeScript
- Tailwind CSS for styling with `cn()` utility
- Radix UI for accessible components
- API calls via `/src/services/`

### Game Development

1. **Open in Godot Editor**
   ```bash
   cd apps/game
   godot -e .  # Opens editor
   ```

2. **Run Tests**
   - In editor: Scene → GUT → Run All Tests
   - Select test file for single test

3. **Build Executable**
   ```bash
   # In Godot editor:
   # Project → Export → Select profile → Export
   ```

4. **Code Structure**
   - Models in `models/`
   - Controllers in `scripts/controllers/`
   - Scenes in `scenes/`
   - Tests in `test/unit/` and `test/integrations/`

---

## 🔄 Running Complete Development Environment

### Using Docker Compose (Recommended)

```bash
# Start everything
docker compose -f infraestructure/docker/docker-compose.dev.yml up -d

# View logs
docker compose -f infraestructure/docker/docker-compose.dev.yml logs -f

# Stop services
docker compose -f infraestructure/docker/docker-compose.dev.yml down

# Rebuild specific service
docker compose -f infraestructure/docker/docker-compose.dev.yml up -d --build hello-world-backend
```

### Services Overview

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | Next.js web application |
| Backend | 8000 | FastAPI REST API |
| PostgreSQL | 5432 | Primary database |
| Adminer | 8081 | Database management UI |

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
- Docstrings for classes and complex functions

**TypeScript (Frontend):**
- ESLint configuration enforced
- Functional components only
- Proper error boundaries
- Component prop interfaces

**GDScript (Game):**
- `snake_case` for functions and variables
- `PascalCase` for classes
- 4-space indentation
- Type hints on function signatures

### 4. Make Changes and Test

```bash
# Backend tests
cd apps/backend && pytest

# Frontend tests (if configured)
cd apps/frontend && npm test

# Game tests
# Open in Godot and run GUT tests
```

### 5. Commit with Conventional Commits

```bash
git commit -m "feat: add new adaptive algorithm for difficulty scaling"
git commit -m "fix: resolve JWT token expiration issue"
git commit -m "docs: update API documentation"
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

- [Backend README](./apps/backend/README.md) - API documentation
- [Frontend README](./apps/frontend/README.md) - UI development guide
- [Game README](./apps/game/README.md) - Game architecture
- [Architecture Decision Records](./docs/adr/) - Technical decisions
- [API Specification](./apps/backend/PROJECT_SPEC.md) - Complete API specs

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

- **Languages**: Python, TypeScript, GDScript
- **Components**: 50+ API endpoints, 30+ React components, 20+ Game scenes
- **Test Coverage**: 70%+ (backend), extensible test suite
- **Database**: 20+ tables for complete education platform

---

## 🎓 Learning Resources

### For Contributors
- [FastAPI Advanced Patterns](./docs/backend-patterns.md)
- [Next.js 15 Best Practices](./docs/frontend-patterns.md)
- [Godot 4 Architecture Guide](./docs/game-architecture.md)
- [API Design Standards](./docs/api-standards.md)

### For Users
- [Getting Started Tutorial](https://example.com/tutorial)
- [Teacher Guide](https://example.com/teacher-guide)
- [Student Guide](https://example.com/student-guide)

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

## 👥 Authors and Contributors

### Core Team
- **Project Lead**: [Your Name](https://github.com/yourusername)
- **Backend Architect**: [Backend Lead](https://github.com/backend-lead)
- **Frontend Lead**: [Frontend Lead](https://github.com/frontend-lead)
- **Game Designer**: [Game Lead](https://github.com/game-lead)

### Contributors
See [CONTRIBUTORS.md](./CONTRIBUTORS.md) for the full list of amazing people who have contributed to this project.

---

## 🤔 FAQ

**Q: Can I use this in production?**
A: Yes! The platform is designed for production use. Follow the deployment guide in docs/.

**Q: Is the game available standalone?**
A: Yes, the Godot game can run independently but syncs better with the backend.

**Q: What's the minimum database size?**
A: PostgreSQL 13+ with ~500MB initial storage; grows with user data.

**Q: Can I customize the game content?**
A: Absolutely! The game is fully extensible - modify scenes, add new problem contexts, and define custom blocks.

**Q: How do I self-host this?**
A: See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for complete self-hosting guide.

---

## 📞 Support and Community

- **Issues**: [GitHub Issues](https://github.com/yourusername/hello-world-project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/hello-world-project/discussions)
- **Email**: support@example.com
- **Discord**: [Join our community](https://discord.gg/example)

---

## 🌟 Show Your Support

Give us a ⭐ if this project helped you! We'd love to see what you're building.

---

**Made with ❤️ for educators and learners everywhere.**
