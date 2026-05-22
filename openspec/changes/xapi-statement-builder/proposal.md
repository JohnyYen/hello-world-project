# Proposal: xAPI Statement Builder Service (Game Side)

## Intent

Implementar en el juego (Godot 4.x / GDScript) un sistema de tracking xAPI que permita:
1. Construir sentencias xAPI válidas a partir de eventos del juego
2. Almacenarlas localmente en SQLite
3. Sincronizarlas con el backend cuando haya conexión disponible
4. Mantener soporte offline (cola de batches pendientes)

**Problema**: El juego necesita registrar learning events en formato xAPI para cumplir con estándares de e-learning, pero debe funcionar offline y sincronizar cuando haya conectividad.

## Scope

### In Scope
- **Modelo SQLite `xapi_statement`**: Almacenar statements xAPI construidos
- **Modelo SQLite `pending_batch`**: Cola de batches pendientes de sync
- **XAPIBuilderService**: Transforma datos crudos → statements xAPI válidos
- **SyncBatchService**: Gestiona envío de batches al backend con retry offline
- **ConnectionDetector**: Detecta conectividad y triggereando sync automático

### Out of Scope
- UI para visualizar statements
- Procesamiento de statements en el backend (eso es otro cambio)
- Dashboard de analytics en el juego

## Approach

### Arquitectura

```
[Juego Events]
    │
    ▼
XAPIBuilderService ──► SQLite (xapi_statement)
    │                        │
    │                        ▼
    │               SyncBatchService
    │                        │
    ▼                        ▼
ConnectionDetector ◄──► Backend API (sync_events)
     │
     ▼ (si hay conexión)
PendingBatchRepository (retry logic)
```

### Estructura de Archivos (Game)

```
apps/game/scripts/
├── database/
│   ├── repositories/
│   │   ├── xapi_statement_repository.gd      # CRUD para statements
│   │   └── pending_batch_repository.gd        # CRUD para batches pendientes
│   └── migrations/
│       └── 001_create_xapi_tables.gd           # Setup SQLite schema
├── xapi/
│   ├── builder/
│   │   ├── xapi_builder_service.gd            # Factory de statements
│   │   └── verbs.gd                           # Definiciones de verbos xAPI
│   └── sync/
│       ├── sync_batch_service.gd              # Envío de batches al backend
│       └── connection_detector.gd             # Detección de conectividad
└── core/
    └── config/
        └── xapi_config.gd                     # Configuración de xAPI
```

### Modelos SQLite

#### xapi_statement

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | TEXT (UUID) | PK |
| `verb_id` | TEXT | URI del verbo xAPI (ej: `http://adlnet.gov/expapi/verbs/completed`) |
| `verb_display` | TEXT | Display string del verbo |
| `object_type` | TEXT | Tipo de objeto (course, level, assessment, game) |
| `object_id` | TEXT | ID del objeto |
| `object_name` | TEXT | Nombre del objeto |
| `actor_id` | TEXT | UUID del usuario |
| `result_score_raw` | REAL | Score raw (nullable) |
| `result_score_scaled` | REAL | Score como decimal 0-1 (nullable) |
| `result_success` | INTEGER | 0/1 - Boolean (nullable) |
| `result_completion` | INTEGER | 0/1 - Boolean (nullable) |
| `result_duration` | TEXT | Duración ISO 8601 (nullable) |
| `context_extensions` | TEXT | JSON con contexto adicional (nullable) |
| `timestamp` | TEXT | ISO 8601 timestamp |
| `created_at` | TEXT | Fecha de creación |
| `batch_id` | TEXT | UUID del batch al que pertenece (nullable) |

#### pending_batch

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | TEXT (UUID) | PK |
| `statements` | TEXT | JSON array de statement IDs |
| `payload` | TEXT | JSON con formato sync_event |
| `status` | TEXT | pending/sending/failed |
| `retry_count` | INTEGER | Intentos de reintento |
| `last_error` | TEXT | Último error (nullable) |
| `created_at` | TEXT | Fecha de creación |
| `last_attempt_at` | TEXT | Último intento (nullable) |

### Verbos xAPI Definidos

```gdscript
const VERBS := {
    "attempted": {
        "id": "http://adlnet.gov/expapi/verbs/attempted",
        "display": {"en-US": "attempted", "es": "intentó"}
    },
    "completed": {
        "id": "http://adlnet.gov/expapi/verbs/completed",
        "display": {"en-US": "completed", "es": "completó"}
    },
    "answered": {
        "id": "http://adlnet.gov/expapi/verbs/answered",
        "display": {"en-US": "answered", "es": "respondió"}
    },
    "initialized": {
        "id": "http://adlnet.gov/expapi/verbs/initialized",
        "display": {"en-US": "initialized", "es": "inició"}
    },
    "terminated": {
        "id": "http://adlnet.gov/expapi/verbs/terminated",
        "display": {"en-US": "terminated", "es": "finalizó"}
    },
    "passed": {
        "id": "http://adlnet.gov/expapi/verbs/passed",
        "display": {"en-US": "passed", "es": "aprobó"}
    },
    "failed": {
        "id": "http://adlnet.gov/expapi/verbs/failed",
        "display": {"en-US": "failed", "es": "falló"}
    }
}
```

### Formato de Sync al Backend

El batch se envía al endpoint `POST /api/v1/sync/sync-sessions` y `POST /api/v1/sync/sync-events` según la estructura actual del backend:

```json
// Start session
{
  "instance_id": "game-instance-uuid"
}

// Sync events (uno por statement)
{
  "sync_session_id": "session-uuid",
  "event_type": "xapi_statement",
  "payload": {
    "statement_id": "xapi-statement-uuid",
    "verb_id": "http://adlnet.gov/expapi/verbs/completed",
    "verb_display": "completed",
    "object_type": "level",
    "object_id": "level_1",
    "object_name": "Nivel 1",
    "actor_id": "user-uuid",
    "result": {
      "score_raw": 85,
      "score_scaled": 0.85,
      "success": true,
      "duration": "PT2M30S"
    },
    "timestamp": "2025-05-12T10:30:00Z"
  }
}
```

### Offline Support

```
┌─────────────────────────────────────────────────────────┐
│                    Offline Flow                         │
├─────────────────────────────────────────────────────────┤
│  1. Evento ocurre → XAPIBuilderService.create()        │
│  2. Statement guardado en SQLite                        │
│  3. ConnectionDetector.check() → sin conexión           │
│  4. Batch se marca como "pending"                       │
│  5. Timer polling (cada 30s)                            │
│  6. Conexión disponible → SyncBatchService.process()    │
│  7. Envío batch al backend                              │
│  8. Si falla → retry con backoff (1s, 2s, 4s, 8s...)    │
│  9. Max 5 retries, luego marcar "failed"                │
└─────────────────────────────────────────────────────────┘
```

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `apps/game/scripts/database/repositories/` | New | xapi_statement y pending_batch repos |
| `apps/game/scripts/xapi/` | New | Módulo completo de xAPI |
| `apps/game/scripts/core/config/` | Modified | Agregar xapi_config.gd |
| `apps/game/scripts/controllers/service/` | Modified | Integrar con SyncService existente |
| `apps/game/scripts/http/api_client.gd` | Modified | Agregar método para batch |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Datos corruptos en SQLite offline | Low | Validación en builder, rollback si falla |
| Batch muy grande para el backend | Medium | Chunking en batches de 50 statements |
| Pérdida de datos si app se cierra | Low | statements en SQLite inmediatos, batch en transaction |
| Retry loop infinito | Low | Max 5 retries, luego marcar failed para revisión manual |

## Rollback Plan

1. Eliminar archivos del módulo `xapi/`
2. Eliminar repositorios si no se usan en otros lados
3. Revertir cambios en `api_client.gd` y `sync_service.gd`
4. La migración SQLite puede quedarse (no afecta si no se usa)

## Dependencies

- GDScript 2.0
- SQLite plugin para Godot
- ApiClient existente (para hacer los requests HTTP)
- SyncService existente (como referencia)
- Config del juego (`env.gd`)

## Success Criteria

- [ ] `XAPIBuilderService.build(verb, object, result)` retorna statement válido
- [ ] Statement se guarda en SQLite inmediatamente
- [ ] `PendingBatchRepository` mantiene cola de batches
- [ ] `ConnectionDetector` detecta conexión y emite señal
- [ ] `SyncBatchService` envía batches cuando hay conexión
- [ ] Retry logic funciona con backoff exponencial
- [ ] Sin conexión: todo funciona offline, se sincroniza después