# Hello World Project - Especificaciones del Proyecto

## Descripción del Proyecto

Hello World Project es una plataforma educativa basada en videojuegos interactivos para enseñar programación, que actúa como puente de comunicación entre un frontend Next.js y videojuegos educativos. El sistema permite a profesores crear y gestionar contenidos de aprendizaje, a estudiantes interactuar con videojuegos en tiempo real, y proporciona herramientas de seguimiento, análisis y sincronización de progreso. Incluye integración con LMS externos, sistema de feedback y generación de reportes detallados.

---

## Historias de Usuario

### Epic 1: Gestión de Usuarios y Autenticación

#### US-001: Registro de usuario
As a new user, I want to register an account to access the platform and start learning
**Acceptance Criteria:**
- Form with fields: username (unique, 3-100 chars), email (unique, valid format), password (8+ chars, uppercase, lowercase, number)
- Password validation with regex for strength
- Hash password using bcrypt before storing
- Return JWT token upon successful registration
- Email/username uniqueness validation
- **Role assignment: system automatically assigns 'professor' role upon registration**
- **Technical Notes:** Use UserCreate schema (without role_id), password hash in UserService.create_user(), role assigned via RoleRepository.get_professor_role(). Throws NotFoundException if 'professor' role doesn't exist in DB (HTTP 500)

#### US-002: Inicio de sesión
As a registered user, I want to login with email and password to authenticate and receive an access token
**Acceptance Criteria:**
- Form with email and password fields
- Validate credentials against hashed password in database
- Return JWT access token with expiration (30 min default)
- Include user profile in response
- Reject inactive or deleted users
- Use Bearer token authentication scheme
**Technical Notes:** JWT via pyjwt, password verification with passlib bcrypt

#### US-003: Cambio de contraseña
As an authenticated user, I want to change my password to maintain security
**Acceptance Criteria:**
- Form with current_password and new_password fields
- Validate current password matches stored hash
- Apply same password strength validation as registration
- New password must be different from current password
- Update hashed_password field in database
- Return success message after update
**Validations:** New password must differ from current, strength rules same as US-001

---

### Epic 2: Gestión de Estudiantes

#### US-004: Crear estudiante
As a professor, I want to register new students to enroll them in the platform
**Acceptance Criteria:**
- Form with username, email, name, lastname, password, is_active (default True)
- Auto-link Student profile to User profile
- Validate email/username uniqueness across platform
- Student must have role_id pointing to "student" role (assigned by professor)
- Return created student with user profile included
**Technical Notes:** Creates User entry with 'student' role (via RoleRepository.get_student_role()) then Student entry with user_id foreign key

#### US-005: Listar estudiantes
As a professor, I want to see a list of students with filters and pagination to manage my class
**Acceptance Criteria:**
- Paginated list with skip (default 0) and limit (max 100, default 10) parameters
- Search filter by name or email (partial match)
- Filter by active status (True/False)
- Each student displays: id, username, email, name, lastname, is_active, created_at, updated_at
- Return empty array if no students match criteria
**Validations:** skip >= 0, limit between 1-100

#### US-006: Ver progreso de estudiante
As a professor, I want to see a student's progress to identify areas needing attention
**Acceptance Criteria:**
- Show completed_levels, total_levels, completion_percentage
- Display current_level name and last_activity timestamp
- Show total_time_spent in human-readable format
- Calculate completion_percentage as (completed_levels / total_levels) * 100
- Return 404 if student_id doesn't exist
**Technical Notes:** Query from Progress and Level tables aggregated by student

#### US-007: Ver reportes de estudiante
As a professor, I want to see detailed student reports including performance, activity, and engagement metrics
**Acceptance Criteria:**
- Performance report: average_score, completed_assignments, passed_assignments, failed_assignments
- Activity report: total_sessions, total_time_spent, last_login
- Engagement report: participation_rate (%), completed_activities, total_activities
- All reports tied to student_id
- Return 404 if student has no data
**Technical Notes:** Aggregated data from Progress, GameInstance, and SyncEvent tables

#### US-008: Actualizar estudiante
As a professor, I want to update student information to keep records current
**Acceptance Criteria:**
- Accept partial updates: username, email, name, lastname, is_active
- Email/username uniqueness validation excluding current student
- Update both User and Student tables if needed
- Return updated student profile
- Soft delete if setting is_active to False
**Validations:** Unique constraints apply, password updates handled separately via US-003

#### US-009: Eliminar estudiante
As a professor, I want to delete a student to remove them from the platform
**Acceptance Criteria:**
- Perform soft delete on both User and Student records
- Set deleted_at and is_deleted flags on User table
- Return success message with deleted student_id
- Student still exists in database but excluded from queries
- Cascade soft delete to related records (GameInstance, Feedback, Progress)
**Technical Notes:** Use BaseRepository.delete() which performs soft delete

---

### Epic 3: Gestión de Profesores

#### US-010: Ver perfil de profesor
As a professor, I want to view my profile information to manage my account
**Acceptance Criteria:**
- Display: id, username, name, lastname, email, department, contact_phone, avatar_url, is_active
- Show created_at and updated_at timestamps
- Profile associated with authenticated user via JWT token
- Return 401 if not authenticated, 404 if profile not found
**Technical Notes:** Query Professor table joined with User table via user_id FK

#### US-011: Actualizar perfil de profesor
As a professor, I want to update my profile information to keep it current
**Acceptance Criteria:**
- Accept partial updates: name, lastname, email, department, contact_phone, avatar_url
- Email uniqueness validation excluding current professor
- Update both User and Professor tables
- Return updated profile with updated_at timestamp
**Validations:** Email uniqueness constraint, avatar_url should be valid URL

#### US-012: Ver configuraciones de profesor
As a professor, I want to view my dashboard settings to customize my experience
**Acceptance Criteria:**
- Display: theme (light/dark), notifications_enabled (bool), notification_frequency (instant/daily/weekly), interface_language (es/en)
- Settings tied to authenticated user's TeacherSettings record
- Return default values if no custom settings exist
**Defaults:** theme="light", notifications_enabled=True, notification_frequency="instant", interface_language="es"

#### US-013: Actualizar configuraciones de profesor
As a professor, I want to update my settings to personalize the platform
**Acceptance Criteria:**
- Accept all or partial settings updates
- Validate theme is "light" or "dark"
- Validate notification_frequency is "instant", "daily", or "weekly"
- Validate interface_language is 2-10 character code (es, en, pt, etc.)
- Update updated_at timestamp
- Return updated settings
**Validations:** Enum constraints on theme and frequency, language code format

---

### Epic 4: Gestión de Videojuegos

#### US-014: Crear videojuego
As a professor, I want to create an educational game to teach programming concepts
**Acceptance Criteria:**
- Form with: title (required), description (optional), creator (optional), subject (optional), publication_status (optional)
- Returns created game with id, timestamps, and success response
- Response format: `{ success: true, message: "Juego creado exitosamente", data: GameResponse }`
- HTTP 201 on success, HTTP 400 on duplicate title
**Technical Notes:** Creates Game entry using GameRepository. publication_status defaults to empty string if not provided. Levels must be added separately via US-017.

#### US-015: Listar videojuegos
As a user, I want to browse available games to find content to learn from
**Acceptance Criteria:**
- Paginated list with skip (default 0) and limit (max 100, default 10)
- Each game displays: id, title, description, creator, subject, publication_status, created_at, updated_at, is_deleted
- Returns response: `{ success: true, message: "Juegos obtenidos exitosamente", data: GameResponse[], total, skip, limit }`
- Games with is_deleted=True are excluded from results
- Returns empty array if no games exist
**Validations:** skip >= 0, limit between 1-100
**Technical Notes:** Uses GameRepository.get_all_with_levels() with eager loading for levels relationship.

#### US-016: Ver detalle de videojuego
As a user, I want to see detailed information about a specific game before playing
**Acceptance Criteria:**
- Show all game fields including levels_count (number of associated levels)
- Returns response: `{ success: true, message: "Juego obtenido exitosamente", data: GameDetailResponse }`
- Return 404 if game_id doesn't exist
**Technical Notes:** Uses GameRepository.get_by_id_with_levels() with eager loading for levels relationship. levels_count calculated from loaded relationship.

#### US-017: Actualizar videojuego
As a professor/creator, I want to update game information to improve content
**Acceptance Criteria:**
- Accept partial updates: title, description, creator, subject, publication_status
- Returns response: `{ success: true, message: "Juego actualizado exitosamente", data: GameResponse }`
- Return 404 if game_id doesn't exist
- Return 400 on duplicate title conflict
**Technical Notes:** Uses GameRepository.update(). Only provided fields are updated (PATCH-like behavior).

#### US-018: Eliminar videojuego
As a professor/creator, I want to delete a game to remove outdated content
**Acceptance Criteria:**
- Perform soft delete on Game record (sets is_deleted=True and deleted_at timestamp)
- Returns response: `{ success: true, message: "Juego eliminado exitosamente" }`
- Return 404 if game_id doesn't exist
- Soft delete is reversible (not permanent deletion)
**Technical Notes:** Uses BaseRepository.delete() which performs soft delete. Related entities (Levels, GameInstances) remain in database but are excluded from queries via is_deleted filter.

---

### Epic 5: Sistema de Niveles

#### US-019: Crear nivel
As a professor, I want to create levels within a game to structure learning content
**Acceptance Criteria:**
- Form with: level_number (required), title (required), description (optional), goal (optional)
- game_id provided in URL path parameter
- Returns response: `{ success: true, message: "Nivel creado exitosamente", data: LevelResponse }`
- Return 404 if game_id doesn't exist
- Return 400 on duplicate level_number within same game
- HTTP 201 on success
**Technical Notes:** Creates Level entry linked to Game via game_id FK. Uses LevelRepository.create(). game_id set from URL path, not request body.

#### US-020: Listar niveles de videojuego
As a student/professor, I want to see all levels in a game to understand the structure
**Acceptance Criteria:**
- Paginated list with skip (default 0) and limit parameters
- Returns response: `{ success: true, message: "Niveles obtenidos exitosamente", data: LevelResponse[], total }`
- Each level displays: id, game_id, level_number, title, description, goal, created_at, updated_at, is_deleted
- Return 404 if game_id doesn't exist
- Levels with is_deleted=True are excluded
**Validations:** skip >= 0, limit between 1-100
**Technical Notes:** Uses LevelRepository.get_by_game_id_with_segments() with eager loading for segments relationship.

#### US-021: Ver detalle de nivel
As a student, I want to see level details before attempting it
**Acceptance Criteria:**
- Show all level fields: id, game_id, level_number, title, description, goal, created_at, updated_at
- Show related segments_count (number of associated SegmentLevel)
- Returns response: `{ success: true, message: "Nivel obtenido exitosamente", data: LevelDetailResponse }`
- Return 404 if level_id doesn't exist
**Technical Notes:** Uses LevelRepository.get_by_id_with_segments() with eager loading for segments relationship. segments_count calculated from loaded relationship.

#### US-022: Actualizar nivel
As a professor/creator, I want to update level details to improve learning material
**Acceptance Criteria:**
- Accept partial updates: level_number, title, description, goal
- Returns response: `{ success: true, message: "Nivel actualizado exitosamente", data: LevelResponse }`
- Return 404 if level_id doesn't exist
- Return 400 on duplicate level_number conflict within same game
**Technical Notes:** Uses LevelRepository.update(). Only provided fields are updated (PATCH-like behavior).

#### US-023: Eliminar nivel
As a professor/creator, I want to delete a level to remove outdated content
**Acceptance Criteria:**
- Perform soft delete on Level record (sets is_deleted=True and deleted_at timestamp)
- Returns response: `{ success: true, message: "Nivel eliminado exitosamente" }`
- Return 404 if level_id doesn't exist
- Soft delete is reversible (not permanent deletion)
**Technical Notes:** Uses BaseRepository.delete() which performs soft delete. Related SegmentLevels remain in database but are excluded from queries via is_deleted filter.

---

### Epic 6: Instancias de Juego

#### US-024: Crear instancia de juego
As a student, I want to start a game instance to begin playing and learning
**Acceptance Criteria:**
- Form with: student_id (required)
- game_id provided in URL path parameter
- Set start_instance to current timestamp automatically
- Set status to "active" by default
- Returns response: `{ success: true, message: "Instancia creada exitosamente", data: GameInstanceResponse }`
- Return 404 if game_id doesn't exist
- HTTP 201 on success
**Technical Notes:** Creates GameInstance linked to Game and Student. Uses GameInstanceRepository.create(). start_instance set server-side to datetime.utcnow().

#### US-025: Listar instancias activas
As a professor, I want to see active game instances to monitor student activity
**Acceptance Criteria:**
- Filter by game_id (URL path parameter), status (optional query param: active/completed/abandoned)
- Paginated with skip (default 0) and limit (max 100, default 10)
- Returns response: `{ success: true, message: "Instancias obtenidas exitosamente", data: GameInstanceResponse[], total, skip, limit }`
- Each instance displays: id, game_id, student_id, status, start_instance, created_at, updated_at
- Instances with is_deleted=True are excluded
- Return empty data array if no instances match
**Validations:** skip >= 0, limit between 1-100
**Technical Notes:** Uses GameInstanceRepository.get_by_game_id() with optional status filter applied in endpoint.

#### US-026: Ver instancia específica
As a student/professor, I want to see instance details to review progress
**Acceptance Criteria:**
- Show all instance fields: id, game_id, student_id, status, start_instance, created_at, updated_at
- Show related game_title (from Game relationship)
- Returns response: `{ success: true, message: "Instancia obtenida exitosamente", data: GameInstanceDetailResponse }`
- Return 404 if instance_id doesn't exist
**Technical Notes:** Uses GameInstanceRepository.get_by_id_with_relations() with eager loading for game and student relationships. game_title populated from loaded game relationship.

#### US-027: Finalizar instancia
As a student, I want to mark a game instance as completed when finished
**Acceptance Criteria:**
- Change status from "active" to "completed" or "abandoned"
- Returns response: `{ success: true, message: "Instancia finalizada exitosamente", data: GameInstanceResponse }`
- Return 404 if instance_id doesn't exist
- Status parameter optional (defaults to "completed")
**Technical Notes:** Uses GameInstanceRepository.update() to modify status field. No end_instance timestamp field in current model.

---

### Epic 7: Sincronización en Tiempo Real

#### US-028: Iniciar sesión de sincronización
As a game client, I want to start a sync session to begin real-time data exchange
**Acceptance Criteria:**
- Form with: instance_id (required, must exist)
- Set start_time to current timestamp
- Set status to "active"
- Auto-generate unique session_id
- End_time is null initially
- Return created session with id and timestamps
**Technical Notes:** Creates SyncSession linked to GameInstance

#### US-029: Registrar evento de sincronización
As a game client, I want to register player actions/events to track gameplay
**Acceptance Criteria:**
- Form with: sync_session_id (required), event_type (required), payload (JSON, optional), timestamp (required)
- Event types: player_move, level_complete, item_collected, hint_used, error_occurred, etc.
- Store payload as JSON field with event-specific data
- Auto-generate event_id
- Set status to "synced" by default
- Return created event with id
**Technical Notes:** Creates SyncEvent linked to SyncSession, payload is flexible JSON

#### US-030: Listar eventos de sesión
As a professor/game, I want to see all events in a sync session for analysis
**Acceptance Criteria:**
- Filter by sync_session_id
- Return all events ordered by timestamp ascending
- Each event displays: id, sync_session_id, event_type, payload, timestamp, status
- Return empty array if session has no events
**Technical Notes:** Query SyncEvent filtered by sync_session_id

#### US-031: Finalizar sesión de sincronización
As a game client, I want to end a sync session when gameplay stops
**Acceptance Criteria:**
- Change status from "active" to "completed"
- Set end_time to current timestamp
- Calculate session duration (end_time - start_time)
- Return updated session with new status and end time
- Only active sessions can be ended
**Validations:** Session must exist and be in "active" status

#### US-032: Ver sesiones por instancia
As a professor, I want to see all sync sessions for a game instance to analyze play patterns
**Acceptance Criteria:**
- Filter by instance_id
- Return all sessions ordered by start_time descending
- Each session displays: id, instance_id, start_time, end_time, status
- Include active sessions (end_time is null)
- Return empty array if instance has no sessions
**Technical Notes:** Query SyncSession filtered by instance_id FK

---

### Epic 8: Seguimiento de Progreso

#### US-033: Registrar métricas de progreso
As a game client, I want to record student progress metrics to track learning
**Acceptance Criteria:**
- Form with: segment_level_id (required), attempt_count, error_count, hints_used_count, errors_details (JSON), objectives_completed, efficiency_rating
- All metrics default to 0 if not provided
- errors_details stores array of error objects with type, timestamp, code snippet
- objectives_completed is integer count of completed objectives
- efficiency_rating calculated as (objectives_completed / (attempt_count + 1)) * 100
- Return created progress record
**Technical Notes:** Creates Progress linked to SegmentLevel

#### US-034: Ver progreso detallado
As a student, I want to see my detailed progress to understand my learning journey
**Acceptance Criteria:**
- Aggregate progress by game or level
- Show attempt_count, error_count, hints_used_count per segment
- Show objectives_completed and efficiency_rating
- Display errors_details array for learning from mistakes
- Filter by student_id and optional game_id/level_id
- Return 404 if no progress data exists for student
**Technical Notes:** Join Progress, SegmentLevel, Level, and Game tables

#### US-035: Ver progreso global
As a professor, I want to see aggregate progress across all students to identify trends
**Acceptance Criteria:**
- Average metrics across all students: avg_attempt_count, avg_error_count, avg_efficiency_rating
- Total objectives completed per game/level
- Error frequency analysis (most common error types)
- Engagement metrics: hints_used frequency, session duration
- Paginated results
- Return summary even if no students (all zeros)
**Technical Notes:** Aggregation queries with GROUP BY on segment_level_id

---

### Epic 9: Sistema de Feedback

#### US-036: Enviar feedback
As a student, I want to submit feedback about the platform or specific content
**Acceptance Criteria:**
- Form with: student_id (auto-filled from auth), comments (required, max 255 chars), rating (optional, 1-5 scale)
- Set created_at to current timestamp
- Rating defaults to 5 if not provided
- Comments must not be empty
- Store as plain text (no HTML allowed)
- Return created feedback with id
**Validations:** comments 1-255 characters, rating between 1-5

#### US-037: Ver histórico de feedback
As a professor, I want to see a student's feedback history to understand their experience
**Acceptance Criteria:**
- Filter by student_id
- Return all feedback ordered by created_at descending
- Each feedback displays: id, student_id, comments, rating, created_at
- Show average rating across all feedback
- Return empty array if student has no feedback
- Pagination supported with skip/limit
**Validations:** skip >= 0, limit between 1-100

#### US-038: Ver feedback agregado
As a professor/admin, I want to see all feedback with aggregate statistics to improve the platform
**Acceptance Criteria:**
- Show all feedback with student names (sanitized)
- Calculate average rating across all feedback
- Group feedback by rating categories (1-2 stars, 3 stars, 4-5 stars)
- Show most recent feedback first
- Paginated results
- Filter by date range (optional)
**Technical Notes:** Join Feedback with Student tables, aggregation for statistics

---

### Epic 10: Integración LMS

#### US-039: Registrar credenciales LMS
As a professor, I want to register LMS credentials to enable integration
**Acceptance Criteria:**
- Form with: user_id (required), lms_url (required, valid URL), lms_email (required, valid email), lms_password (required), lms_provider (required, e.g., moodle, canvas), access_token (optional), expire_at (optional)
- lms_email must be unique across platform
- Hash lms_password using bcrypt before storing
- access_token and expire_at populated during LMS OAuth flow
- Return created credentials with id
**Validations:** URL format, email format, password strength, unique lms_email

#### US-040: Ver credenciales del usuario
As a professor, I want to view my LMS credentials to manage integration
**Acceptance Criteria:**
- Show all credential fields except lms_password
- Mask access_token (show only first/last 4 chars)
- Display expire_at with days remaining
- Return 404 if user has no LMS credentials registered
- Only credential owner can view
**Technical Notes:** Query LMSCredential by user_id, filter password field from response

#### US-041: Actualizar credenciales LMS
As a professor, I want to update LMS credentials to maintain connection
**Acceptance Criteria:**
- Accept partial updates: lms_url, lms_email, lms_password, lms_provider, access_token, expire_at
- lms_email uniqueness validation excluding current user
- Hash new password if provided
- Update updated_at timestamp on parent User record
- Return updated credentials (password masked)
**Validations:** URL/email format, password strength, uniqueness

#### US-042: Sincronizar datos del LMS
As a professor, I want to trigger LMS sync to import/export student data
**Acceptance Criteria:**
- Trigger bidirectional sync with configured LMS
- Import: users, courses, grades from LMS
- Export: student progress, game instances to LMS
- Return sync results: status (success/partial/failed), records_synced (counts by type), sync_time, next_sync_scheduled
- Handle API errors gracefully with partial success status
- Update access_token if refreshed during sync
**Technical Notes:** Async background task, retry logic, error handling

#### US-043: Ver histórico de sincronización
As a professor, I want to see sync event history to audit data transfers
**Acceptance Criteria:**
- Filter by user_id
- Return all sync events ordered by timestamp descending
- Each event displays: id, sync_session_id (linked), event_type (import_user, export_grade, sync_courses, etc.), payload (JSON with sync details), timestamp, status (success/failed)
- Show count of records processed in payload
- Paginated results
**Technical Notes:** Use existing SyncEvent model with LMS-specific event_types

---

## Estructura de Datos

```typescript
// User Model
interface User {
  id: number;
  username: string;           // 3-100 chars, unique
  email: EmailStr;             // unique, valid format
  password: string;            // hashed with bcrypt
  name: string;                // first name
  lastname: string;            // last name
  lms_id?: string;             // FK to LMSCredential.id
  avatar_url?: string;          // optional profile image URL
  is_active: boolean;          // default true
  last_login?: DateTime;
  role_id: number;             // FK to Role.id
  created_at: DateTime;
  updated_at: DateTime;
  deleted_at: DateTime;         // soft delete
  is_deleted: boolean;
}

// Role Model
interface Role {
  id: number;
  role_name: string;           // 'admin', 'professor', 'student'
  description?: string;
}

// Student Model
interface Student {
  id: number;
  user_id: number;             // FK to User.id
}

// Professor Model
interface Professor {
  id: number;
  user_id: number;             // FK to User.id
  department: string;
  contact_phone?: string;
}

// TeacherSettings Model
interface TeacherSettings {
  id: number;
  user_id: number;             // FK to User.id
  theme: 'light' | 'dark';     // default 'light'
  notifications_enabled: boolean;  // default true
  notification_frequency: 'instant' | 'daily' | 'weekly';  // default 'instant'
  interface_language: string;   // default 'es', 2-10 chars
}

// LMSCredential Model
interface LMSCredential {
  id: string;                  // UUID
  lms_email: string;           // unique
  lms_password: string;        // hashed
  lms_provider: string;         // 'moodle', 'canvas', etc.
  acces_token?: string;         // OAuth token
  expire_at?: DateTime;
}

// Game Model
interface Game {
  id: number;
  title: string;               // required, max 255 chars
  description?: string;        // max 255 chars
  creator?: string;            // max 255 chars
  subject?: string;            // max 255 chars
  publication_status?: string; // max 255 chars
  created_at: DateTime;        // server default
  updated_at?: DateTime;       // auto-updated
  deleted_at?: DateTime;       // for soft delete
  is_deleted: boolean;         // default false
  
  // Relationships (eager loaded on demand)
  levels: Level[];             // One-to-many relationship
  instances: GameInstance[];   // One-to-many relationship
}

// Level Model
interface Level {
  id: number;
  level_number: number;        // required
  title: string;               // required, max 255 chars
  description?: string;        // max 255 chars
  goal?: string;               // max 255 chars
  game_id: number;             // FK to Game.id
  created_at: DateTime;        // server default
  updated_at?: DateTime;       // auto-updated
  deleted_at?: DateTime;       // for soft delete
  is_deleted: boolean;         // default false
  
  // Relationships (eager loaded on demand)
  game: Game;                  // Many-to-one relationship
  segments: SegmentLevel[];    // One-to-many relationship
}

// SegmentLevel Model
interface SegmentLevel {
  id: number;
  configuration?: JSON;        // flexible config object
  level_number_id: number;     // FK to Level.id (mapped from level_id in API)
  created_at: DateTime;        // server default
  updated_at?: DateTime;       // auto-updated
  deleted_at?: DateTime;       // for soft delete
  is_deleted: boolean;         // default false
  
  // Relationships
  level: Level;                // Many-to-one relationship
}

// GameInstance Model
interface GameInstance {
  id: number;
  start_instance: DateTime;    // required, set on creation
  status?: string;             // max 255 chars (active/completed/abandoned)
  student_id: number;          // FK to Student.id
  game_id: number;             // FK to Game.id
  created_at: DateTime;        // server default
  updated_at?: DateTime;       // auto-updated
  deleted_at?: DateTime;       // for soft delete
  is_deleted: boolean;         // default false
  
  // Relationships (eager loaded on demand)
  game: Game;                  // Many-to-one relationship
  student: Student;            // Many-to-one relationship
}

// SyncSession Model
interface SyncSession {
  id: number;
  instance_id: number;         // FK to GameInstance.id
  start_time: DateTime;
  end_time?: DateTime;
  status: 'active' | 'completed';
}

// SyncEvent Model
interface SyncEvent {
  id: number;
  sync_session_id: number;     // FK to SyncSession.id
  event_type: string;          // 'player_move', 'level_complete', etc.
  payload: JSON;               // event-specific data
  timestamp: DateTime;
  status: 'synced' | 'failed';
}

// Progress Model
interface Progress {
  id: number;
  segment_level_id: number;    // FK to SegmentLevel.id
  attempt_count: number;       // default 0
  error_count: number;         // default 0
  hints_used_count: number;    // default 0
  errors_details?: JSON;       // array of error objects
  objectives_completed: number; // default 0
  efficiency_rating: number;   // 0-100, default 0
}

// Feedback Model
interface Feedback {
  id: number;
  student_id: number;          // FK to Student.id
  comments: string;            // 1-255 chars
  created_at: DateTime;
}

// MetricType Model
interface MetricType {
  id: number;
  name: string;
  description?: string;
}
```

---

## Reglas de Negocio

### Authentication & Authorization
- JWT tokens expire in 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Password must contain: 8+ characters, at least 1 uppercase, 1 lowercase, 1 number
- Password hashing uses bcrypt (passlib) with minimum strength
- Three user roles: `admin`, `professor`, `student`
- Only authenticated users can access protected endpoints (Bearer token required)
- Resource ownership checks: professors can only modify their own games/levels

### Role Management
- **Role Assignment Rules:**
  - `admin`: Assigned via seed data only (system initialization)
  - `professor`: **Automatically assigned** when registering via `/auth/register` endpoint
  - `student`: Assigned by professors when creating students via US-004
- **Role Validation:**
  - Registration endpoint does NOT accept `role_id` in request body
  - Role existence validated against database before assignment
  - If required role doesn't exist in DB, system throws NotFoundException (HTTP 500)
- **Seed Data Required:**
  - Roles table must be seeded before first registration
  - Run: `python -m src.shared.seed.run_seed` or execute migrations
  - Expected roles: `admin`, `professor`, `student`

### User Management
- Username must be 3-100 characters, unique across platform
- Email must be valid format, unique across platform
- Soft delete is used for all deletions (sets `is_deleted=True` and `deleted_at`)
- Active/inactive users distinguished by `is_active` flag
- Students linked to User via `student_id`, professors via `professor_id`

### Games & Levels
- Game titles are validated for uniqueness at database level (IntegrityError on duplicate)
- Game publication_status is optional string field (not enforced enum in DB)
- Level numbers must be unique within a game (composite constraint)
- Games and levels use soft delete (is_deleted flag + deleted_at timestamp)
- Soft delete does NOT cascade automatically; related entities remain but are filtered by is_deleted
- All endpoints return standardized response format: `{ success, message, data }`
- Eager loading: Game→levels, Level→segments, GameInstance→game+student loaded on demand via repository methods

### Game Instances & Progress
- Multiple instances allowed per (game_id, student_id) combination
- Instance status values: `active`, `completed`, `abandoned` (string field, not enforced enum)
- Instance status can be updated via PUT /game-instances/{id}/end endpoint
- start_instance timestamp set automatically by server on creation (datetime.utcnow())
- No end_instance timestamp field in current model
- All queries exclude is_deleted=True records by default
- GameInstanceRepository provides eager loading methods: get_by_id_with_relations(), get_all_with_relations()

### Sync Sessions & Events
- One active sync session per game instance
- Event types: `player_move`, `level_complete`, `item_collected`, `hint_used`, `error_occurred`, `import_user`, `export_grade`, `sync_courses`
- Payload is flexible JSON structure per event type
- Sessions auto-end after inactivity timeout (configurable, default 1 hour)
- Events stored with exact timestamp from game client

### Feedback System
- Rating scale: 1-5 stars, optional (defaults to 5 if not provided)
- Comments required, 1-255 characters, no HTML allowed
- Feedback immutable once submitted (no updates/deletes)
- Students can only submit their own feedback

### LMS Integration
- LMS credentials use `lms_email` as unique identifier (not user email)
- LMS password hashed separately from platform password
- OAuth flow refreshes `access_token` automatically
- Sync can be partial success if some records fail
- Sync triggered manually or scheduled (24-hour default interval)

### Pagination & Filtering
- Default pagination: `skip=0`, `limit=10`
- Max limit: 100 records per request
- `skip` must be >= 0
- Filters are AND logic (all must match)
- Search uses partial matching (LIKE %query%)

### Data Integrity
- All timestamps in UTC
- Foreign keys cascade soft delete appropriately
- Unique constraints validated before INSERT/UPDATE
- JSON fields validated for valid JSON format
- All write operations use async/await with explicit commit

### Domain Game - Implementation Summary

#### Endpoints Implemented (18 total)

**Games (`/api/v1/games`):**
- `POST /` - Create game (US-014)
- `GET /` - List games with pagination (US-015)
- `GET /{game_id}` - Get game detail with levels_count (US-016)
- `PUT /{game_id}` - Update game (US-017)
- `DELETE /{game_id}` - Soft delete game (US-018)

**Levels (`/api/v1/games/{game_id}/levels` & `/api/v1/levels`):**
- `POST /games/{game_id}/levels` - Create level (US-019)
- `GET /games/{game_id}/levels` - List levels with pagination (US-020)
- `GET /levels/{level_id}` - Get level detail with segments_count (US-021)
- `PUT /levels/{level_id}` - Update level (US-022)
- `DELETE /levels/{level_id}` - Soft delete level (US-023)

**Segments (`/api/v1/segments`):**
- `POST /{level_id}/segments` - Create segment level
- `GET /{level_id}/segments` - List segment levels
- `PUT /{segment_id}` - Update segment level
- `DELETE /{segment_id}` - Soft delete segment level

**Game Instances (`/api/v1/game-instances`):**
- `POST /{game_id}/instances` - Create game instance (US-024)
- `GET /{game_id}/instances` - List instances with status filter (US-025)
- `GET /{instance_id}` - Get instance detail with game_title (US-026)
- `PUT /{instance_id}/end` - End game instance (US-027)

#### Response Schemas
All endpoints return standardized response format:
```typescript
// Base Response
interface ResponseSchema {
  success: boolean;
  message: string;
  data?: any;
}

// List Response (for paginated endpoints)
interface ListResponseSchema extends ResponseSchema {
  data: any[];
  total: number;
  skip: number;
  limit: number;
}

// Game Schemas
interface GameBase {
  title: string;
  description?: string;
  creator?: string;
  subject?: string;
  publication_status?: string;
}

interface GameCreate extends GameBase {}
interface GameUpdate extends Partial<GameBase> {}
interface GameResponse extends GameBase {
  id: number;
  created_at: string;
  updated_at?: string;
  is_deleted: boolean;
}

interface GameDetailResponse extends GameResponse {
  levels_count: number;
}

// Level Schemas
interface LevelBase {
  level_number: number;
  title: string;
  description?: string;
  goal?: string;
}

interface LevelCreate extends LevelBase {
  game_id?: number;  // Set from URL path
}

interface LevelUpdate extends Partial<LevelBase> {}

interface LevelResponse extends LevelBase {
  id: number;
  game_id: number;
  created_at: string;
  updated_at?: string;
  is_deleted: boolean;
}

interface LevelDetailResponse extends LevelResponse {
  segments_count: number;
}

// SegmentLevel Schemas
interface SegmentLevelCreate {
  level_id?: number;  // Set from URL path
  configuration?: object;
}

interface SegmentLevelUpdate {
  configuration?: object;
}

interface SegmentLevelResponse {
  id: number;
  level_id: number;  // Alias for level_number_id
  configuration?: object;
  created_at: string;
  updated_at?: string;
  is_deleted: boolean;
}

// GameInstance Schemas
interface GameInstanceCreate {
  game_id?: number;  // Set from URL path
  student_id: number;
  status?: string;   // Default: "active"
}

interface GameInstanceEnd {
  status?: string;   // Default: "completed"
}

interface GameInstanceResponse {
  id: number;
  game_id: number;
  student_id: number;
  status: string;
  start_instance: string;
  created_at: string;
  updated_at?: string;
  is_deleted: boolean;
}

interface GameInstanceDetailResponse extends GameInstanceResponse {
  game_title?: string;
}
```

#### Repository Pattern with Eager Loading

**GameRepository:**
- `get_by_id_with_levels(id)` - Get game with levels eagerly loaded
- `get_all_with_levels(skip, limit)` - List games with levels eagerly loaded

**LevelRepository:**
- `get_by_id_with_segments(id)` - Get level with segments eagerly loaded
- `get_by_game_id_with_segments(game_id)` - List levels with segments eagerly loaded

**GameInstanceRepository:**
- `get_by_id_with_relations(id)` - Get instance with game and student eagerly loaded
- `get_all_with_relations(skip, limit)` - List instances with relations eagerly loaded

#### Key Implementation Details

1. **Soft Delete**: All entities use soft delete via BaseRepository.delete() which sets is_deleted=True and deleted_at timestamp
2. **Field Mapping**: SegmentLevel uses level_number_id in DB but exposes as level_id in API via Pydantic Field alias
3. **URL Parameters**: game_id and level_id in URLs are set automatically, not from request body
4. **Timestamps**: start_instance, created_at, updated_at set automatically by server
5. **Validation**: 404 returned when parent resource doesn't exist (e.g., game not found when creating level)
6. **Partial Updates**: PUT endpoints accept partial data (only provided fields are updated)

### Error Handling
- HTTP 400: DuplicateEntryException (unique constraint violations), validation errors
- HTTP 401: InvalidCredentialsException (auth failures)
- HTTP 403: UnauthorizedException (permission denied)
- HTTP 404: NotFoundException (resource not found or parent resource not found)
- HTTP 500: DatabaseException (unexpected DB errors)

### Response Format
- All responses use standard schema: `{ success: boolean, message: string, data?: any, error?: any }`
- List responses include pagination metadata
- Datetime fields formatted as ISO 8601 strings
- Password fields never included in responses
- Sensitive data (tokens, passwords) masked in logs
