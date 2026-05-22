# Design: xAPI Statement Builder Service

## Technical Approach

Implementar un sistema xAPI en Godot que construye statements válidos, los persiste en SQLite localmente, y los sincroniza con el backend usando batch processing con soporte offline completo.

**Mapeo al Proposal:**
- `XAPIBuilderService` transforma eventos del juego → statements xAPI válidos
- Repositorios SQLite para persistencia local (`xapi_statement`, `pending_batch`)
- `ConnectionDetector` monitorea conectividad y emite señales
- `SyncBatchService` gestiona envío de batches con retry exponencial

## Architecture Decisions

### Decision: Repository Pattern para SQLite

**Choice**: Crear `XAPIStatementRepository` y `PendingBatchRepository` separados
**Alternatives considered**: Un solo repositorio genérico o queries directas en los servicios
**Rationale**: Separa responsabilidades (persistencia vs lógica de negocio), facilita testing unitario, sigue el patrón existente del proyecto (`LevelRepository`)

### Decision: Signals para Conectividad

**Choice**: `ConnectionDetector` emite señal `connection_changed(is_connected: bool)`
**Alternatives considered**: Polling activo en `SyncBatchService`, callbacks directos
**Rationale**: Desacopla detección de conectividad del proceso de sync, permite que múltiples componentes escuchen cambios de conexión, patrón usado en el proyecto (`ApiClient` usa señales)

### Decision: Batch Processing con Chunking

**Choice**: Statements agrupados en batches de 50, enviados secuencialmente
**Alternatives considered**: Un request por statement, bulk gigante
**Rationale**: Balance entre throughput y resiliencia - si falla un batch pequeño se reintenta rápido; si falla bulk gigante se pierde todo el progreso

### Decision: Retry con Exponential Backoff

**Choice**: `1s, 2s, 4s, 8s, 16s` hasta máximo 5 intentos
**Alternatives considered**: Retry infinito, sin retry, backoff lineal
**Rationale**: Exponencial reduce server load en problemas de conectividad; 5 intentos permiten recuperación rápida en conexiones inestables sin loop infinito

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         GAME EVENT                                    │
│  (level_completed, problem_solved, game_initialized, etc.)           │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       XAPIBuilderService                              │
│  build(verb, object, result) → XAPIStatement                          │
│  1. Valida verb existe                                                │
│  2. Valida object tiene campos requeridos                             │
│  3. Genera UUID para statement                                        │
│  4. Agrega timestamp ISO 8601                                         │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   XAPIStatementRepository                              │
│  save(statement) → SQLite                                             │
│  - Persistencia inmediata en transaction                              │
│  - Retorna statement_id para tracking                                 │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
         ┌──────────────────┐     ┌────────────────────────┐
         │ connection: true  │     │ connection: false       │
         └────────┬─────────┘     └────────────┬─────────────┘
                  │                            │
                  ▼                            ▼
    ┌────────────────────┐        ┌─────────────────────────┐
    │ SyncBatchService   │        │ Mark batch as PENDING   │
    │ process_batch()    │        │ Wait for next poll      │
    └────────┬───────────┘        └─────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │ POST /sync-events  │
    │ (ApiClient)        │
    └────────┬───────────┘
             │
    ┌────────┴─────────┐
    │                  │
    ▼                  ▼
 SUCCESS            FAILURE
    │                  │
    ▼                  ▼
 Delete batch     Retry with backoff
                  (max 5 attempts)
```

### Offline Sync Sequence Diagram

```
Actor              Game Events          XAPIBuilderService    Repositories         ConnectionDetector       SyncBatchService         ApiClient
   │                     │                      │                     │                        │                        │                    │
   │ level_completed     │                      │                     │                        │                        │                    │
   │────────────────────>│                      │                     │                        │                        │                    │
   │                     │ build(verb, obj)     │                     │                        │                        │                    │
   │                     │─────────────────────>│                     │                        │                        │                    │
   │                     │                      │ validate & create   │                        │                        │                    │
   │                     │                      │ statement_id        │                        │                        │                    │
   │                     │                      │                     │                        │                        │                    │
   │                     │ save(statement)      │                     │                        │                        │                    │
   │                     │──────────────────────────────────────────>│                        │                        │                    │
   │                     │                      │                     │ persist to SQLite      │                        │                    │
   │                     │                      │                     │<─────────────────────────────────────────         │                    │
   │                     │                      │                     │                        │                        │                    │
   │                     │<─────────────────────│                     │                        │                        │                    │
   │                     │ {statement_id}       │                     │                        │                        │                    │
   │                     │                      │                     │                        │                        │                    │
   │                     │                      │                     │ check_connection()      │                        │                    │
   │                     │                      │                     │<─────────────────────────────────────          │                    │
   │                     │                      │                     │                        │                        │                    │
   │                     │                      │                     │           NO ──────────┼────> Create PENDING batch│
   │                     │                      │                     │                        │                        │                    │
   │                     │                      │                     │           YES ─────────┼────> process_batch() │
   │                     │                      │                     │                        │                        │                    │
   │                     │                      │                     │                        │        get_pending_batches()
   │                     │                      │                     │                        │──────────────────────>│
   │                     │                      │                     │                        │                        │                    │
   │                     │                      │                     │                        │        create_payload()
   │                     │                      │                     │                        │──────────────────────>│
   │                     │                      │                     │                        │                        │                    │
   │                     │                      │                     │                        │        sync_events(payload)
   │                     │                      │                     │                        │                        │─────────>POST /sync-events
   │                     │                      │                     │                        │                        │                    │
   │                     │                      │                     │                        │                        │<─────────200 OK
   │                     │                      │                     │                        │                        │                    │
   │                     │                      │                     │                        │        mark_complete() │
   │                     │                      │                     │                        │──────────────────────>│
   │                     │                      │                     │                        │                        │                    │
```

## File Structure

```
apps/game/scripts/
├── database/
│   ├── repositories/
│   │   ├── xapi_statement_repository.gd       # CRUD statements xAPI
│   │   └── pending_batch_repository.gd         # CRUD batches pendientes
│   └── migrations/
│       └── 001_create_xapi_tables.gd            # Migration runner
├── xapi/
│   ├── xapi_builder_service.gd                 # Factory de statements
│   ├── xapi_verbs.gd                           # Definiciones verbos xAPI
│   ├── xapi_statement.gd                       # Data class para statement
│   ├── sync/
│   │   ├── sync_batch_service.gd               # Batch processing
│   │   └── connection_detector.gd              # Connectivity detection
│   └── sync_manager.gd                        # Orchestrates all xAPI components
└── core/
    └── config/
        └── xapi_config.gd                     # Configuración centralizada
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `apps/game/scripts/xapi/xapi_statement.gd` | Create | Data class con validación para statement |
| `apps/game/scripts/xapi/xapi_verbs.gd` | Create | Constantes de verbos xAPI |
| `apps/game/scripts/xapi/xapi_builder_service.gd` | Create | Factory service para construir statements |
| `apps/game/scripts/xapi/sync/connection_detector.gd` | Create | Detección de conectividad con señales |
| `apps/game/scripts/xapi/sync/sync_batch_service.gd` | Create | Batch processing con retry |
| `apps/game/scripts/xapi/sync_manager.gd` | Create | Orchestrator que conecta todos los componentes |
| `apps/game/scripts/database/repositories/xapi_statement_repository.gd` | Create | Repository para statements SQLite |
| `apps/game/scripts/database/repositories/pending_batch_repository.gd` | Create | Repository para batches SQLite |
| `apps/game/scripts/database/migrations/001_create_xapi_tables.gd` | Create | Migration script para SQLite |
| `apps/game/scripts/core/config/xapi_config.gd` | Create | Configuración xAPI |
| `apps/game/scripts/database/connect.gd` | Modify | Agregar llamada a migración xAPI |
| `apps/game/scripts/http/api_client.gd` | Modify | Agregar método `sync_xapi_batch()` |

## Interfaces / Contracts

### XAPIStatement (Data Class)

```gdscript
class_name XAPIStatement
extends RefCounted

var id: String
var verb_id: String
var verb_display: String
var object_type: String
var object_id: String
var object_name: String
var actor_id: String
var result: XAPIResult
var timestamp: String
var created_at: String
var batch_id: String

func _init(
    p_id: String,
    p_verb_id: String,
    p_verb_display: String,
    p_object_type: String,
    p_object_id: String,
    p_object_name: String,
    p_actor_id: String,
    p_result: XAPIResult = null,
    p_timestamp: String = ""
) -> void:
    id = p_id
    verb_id = p_verb_id
    verb_display = p_verb_display
    object_type = p_object_type
    object_id = p_object_id
    object_name = p_object_name
    actor_id = p_actor_id
    result = p_result
    timestamp = p_timestamp if p_timestamp != "" else Time.get_datetime_as_iso_string(true)
    created_at = Time.get_datetime_as_iso_string(true)
    batch_id = ""

func to_dict() -> Dictionary:
    var dict := {
        "statement_id": id,
        "verb_id": verb_id,
        "verb_display": verb_display,
        "object_type": object_type,
        "object_id": object_id,
        "object_name": object_name,
        "actor_id": actor_id,
        "timestamp": timestamp
    }
    if result:
        dict["result"] = result.to_dict()
    return dict

static func from_dict(data: Dictionary) -> XAPIStatement:
    var res: XAPIResult = null
    if data.has("result"):
        res = XAPIResult.from_dict(data["result"])
    return XAPIStatement.new(
        data.get("id", ""),
        data.get("verb_id", ""),
        data.get("verb_display", ""),
        data.get("object_type", ""),
        data.get("object_id", ""),
        data.get("object_name", ""),
        data.get("actor_id", ""),
        res,
        data.get("timestamp", "")
    )
```

### XAPIResult (Value Object)

```gdscript
class_name XAPIResult
extends RefCounted

var score_raw: float
var score_scaled: float
var success: bool
var completion: bool
var duration: String

func _init(
    p_score_raw: float = -1.0,
    p_score_scaled: float = -1.0,
    p_success: bool = false,
    p_completion: bool = false,
    p_duration: String = ""
) -> void:
    score_raw = p_score_raw
    score_scaled = p_score_scaled
    success = p_success
    completion = p_completion
    duration = p_duration

func to_dict() -> Dictionary:
    var dict := {}
    if score_raw >= 0:
        dict["score_raw"] = score_raw
    if score_scaled >= 0:
        dict["score_scaled"] = score_scaled
    if success:
        dict["success"] = true
    if completion:
        dict["completion"] = true
    if duration != "":
        dict["duration"] = duration
    return dict

static func from_dict(data: Dictionary) -> XAPIResult:
    return XAPIResult.new(
        data.get("score_raw", -1.0),
        data.get("score_scaled", -1.0),
        data.get("success", false),
        data.get("completion", false),
        data.get("duration", "")
    )
```

### XAPIBuilderService Interface

```gdscript
class_name XAPIBuilderService
extends Node

signal statement_created(statement: XAPIStatement)
signal statement_error(error: String)

func build(
    verb_key: String,
    object_type: String,
    object_id: String,
    object_name: String,
    actor_id: String,
    result: XAPIResult = null,
    context_extensions: Dictionary = {}
) -> XAPIStatement:
    pass

func build_level_started(level_id: String, level_name: String, actor_id: String) -> XAPIStatement:
    pass

func build_level_completed(level_id: String, level_name: String, actor_id: String, result: XAPIResult) -> XAPIStatement:
    pass

func build_problem_solved(problem_id: String, problem_name: String, actor_id: String, success: bool) -> XAPIStatement:
    pass

func build_game_initialized(game_instance_id: String, actor_id: String) -> XAPIStatement:
    pass

func build_game_terminated(game_instance_id: String, actor_id: String, duration: String) -> XAPIStatement:
    pass
```

### ConnectionDetector Interface

```gdscript
class_name ConnectionDetector
extends Node

signal connection_changed(is_connected: bool)
signal connection_checked(available: bool)

var is_online: bool = false
var poll_interval: float = 30.0  # segundos

func start_monitoring() -> void:
    pass

func stop_monitoring() -> void:
    pass

func check_now() -> bool:
    pass
```

### SyncBatchService Interface

```gdscript
class_name SyncBatchService
extends Node

signal batch_sent(batch_id: String, count: int)
signal batch_failed(batch_id: String, error: String)
signal sync_completed(total_sent: int)
signal sync_failed(error: String)

var max_batch_size: int = 50
var max_retries: int = 5
var base_retry_delay: float = 1.0  # segundos

func _ready() -> void:
    pass

func queue_statement(statement_id: String) -> void:
    pass

func process_pending_batches() -> void:
    pass

func force_sync() -> void:
    pass

func get_pending_count() -> int:
    pass
```

### PendingBatchStatus (Enum)

```gdscript
enum PendingBatchStatus {
    PENDING = "pending",
    SENDING = "sending",
    FAILED = "failed"
}
```

### Repository Interfaces

```gdscript
class_name XAPIStatementRepository
extends Node

func save(statement: XAPIStatement) -> bool:
    pass

func save_batch(statements: Array[XAPIStatement]) -> bool:
    pass

func get_by_id(statement_id: String) -> XAPIStatement:
    pass

func get_unbatched(limit: int = 100) -> Array[XAPIStatement]:
    pass

func mark_as_batched(statement_ids: Array[String], batch_id: String) -> bool:
    pass

func delete_by_batch_id(batch_id: String) -> bool:
    pass

func count() -> int:
    pass
```

```gdscript
class_name PendingBatchRepository
extends Node

func create_batch(statement_ids: Array[String], payload: Dictionary) -> String:
    pass

func get_pending_batches() -> Array[Dictionary]:
    pass

func update_status(batch_id: String, status: String, error: String = "") -> bool:
    pass

func increment_retry(batch_id: String) -> int:
    pass

func get_batch(batch_id: String) -> Dictionary:
    pass

func delete_batch(batch_id: String) -> bool:
    pass

func get_retry_count(batch_id: String) -> int:
    pass
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `XAPIBuilderService.build()` | Mock repository, verify statement structure |
| Unit | `XAPIResult.to_dict()` | Verify ISO 8601 duration format |
| Unit | `ConnectionDetector.check_now()` | Mock HTTP response |
| Unit | `SyncBatchService.retry_logic()` | Mock repository, verify backoff |
| Integration | `XAPIStatementRepository.save()` | Real SQLite, verify persistence |
| Integration | Full offline → online flow | Mock connection detector |

**Test Coverage Target:** 70%

## Migration / Rollback

### Migration Script (001_create_xapi_tables.gd)

```gdscript
class_name CreateXAPITablesMigration
extends Node

func run(db: SQLite) -> bool:
    # Crear tabla xapi_statement
    var xapi_statement_schema := {
        "id": {"data_type": "text", "primary_key": true},
        "verb_id": {"data_type": "text", "not_null": true},
        "verb_display": {"data_type": "text", "not_null": true},
        "object_type": {"data_type": "text", "not_null": true},
        "object_id": {"data_type": "text", "not_null": true},
        "object_name": {"data_type": "text", "not_null": true},
        "actor_id": {"data_type": "text", "not_null": true},
        "result_score_raw": {"data_type": "real"},
        "result_score_scaled": {"data_type": "real"},
        "result_success": {"data_type": "integer"},
        "result_completion": {"data_type": "integer"},
        "result_duration": {"data_type": "text"},
        "context_extensions": {"data_type": "text"},
        "timestamp": {"data_type": "text", "not_null": true},
        "created_at": {"data_type": "text", "not_null": true},
        "batch_id": {"data_type": "text"}
    }
    db.create_table("xapi_statement", xapi_statement_schema)

    # Crear tabla pending_batch
    var pending_batch_schema := {
        "id": {"data_type": "text", "primary_key": true},
        "statements": {"data_type": "text", "not_null": true},
        "payload": {"data_type": "text", "not_null": true},
        "status": {"data_type": "text", "not_null": true},
        "retry_count": {"data_type": "integer", "not_null": true, "default": "0"},
        "last_error": {"data_type": "text"},
        "created_at": {"data_type": "text", "not_null": true},
        "last_attempt_at": {"data_type": "text"}
    }
    db.create_table("pending_batch", pending_batch_schema)

    # Crear índices
    db.query("CREATE INDEX IF NOT EXISTS idx_xapi_batch ON xapi_statement(batch_id);")
    db.query("CREATE INDEX IF NOT EXISTS idx_xapi_timestamp ON xapi_statement(timestamp);")
    db.query("CREATE INDEX IF NOT EXISTS idx_batch_status ON pending_batch(status);")

    print("Migration 001_create_xapi_tables: OK")
    return true
```

### Rollback Plan

1. Eliminar `apps/game/scripts/xapi/` (módulo completo)
2. Eliminar `apps/game/scripts/database/repositories/xapi_statement_repository.gd`
3. Eliminar `apps/game/scripts/database/repositories/pending_batch_repository.gd`
4. Eliminar `apps/game/scripts/database/migrations/001_create_xapi_tables.gd`
5. Eliminar `apps/game/scripts/core/config/xapi_config.gd`
6. Revertir cambios en `connect.gd` (quitar llamada a migración)
7. Revertir cambios en `api_client.gd` (quitar método `sync_xapi_batch`)

**Nota**: La migración SQLite no afecta si no se ejecuta (no hay tables creadas).

## Open Questions

- [ ] ¿El `game_instance_id` para `game_initialized` viene del backend o se genera localmente?
- [ ] ¿Cuántos statements máximos deberían guardarse offline antes de forzar sync?
- [ ] ¿Debe haber una UI de debug para ver statements pendientes en desarrollo?
- [ ] ¿Los `context_extensions` tienen un schema definido o son libres?
