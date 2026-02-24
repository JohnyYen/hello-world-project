# Hello World Backend

Backend API para Hello World Project - una plataforma educativa basada en videojuegos interactivos para enseñar programación.

## 📋 Descripción

Hello World Project es una plataforma educativa que actúa como puente de comunicación entre un frontend Next.js y videojuegos educativos. El sistema permite:

- **Profesores**: Crear y gestionar contenidos de aprendizaje, videojuegos y niveles
- **Estudiantes**: Interactuar con videojuegos en tiempo real
- **Administración**: Herramientas de seguimiento, análisis y sincronización de progreso
- **Integración**: Conexión con LMS externos (Moodle, Canvas)

---

## 🚀 Características Principales

- **Arquitectura Limpia**: Separación clara entre capas (API, Application, Domain, Infrastructure)
- **Autenticación JWT**: Tokens con expiración configurable (30 minutos por defecto)
- **Base de Datos Async**: SQLAlchemy 2.0+ con soporte asíncrono
- **Validación Pydantic**: Esquemas validados con regex para contraseñas
- **Patrón Repository**: Operaciones CRUD desacopladas del dominio
- **Gestión de Roles**: admin, professor, student con asignación automática
- **Documentación**: Swagger UI y ReDoc disponibles

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
│   ├── shared/                  # Código compartido
│   │   ├── api/schemas/
│   │   │   ├── base.py          # ResponseSchema, DateTimeSchema
│   │   │   └── pagination.py    # Paginación
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
├── tests/                       # Pruebas unitarias y de integración
├── alembic/                     # Migraciones de base de datos
├── .env.example                 # Variables de entorno ejemplo
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── AGENTS.md                    # Guía para agentes IA
├── PROJECT_SPEC.md              # Especificaciones del proyecto
└── README.md
```

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
| `SyncEvent` | Evento de juego |
| `Progress` | Métricas de progreso |
| `Feedback` | Feedback de estudiantes |
| `LMSCredential` | Credenciales LMS |

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

## 🐳 Docker

```bash
# Construir imagen
docker build -t hello-world-backend .

# Ejecutar contenedor
docker run -d -p 8000:8000 hello-world-backend

# Con Docker Compose
docker-compose up -d
```

---

## 📚 API Endpoints

### Autenticación
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Registrar usuario | No |
| POST | `/api/v1/auth/login` | Iniciar sesión | No |
| POST | `/api/v1/auth/change-password` | Cambiar contraseña | Sí |

### Usuarios
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/users/` | Listar usuarios | Sí |
| GET | `/api/v1/users/{id}` | Obtener usuario | Sí |
| PUT | `/api/v1/users/{id}` | Actualizar usuario | Sí |
| DELETE | `/api/v1/users/{id}` | Eliminar usuario (soft) | Sí |

### Videojuegos
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/games/` | Crear videojuego | Sí |
| GET | `/api/v1/games/` | Listar videojuegos | Sí |
| GET | `/api/v1/games/{id}` | Ver detalle | Sí |
| PUT | `/api/v1/games/{id}` | Actualizar | Sí |
| DELETE | `/api/v1/games/{id}` | Eliminar | Sí |

---

## 📄 Licencia

Este proyecto está bajo desarrollo para fines educativos.

---

## 📞 Soporte

Para consultas sobre el proyecto, revisar `PROJECT_SPEC.md` para especificaciones completas.
