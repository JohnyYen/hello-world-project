# Diseño Conceptual de Base de Datos - Hello World Project

## Visión General

El backend de Hello World Project utiliza **PostgreSQL** como motor de base de datos, con **SQLAlchemy 2.0** en modo asíncrono para el ORM. El proyecto sigue una arquitectura basada en dominios, separando las entidades en módulos claramente definidos.

---

## Arquitectura de la Base

### Base Común (Soft Delete)

Todos los modelos heredan de una clase base que proporciona:

| Campo | Tipo | Descripción |
|-------|------|--------------|
| `id` | Integer (PK) | Identificador único auto-incremental |
| `created_at` | DateTime | Fecha de creación (timezone-aware) |
| `updated_at` | DateTime | Fecha de última modificación |
| `deleted_at` | DateTime | Fecha de eliminación (soft delete) |
| `is_deleted` | Boolean | Flag de eliminación lógica |

> **Nota**: Según las reglas del proyecto, se debería usar **UUIDv4** para las primary keys, pero la implementación actual utiliza enteros auto-incrementales.

---

## Dominio: Usuarios (`users`)

### Tabla: `users`

Entidad principal de autenticación y perfil de usuario.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `username` | String(255) | UNIQUE, NOT NULL, Index | Nombre de usuario |
| `email` | String(255) | UNIQUE, NOT NULL, Index | Correo electrónico |
| `hashed_password` | String(255) | NOT NULL | Contraseña hasheada |
| `name` | String(255) | NOT NULL | Nombre completo |
| `lastname` | String(255) | NULLABLE | Apellido |
| `avatar_url` | String(255) | NULLABLE | URL del avatar |
| `is_active` | Boolean | DEFAULT TRUE | Cuenta activa |
| `last_login` | DateTime | NULLABLE | Último inicio de sesión |
| `role_id` | Integer | FK → `roles.id`, NULLABLE | Rol del usuario |
| `lms_id` | Integer | FK → `lms_credentials.id`, NULLABLE | Credencial LMS asociada |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |
| `deleted_at` | DateTime | NULLABLE | Soft delete |
| `is_deleted` | Boolean | DEFAULT FALSE | Flag de eliminación |

**Relaciones:**
- `role` → `Role` (Many-to-One)
- `student` → `Student` (One-to-One, optional)
- `professor` → `Professor` (One-to-One, optional)
- `teacher_settings` → `TeacherSettings` (One-to-One, optional)
- `lms_credential` → `LMSCredential` (One-to-One, optional)

---

### Tabla: `roles`

Catálogo de roles del sistema.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `role_name` | String(255) | UNIQUE, NOT NULL, Index | Nombre del rol |
| `description` | String(255) | NULLABLE | Descripción del rol |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

---

### Tabla: `students`

Perfil de estudiante extendido.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `user_id` | Integer | FK → `users.id`, NOT NULL | Usuario asociado |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `user` → `User` (One-to-One)
- `game_instances` → `GameInstance` (One-to-Many)
- `feedbacks` → `Feedback` (One-to-Many)
- `progresses` → `Progress` (One-to-Many)
- `xapi_statements` → `XAPIStatement` (One-to-Many)

---

### Tabla: `professors`

Perfil de profesor extendido.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `user_id` | Integer | FK → `users.id`, NOT NULL | Usuario asociado |
| `department` | String(255) | NOT NULL | Departamento |
| `contact_phone` | String(255) | NULLABLE | Teléfono de contacto |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `user` → `User` (One-to-One)

---

### Tabla: `teacher_settings`

Configuraciones de preferencias del profesor.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `user_id` | Integer | FK → `users.id`, NOT NULL | Usuario asociado |
| `theme` | String(50) | DEFAULT 'light' | Tema (light/dark) |
| `notifications_enabled` | Boolean | DEFAULT TRUE | Notificaciones habilitadas |
| `notification_frequency` | String(50) | DEFAULT 'instant' | Frecuencia (instant/daily/weekly) |
| `interface_language` | String(10) | DEFAULT 'es' | Idioma de interfaz |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `user` → `User` (One-to-One)

---

### Tabla: `lms_credentials`

Credenciales para integración con LMS externos (Moodle, Canvas, etc.).

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `lms_email` | String(255) | UNIQUE, NOT NULL | Email en el LMS |
| `lms_password` | String(255) | NOT NULL | Contraseña del LMS |
| `lms_provider` | String(255) | NOT NULL | Proveedor LMS |
| `lms_url` | String(500) | NULLABLE | URL del LMS |
| `access_token` | String(500) | NULLABLE | Token de acceso OAuth |
| `refresh_token` | String(500) | NULLABLE | Token de refresh OAuth |
| `expire_at` | DateTime | NULLABLE | Fecha de expiración del token |
| `created_at` | DateTime(timezone) | NOT NULL | Fecha de creación |
| `updated_at` | DateTime(timezone) | NULLABLE | Fecha de actualización |

**Relaciones:**
- `user` → `User` (One-to-One, optional)

---

## Dominio: Juego (`game`)

### Tabla: `games`

Catálogo de juegos disponibles en la plataforma.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `title` | String(255) | NOT NULL | Título del juego |
| `description` | String(255) | NULLABLE | Descripción |
| `creator` | String(255) | NULLABLE | Creador del juego |
| `subject` | String(255) | NULLABLE | Materia/Tema |
| `publication_status` | String(255) | NULLABLE | Estado de publicación |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |
| `deleted_at` | DateTime | NULLABLE | Soft delete |
| `is_deleted` | Boolean | DEFAULT FALSE | Flag de eliminación |

**Relaciones:**
- `levels` → `Level` (One-to-Many)
- `instances` → `GameInstance` (One-to-Many)

---

### Tabla: `levels`

Niveles dentro de un juego.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `level_number` | Integer | NOT NULL | Número de nivel |
| `title` | String(255) | NOT NULL | Título del nivel |
| `description` | String(255) | NULLABLE | Descripción |
| `goal` | String(255) | NULLABLE | Objetivo del nivel |
| `game_id` | Integer | FK → `games.id`, NOT NULL | Juego asociado |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `game` → `Game` (Many-to-One)
- `segments` → `SegmentLevel` (One-to-Many)

---

### Tabla: `segment_levels`

Segmentos o configuraciones específicas de cada nivel.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `level_number_id` | Integer | FK → `levels.id`, NOT NULL | Nivel asociado |
| `configuration` | JSON | NULLABLE | Configuración del segmento |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `level` → `Level` (Many-to-One)
- `progresses` → `Progress` (One-to-Many)

---

### Tabla: `game_instances`

Instancias de juego activas (sesiones de un estudiante en un juego).

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `start_instance` | DateTime | NOT NULL | Fecha de inicio |
| `status` | String(255) | NULLABLE | Estado de la instancia |
| `student_id` | Integer | FK → `students.id`, NOT NULL | Estudiante |
| `game_id` | Integer | FK → `games.id`, NOT NULL | Juego |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `student` → `Student` (Many-to-One)
- `game` → `Game` (Many-to-One)
- `sync_sessions` → `SyncSession` (One-to-Many)

---

## Dominio: Estadísticas (`statistic`)

### Tabla: `feedbacks`

Comentarios y calificaciones de estudiantes.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `comments` | Text | NOT NULL | Comentarios del estudiante |
| `rating` | Integer | NULLABLE | Calificación (1-5) |
| `student_id` | Integer | FK → `students.id`, NOT NULL | Estudiante |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `student` → `Student` (Many-to-One)

---

### Tabla: `progresses`

Progreso del estudiante en cada segmento de nivel.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `student_id` | Integer | FK → `students.id`, NOT NULL | Estudiante |
| `segment_level_id` | Integer | FK → `segment_levels.id`, NOT NULL | Segmento de nivel |
| `attempt_count` | Integer | DEFAULT 0 | Intentos realizados |
| `error_count` | Integer | DEFAULT 0 | Cantidad de errores |
| `hints_used_count` | Integer | DEFAULT 0 | Pistas utilizadas |
| `errors_details` | JSON | NULLABLE | Detalles de errores |
| `objectives_completed` | Integer | DEFAULT 0 | Objetivos completados |
| `efficiency_rating` | Integer | DEFAULT 0 | Rating de eficiencia |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `student` → `Student` (Many-to-One)
- `segment_level` → `SegmentLevel` (Many-to-One)

---

### Tabla: `metric_types`

Catálogo de tipos de métricas disponibles.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `name` | String(255) | NOT NULL | Nombre de la métrica |
| `code` | String(50) | UNIQUE, NOT NULL | Código único |
| `description` | String(500) | NULLABLE | Descripción |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

---

### Tabla: `xapi_statements`

Almacenamiento de statements xAPI (Experience API) del juego.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |

#### Actor (Actor)
| `actor_mbox` | String(255) | NULLABLE, Index | Email del actor (mailto:) |
| `actor_account_name` | String(255) | NULLABLE, Index | Nombre de cuenta |
| `actor_account_homepage` | String(255) | NULLABLE | Homepage de la cuenta |

#### Verb (Verbo de la acción)
| `verb_id` | String(500) | NOT NULL, Index | ID del verbo xAPI |
| `verb_display` | JSON | NULLABLE | Display del verbo |

#### Object (Objeto de la acción)
| `object_id` | String(1000) | NOT NULL, Index | ID del objeto |
| `object_type` | String(100) | NULLABLE | Tipo de objeto |
| `object_definition_type` | String(255) | NULLABLE | Tipo en definición |
| `object_definition_name` | JSON | NULLABLE | Nombre del objeto |

#### Context (Contexto)
| `platform` | String(255) | NULLABLE | Plataforma |
| `language` | String(10) | NULLABLE | Idioma |
| `context_extensions` | JSON | NULLABLE | Extensiones de contexto |
| `context_platform` | String(255) | NULLABLE | Plataforma de contexto |

#### Result (Resultado)
| `result_score_raw` | String(50) | NULLABLE | Score raw |
| `result_score_min` | String(50) | NULLABLE | Score mínimo |
| `result_score_max` | String(50) | NULLABLE | Score máximo |
| `result_score_scaled` | String(50) | NULLABLE | Score scaled |
| `result_success` | Boolean | NULLABLE | Éxito |
| `result_completion` | Boolean | NULLABLE | Completado |
| `result_duration` | String(50) | NULLABLE | Duración |
| `result_response` | Text | NULLABLE | Respuesta |
| `result_extensions` | JSON | NULLABLE | Extensiones de resultado |

#### Timestamps
| `timestamp` | DateTime(timezone) | NOT NULL, Index | Timestamp del statement |
| `stored` | DateTime(timezone) | NOT NULL | Fecha de almacenamiento |

#### Original Statement
| `statement` | JSON | NOT NULL | Statement completo original |

#### Game-specific Parsed Fields
| `student_id` | Integer | NULLABLE, Index | Estudiante |
| `game_id` | Integer | NULLABLE, Index | Juego |
| `level_id` | Integer | NULLABLE, Index | Nivel |
| `segment_id` | Integer | NULLABLE, Index | Segmento |

**Índices Compuestos:**
- `ix_xapi_statements_composite`: (student_id, game_id, level_id)
- `ix_xapi_statements_actor_timestamp`: (actor_account_name, timestamp)

**Relaciones:**
- `student` → `Student` (Many-to-One, optional)

---

## Dominio: Sincronización (`sync`)

### Tabla: `sync_sessions`

Sesiones de sincronización entre cliente y servidor.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `start_time` | DateTime | NOT NULL | Inicio de la sesión |
| `end_time` | DateTime | NULLABLE | Fin de la sesión |
| `status` | String(255) | NULLABLE | Estado de la sesión |
| `instance_id` | Integer | FK → `game_instances.id`, NOT NULL | Instancia de juego |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `game_instance` → `GameInstance` (Many-to-One)
- `events` → `SyncEvent` (One-to-Many)

---

### Tabla: `sync_events`

Eventos individuales dentro de una sesión de sincronización.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, Auto-increment | Identificador único |
| `event_type` | String(255) | NOT NULL | Tipo de evento |
| `payload` | JSON | NULLABLE | Datos del evento |
| `timestamp` | DateTime | NOT NULL | Timestamp del evento |
| `status` | String(255) | NULLABLE | Estado del evento |
| `sync_session_id` | Integer | FK → `sync_sessions.id`, NOT NULL | Sesión padre |
| `created_at` | DateTime | NOT NULL | Fecha de creación |
| `updated_at` | DateTime | NULLABLE | Fecha de actualización |

**Relaciones:**
- `sync_session` → `SyncSession` (Many-to-One)

---

## Diagrama ER (Mermaid)

```mermaid
erDiagram
    %% ============================================
    %% DOMINIO: USUARIOS
    %% ============================================
    
    ROLES {
        int id PK
        string role_name UK
        string description
        datetime created_at
        datetime updated_at
    }

    USERS {
        int id PK
        string username UK
        string email UK
        string hashed_password
        string name
        string lastname
        string avatar_url
        boolean is_active
        datetime last_login
        int role_id FK
        int lms_id FK
        datetime created_at
        datetime updated_at
        datetime deleted_at
        boolean is_deleted
    }

    LMS_CREDENTIALS {
        int id PK
        string lms_email UK
        string lms_password
        string lms_provider
        string lms_url
        string access_token
        string refresh_token
        datetime expire_at
        datetime created_at
        datetime updated_at
    }

    STUDENTS {
        int id PK
        int user_id FK UK
        datetime created_at
        datetime updated_at
    }

    PROFESSORS {
        int id PK
        int user_id FK UK
        string department
        string contact_phone
        datetime created_at
        datetime updated_at
    }

    TEACHER_SETTINGS {
        int id PK
        int user_id FK UK
        string theme
        boolean notifications_enabled
        string notification_frequency
        string interface_language
        datetime created_at
        datetime updated_at
    }

    %% ============================================
    %% DOMINIO: JUEGO
    %% ============================================

    GAMES {
        int id PK
        string title
        string description
        string creator
        string subject
        string publication_status
        datetime created_at
        datetime updated_at
        datetime deleted_at
        boolean is_deleted
    }

    LEVELS {
        int id PK
        int level_number
        string title
        string description
        string goal
        int game_id FK
        datetime created_at
        datetime updated_at
    }

    SEGMENT_LEVELS {
        int id PK
        int level_number_id FK
        json configuration
        datetime created_at
        datetime updated_at
    }

    GAME_INSTANCES {
        int id PK
        datetime start_instance
        string status
        int student_id FK
        int game_id FK
        datetime created_at
        datetime updated_at
    }

    %% ============================================
    %% DOMINIO: ESTADÍSTICAS
    %% ============================================

    FEEDBACKS {
        int id PK
        text comments
        int rating
        int student_id FK
        datetime created_at
        datetime updated_at
    }

    PROGRESSES {
        int id PK
        int student_id FK
        int segment_level_id FK
        int attempt_count
        int error_count
        int hints_used_count
        json errors_details
        int objectives_completed
        int efficiency_rating
        datetime created_at
        datetime updated_at
    }

    METRIC_TYPES {
        int id PK
        string name
        string code UK
        string description
        datetime created_at
        datetime updated_at
    }

    XAPI_STATEMENTS {
        int id PK
        string actor_mbox
        string actor_account_name
        string actor_account_homepage
        string verb_id
        json verb_display
        string object_id
        string object_type
        string object_definition_type
        json object_definition_name
        string platform
        string language
        json context_extensions
        string context_platform
        string result_score_raw
        string result_score_min
        string result_score_max
        string result_score_scaled
        boolean result_success
        boolean result_completion
        string result_duration
        text result_response
        json result_extensions
        datetime timestamp
        datetime stored
        json statement
        int student_id FK
        int game_id FK
        int level_id FK
        int segment_id FK
    }

    %% ============================================
    %% DOMINIO: SINCRONIZACIÓN
    %% ============================================

    SYNC_SESSIONS {
        int id PK
        datetime start_time
        datetime end_time
        string status
        int instance_id FK
        datetime created_at
        datetime updated_at
    }

    SYNC_EVENTS {
        int id PK
        string event_type
        json payload
        datetime timestamp
        string status
        int sync_session_id FK
        datetime created_at
        datetime updated_at
    }

    %% ============================================
    %% RELACIONES - USUARIOS
    %% ============================================

    ROLES ||--o{ USERS : "has"
    USERS ||--o| STUDENTS : "is"
    USERS ||--o| PROFESSORS : "is"
    USERS ||--o| TEACHER_SETTINGS : "has"
    USERS ||--o| LMS_CREDENTIALS : "has"
    LMS_CREDENTIALS ||--o| USERS : "belongs_to"

    %% ============================================
    %% RELACIONES - JUEGO
    %% ============================================

    GAMES ||--o{ LEVELS : "contains"
    LEVELS ||--o{ SEGMENT_LEVELS : "has"
    GAMES ||--o{ GAME_INSTANCES : "has"
    STUDENTS ||--o{ GAME_INSTANCES : "plays"

    %% ============================================
    %% RELACIONES - ESTADÍSTICAS
    %% ============================================

    STUDENTS ||--o{ FEEDBACKS : "gives"
    STUDENTS ||--o{ PROGRESSES : "makes"
    SEGMENT_LEVELS ||--o{ PROGRESSES : "tracks"
    STUDENTS ||--o{ XAPI_STATEMENTS : "generates"
    GAMES ||--o{ XAPI_STATEMENTS : "related_to"
    LEVELS ||--o{ XAPI_STATEMENTS : "related_to"
    SEGMENT_LEVELS ||--o{ XAPI_STATEMENTS : "related_to"

    %% ============================================
    %% RELACIONES - SINCRONIZACIÓN
    %% ============================================

    GAME_INSTANCES ||--o{ SYNC_SESSIONS : "has"
    SYNC_SESSIONS ||--o{ SYNC_EVENTS : "contains"
```

---

## Observaciones y Mejoras Recomendadas

### 1. Primary Keys

**Problema:** Actualmente se utilizan enteros auto-incrementales (`Integer`) en lugar de UUIDs.

**Recomendación:** Cambiar a UUIDv4 para todas las primary keys según las reglas del proyecto:

```python
import uuid
from sqlalchemy.dialects.postgresql import UUID

id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
```

### 2. Índices

**Existentes:**
- `xapi_statements` tiene índices compuestos útiles
- Los campos `username` y `email` en `users` tienen índice único

**Faltantes sugeridos:**
- `game_instances`: (student_id, game_id) para consultas de sesión activa
- `progresses`: (student_id, segment_level_id) para tracking de progreso
- `sync_events`: (sync_session_id, timestamp) para ordered queries

### 3. Foreign Keys

Todas las relaciones tienen Foreign Keys definidas, lo cual es correcto para integridad referencial.

### 4. JSON Fields

El uso de JSON para `configuration`, `payload`, `context_extensions`, y `statement` es apropiado para datos semiestructurados, pero considerar crear tablas separadas si estos campos crecen en complejidad.

### 5. Soft Delete

El soft delete está implementado en el modelo base pero no se usa consistentemente en todas las consultas. Asegurar que las queries incluyan el filtro `is_deleted = False`.

---

## Tecnologías y Versiones

| Componente | Versión |
|------------|---------|
| PostgreSQL | 16 |
| SQLAlchemy | 2.0 (Async) |
| Alembic | Latest |
| Pydantic | v2 |

---

*Documento generado para Hello World Project - Backend*
