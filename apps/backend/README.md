# Hello World Backend ⚡

[![PRD](https://img.shields.io/badge/PRD-v0.1.0--draft-blue)](PRD.md)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009989)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Package Manager](https://img.shields.io/badge/uv-FAST-brightgreen)](https://github.com/astral-sh/uv)

**Hello World Backend** es el **backbone inteligente** de la plataforma Hello World: una API REST en **FastAPI** con Clean Architecture que garantiza integridad de datos, escalabilidad horizontal y cumplimiento de estándares educativos (xAPI 1.0). Sirve a tres tipos de cliente — el motor de juego (Godot), el panel del profesor (Next.js) y los sistemas LMS institucionales (Moodle, Canvas) — con autenticación JWT, gestión de usuarios, almacenamiento de progreso y sincronización de datos.

## 📋 Descripción

Hello World Backend es la **columna vertebral** de la plataforma educativa Hello World. Actúa como capa de integración invisible que garantiza que cada interacción de aprendizaje — desde que un estudiante conecta un bloque visual hasta que un profesor exporta un informe — sea almacenada con integridad, procesada con eficiencia y accesible bajo estándares abiertos.

El sistema sirve a **tres tipos de cliente**:

- **Game (Godot 4.4)**: Autenticación de estudiantes, entrega de configuraciones de niveles, sincronización offline, statements xAPI
- **Frontend (Next.js 15)**: CRUD de contenido, agregación de progreso, reportes, gestión de usuarios
- **LMS Externos (Moodle, Canvas)**: Sincronización bidireccional, grade passback, importación de matriculaciones

Usuarios del sistema:

- **Profesores**: Crear y gestionar contenidos de aprendizaje, videojuegos y niveles
- **Estudiantes**: Interactuar con videojuegos en tiempo real
- **Administración**: Herramientas de seguimiento, análisis y sincronización de progreso

---

## 🎯 Contexto del Producto

El backend es una API REST **stateless** diseñada para servir a tres clientes con necesidades distintas:

- **Game (Godot 4.4)**: Autenticación, entrega de niveles, sync offline, statements xAPI — prioriza throughput y baja latencia
- **Frontend (Next.js 15)**: CRUD de contenido, reportes de progreso, gestión de usuarios — prioriza flexibilidad de consultas y paginación
- **LMS (Moodle, Canvas)**: Integración standards-compliant (LTI 1.3), sync bidireccional batch — prioriza consistencia transaccional

Para soportar esta heterogeneidad se adoptó **Clean Architecture**: dependencias hacia adentro (el dominio no sabe de infraestructura), casos de uso para lógica multi-servicio, repositorios para abstraer persistencia. Cada cliente evoluciona su capa API sin afectar las reglas de negocio compartidas.

---

## 🚀 Características Principales

### P0 — MVP/GA Critical
- **Autenticación JWT** (F-AUTH): Register/login/change-password con bcrypt cost 12, expiración 30 min
- **CRUD de Usuarios + RBAC** (F-USERS): admin/professor/student con soft delete, asignación automática de roles
- **CRUD de Juegos y Niveles** (F-GAMES): Catálogo de contenido educativo con segmentos y soft delete en cascada
- **Sincronización Offline** (F-SYNC): Pipeline con idempotencia, batch hasta 50 eventos, dead-letter queue
- **Tracking de Progreso** (F-STATS): Métricas por segmento, agregación por estudiante/juego/curso, exportación CSV
- **Statements xAPI** (F-XAPI): Recepción y almacenamiento de statements xAPI 1.0 con soporte JSONB

### P1 — Post-MVP
- **Feedback API** (F-FEEDBACK): Rating 1–5 con estadísticas agregadas y tendencias temporales
- **Game Instances** (F-GAME-INSTANCE): Ciclo de vida de sesiones de juego (active → completed/abandoned)
- **Credenciales LMS** (F-LMS-CRED): Gestión de credenciales para Moodle/Canvas con OAuth
- **Sincronización LMS** (F-LMS-SYNC): Importación/exportación bidireccional con partial success

### P2 — Futuro
- **WebSockets** (F-WS): Actualizaciones en tiempo real para monitoreo de aula en vivo
- **Exportación Masiva** (F-EXPORT): Datos institucionales en CSV/JSON con filtros

### Transversales
- **Clean Architecture**: Separación en capas API → Application → Domain → Infrastructure con inversión de dependencias
- **PostgreSQL Async**: SQLAlchemy 2.0 asíncrono, UUIDv4 en PKs, soft delete obligatorio
- **Validación Pydantic v2**: Schemas con regex, custom validators, documentación Swagger automática
- **Patrón Repository + DI**: Repositorios que abstraen persistencia, inyección con `Depends()` de FastAPI
- **Documentación API**: Swagger UI y ReDoc generados automáticamente

---

## 📂 Estructura del Proyecto

```
hello-world-backend/
├── src/
│   ├── auth/                    # Módulo de autenticación
│   │   ├── api/v1/
│   │   │   ├── endpoints/       # Endpoints: login, register, change-password, LMS
│   │   │   ├── schemas/         # Esquemas Pydantic
│   │   │   └── dependencies.py  # Dependencias de autenticación
│   │   ├── application/
│   │   │   ├── service/         # Servicios de autenticación
│   │   │   └── usecase/         # Casos de uso: RegisterUser, Authenticate, ChangePassword
│   │   ├── infrastructure/
│   │   │   ├── security.py      # JWT, bcrypt, hashing
│   │   │   └── lms_credential_repository.py
│   │   └── domain/
│   │       └── lms_credential.py
│   │
│   ├── users/                   # Módulo de usuarios
│   │   ├── api/v1/
│   │   │   ├── endpoints/       # Endpoints CRUD de usuarios
│   │   │   └── schemas/         # Esquemas User, Student, Professor
│   │   ├── application/
│   │   │   └── service/         # UserService
│   │   ├── infrastructure/
│   │   │   ├── user_repository.py
│   │   │   ├── role_repository.py    # NUEVO
│   │   │   └── user_repository_generic.py
│   │   └── domain/
│   │       ├── user.py
│   │       ├── role.py
│   │       ├── student.py
│   │       ├── professor.py
│   │       └── teacher_settings.py
│   │
│   ├── game/                    # Módulo de videojuegos
│   │   ├── api/v1/
│   │   │   ├── endpoints/       # Endpoints CRUD de juegos, niveles
│   │   │   └── schemas/
│   │   ├── application/
│   │   │   └── service/
│   │   ├── infrastructure/
│   │   └── domain/
│   │       ├── game.py
│   │       ├── level.py
│   │       └── segment_level.py
│   │
│   ├── statistic/               # Módulo de estadísticas y progreso
│   │   ├── api/v1/
│   │   │   ├── endpoints/
│   │   │   └── schemas/
│   │   ├── application/
│   │   │   └── service/
│   │   ├── infrastructure/
│   │   └── domain/
│   │       ├── progress.py
│   │       ├── sync_session.py
│   │       ├── sync_event.py
│   │       ├── feedback.py
│   │       └── metric_type.py
│   │
│   ├── sync/                    # Módulo de sincronización
│   │   ├── api/v1/
│   │   │   ├── endpoints/       # Endpoints de sincronización
│   │   │   └── schemas/
│   │   ├── application/
│   │   │   └── service/
│   │   ├── infrastructure/
│   │   └── domain/
│   │
│   ├── shared/                  # Código compartido
│   │   ├── api/
│   │   │   ├── schemas/
│   │   │   │   ├── base.py      # ResponseSchema, DateTimeSchema
│   │   │   │   └── pagination.py # Paginación
│   │   │   └── routes.py        # Configuración de rutas API
│   │   ├── application/
│   │   │   └── usecase/
│   │   │       └── base_service.py
│   │   ├── domain/
│   │   │   └── exceptions.py    # Excepciones personalizadas
│   │   ├── infrastructure/
│   │   │   ├── config.py        # Settings
│   │   │   ├── session.py       # Database session
│   │   │   ├── base.py          # Base model
│   │   │   └── repositories/
│   │   │       └── base_repository.py
│   │   ├── seed/
│   │   │   ├── run_seed.py      # Ejecutar seeds
│   │   │   ├── seed_roles.py    # Roles: admin, professor, student
│   │   │   └── seed_admin.py    # Usuario admin
│   │   └── deps.py              # Dependencias globales (get_current_user)
│   │
│   └── main.py                  # Punto de entrada
│
├── migrations/                  # Migraciones de base de datos (Alembic)
├── tests/                       # Pruebas unitarias y de integración
├── docs/                        # Documentación del proyecto
├── .env.example                 # Variables de entorno ejemplo
├── .gitignore
├── Dockerfile.dev               # Dockerfile para desarrollo
├── pyproject.toml               # Configuración de dependencias
├── alembic.ini                  # Configuración de Alembic
├── AGENTS.md                    # Guía para agentes IA
└── README.md
```

---

## 📊 Estado del Proyecto

| Funcionalidad | ID PRD | Prioridad | Estado |
|--------------|--------|-----------|--------|
| Autenticación JWT | F-AUTH | P0 | ✅ Implementado |
| CRUD Usuarios + Roles | F-USERS | P0 | ✅ Implementado |
| CRUD Juegos y Niveles | F-GAMES | P0 | ✅ Implementado |
| Sincronización Offline | F-SYNC | P0 | ✅ Implementado |
| Tracking de Progreso | F-STATS | P0 | 🟡 Parcial |
| Statements xAPI | F-XAPI | P0 | 🟡 Parcial |
| Feedback API | F-FEEDBACK | P1 | ❌ Pendiente |
| Game Instances | F-GAME-INSTANCE | P1 | ❌ Pendiente |
| Credenciales LMS | F-LMS-CRED | P1 | 🟡 Parcial |
| Sincronización LMS | F-LMS-SYNC | P1 | ❌ Pendiente |
| WebSockets | F-WS | P2 | ❌ Pendiente |
| Exportación Masiva | F-EXPORT | P2 | ❌ Pendiente |

*Consulta el [PRD](PRD.md) para el detalle completo de requisitos, escenarios de error y criterios de aceptación.*

---

## 🛠️ Requisitos Previos

- **Python 3.11+**
- **uv** (gestor de paquetes recomendado)
- **Docker** (opcional)
- **Git**

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
cd /path/to/hello-world-project
```

### 2. Instalar dependencias con uv

```bash
cd apps/hello-world-backend
uv sync
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus valores
```

### 4. Ejecutar seeds (roles y usuario admin)

```bash
uv run python -m src.shared.seed.run_seed
```

### 5. Iniciar la aplicación

```bash
# Desarrollo
uv run uvicorn main:app --reload

# Producción
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### 6. Acceder a la documentación

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🔐 Autenticación

### Sistema de Roles

El sistema tiene tres roles con asignación automática:

| Rol | Asignación | Endpoint |
|-----|------------|----------|
| `admin` | Solo vía seed | Sistema |
| `professor` | Registro automático | `POST /api/v1/auth/register` |
| `student` | Profesor crea estudiante | US-004 |

### Endpoints de Autenticación

#### 1. Registro de Usuario (Professor)
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "juan_profe",
  "email": "juan@example.com",
  "password": "Password123!"
}
```
**Nota:** El rol `professor` se asigna automáticamente. No enviar `role_id`.

**Respuesta:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 30,
  "user": {
    "id": 1,
    "username": "juan_profe",
    "email": "juan@example.com",
    "role": { "id": 2, "name": "professor" }
  }
}
```

#### 2. Inicio de Sesión
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=juan@example.com&password=Password123!
```

#### 3. Cambio de Contraseña
```http
POST /api/v1/auth/change-password
Authorization: Bearer <token>

{
  "current_password": "Password123!",
  "new_password": "NewPassword456!"
}
```

### Uso del Token JWT

```http
Authorization: Bearer <tu_token_jwt>
```

---

## 📦 Seed Data

### Roles (obligatorio antes del primer registro)

El sistema requiere que los roles existan en la base de datos:

| ID | Role Name | Descripción |
|----|-----------|-------------|
| 1 | admin | Administrador con acceso total |
| 2 | professor | Acceso a recursos de enseñanza |
| 3 | student | Acceso a materiales de aprendizaje |

**Ejecutar seeds:**
```bash
uv run python -m src.shared.seed.run_seed
```

### Usuario Admin

- **Username:** `superadmin`
- **Email:** `admin@example.com`
- **Password:** `adminpass123`

---

## 🗄️ Base de Datos

### Modelos Principales

| Modelo | Descripción |
|--------|-------------|
| `User` | Usuario base con autenticación |
| `Role` | Roles: admin, professor, student |
| `Student` | Perfil de estudiante |
| `Professor` | Perfil de profesor |
| `TeacherSettings` | Configuraciones del profesor |
| `Game` | Videojuego educativo |
| `Level` | Nivel dentro de un juego |
| `SegmentLevel` | Configuración de segmento |
| `GameInstance` | Instancia de juego activa |
| `SyncSession` | Sesión de sincronización |
| `SyncEvent` | Evento de sincronización |
| `Progress` | Métricas de progreso |
| `Feedback` | Feedback de estudiantes |
| `LMSCredential` | Credenciales LMS |
| `XAPIStatement` | Statements xAPI para tracking de aprendizaje |
| `MetricType` | Tipos de métricas de aprendizaje |

### Migraciones

```bash
# Crear migración
alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

---

## 🧪 Pruebas

```bash
# Ejecutar todas las pruebas
uv run pytest

# Con cobertura
uv run pytest --cov=src --cov-report=html

# Prueba específica
uv run pytest tests/test_user.py::test_create_user
```

---

## 📚 API Endpoints

### Autenticación (F-AUTH)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Registrar usuario | No |
| POST | `/api/v1/auth/login` | Iniciar sesión | No |
| POST | `/api/v1/auth/change-password` | Cambiar contraseña | Sí |

### Usuarios (F-USERS)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/users/` | Listar usuarios | Sí |
| GET | `/api/v1/users/{id}` | Obtener usuario | Sí |
| PUT | `/api/v1/users/{id}` | Actualizar usuario | Sí |
| DELETE | `/api/v1/users/{id}` | Eliminar usuario (soft) | Sí |

### Videojuegos (F-GAMES)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/games/` | Crear videojuego | Sí |
| GET | `/api/v1/games/` | Listar videojuegos | Sí |
| GET | `/api/v1/games/{id}` | Ver detalle | Sí |
| PUT | `/api/v1/games/{id}` | Actualizar | Sí |
| DELETE | `/api/v1/games/{id}` | Eliminar | Sí |

### Sincronización (F-SYNC)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/sync/sessions` | Crear sesión de sincronización | Sí |
| POST | `/api/v1/sync/events` | Registrar evento de sincronización | Sí |
| GET | `/api/v1/sync/sessions/{id}/events` | Obtener eventos de una sesión | Sí |
| POST | `/api/v1/statements/xapi` | Enviar statement xAPI | Sí |

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

---

## 🗄️ Diseño de Base de Datos

Consulta el documento de diseño conceptual de base de datos para más detalles:

- **[docs/database-design.md](docs/database-design.md)** - Diagrama ER completo en Mermaid y descripción de todas las tablas

### Dominios de la Base de Datos

| Dominio | Tablas | Descripción |
|---------|--------|-------------|
| **Users** | users, roles, students, professors, teacher_settings, lms_credentials | Gestión de usuarios y autenticación |
| **Game** | games, levels, segment_levels, game_instances | Catálogo de videojuegos y sesiones |
| **Statistic** | feedbacks, progresses, metric_types, xapi_statements | Métricas y tracking de progreso |
| **Sync** | sync_sessions, sync_events | Sincronización offline/online |

---

## 🐳 Docker

```bash
# Construir imagen
docker build -t hello-world-backend .

# Ejecutar contenedor
docker run -d -p 8000:8000 hello-world-backend

# Con Docker Compose (desde la raíz del proyecto)
docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d backend
```

---

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [PRD.md](PRD.md) | **Product Requirements Document** — requisitos funcionales, prioridades P0/P1/P2, escenarios de error |
| [docs/database-design.md](docs/database-design.md) | Diseño conceptual de la base de datos |
| [docs/user_stories.md](docs/user_stories.md) | Historias de usuario |
| [GP.md](GP.md) | Glosario de términos |
| [AGENTS.md](AGENTS.md) | Guías para agentes IA |

---

## 🌍 Links

- **Website**: [hello-world-project.dev](https://hello-world-project.dev)
- **Frontend**: [github.com/.../apps/frontend](https://github.com/tu-usuario/hello-world-project/apps/frontend)
- **Game**: [github.com/.../apps/game](https://github.com/tu-usuario/hello-world-project/apps/game)

