# Tasks: xAPI Statement Builder Service

## Phase 1: Infrastructure

- [ ] 1.1 Crear directorio `apps/game/scripts/xapi/` y subdirectorios `builder/` y `sync/`
- [ ] 1.2 Crear directorio `apps/game/scripts/core/config/` si no existe
- [ ] 1.3 Crear `apps/game/scripts/xapi/verbs.gd` con constantes VERBS y mapa de verbos xAPI (attempted, completed, answered, initialized, terminated, passed, failed)
- [ ] 1.4 Crear `apps/game/scripts/core/config/xapi_config.gd` con configuracion de xAPI (batch size=50, retry max=5, poll interval=30s, backend URLs)
- [ ] 1.5 Agregar migracion en `apps/game/scripts/database/connect.gd`: metodo `on_create_xapi_tables()` que cree las tablas `xapi_statement` y `pending_batch` segun el schema del proposal
- [ ] 1.6 Agregar llamada a `on_create_xapi_tables()` en la secuencia de `create_tables()`

## Phase 2: Domain Models (Repositories)

- [ ] 2.1 Crear `apps/game/scripts/xapi/xapi_statement_repository.gd` — clase `XAPIStatementRepository` con `_init()`, CRUD: `create(statement: Dictionary) -> String`, `get_by_id(id: String) -> Dictionary`, `get_pending(batch_id: String) -> Array[Dictionary]`, `get_all_unbatched() -> Array[Dictionary]`, `mark_as_batched(statement_ids: Array, batch_id: String) -> void`
- [ ] 2.2 Crear `apps/game/scripts/xapi/pending_batch_repository.gd` — clase `PendingBatchRepository` con `_init()`, CRUD: `create(payload: Dictionary) -> String`, `get_pending() -> Dictionary`, `get_by_id(id: String) -> Dictionary`, `update_status(id: String, status: String, error: String) -> void`, `increment_retry(id: String) -> int`, `delete(id: String) -> void`, `get_failed() -> Array[Dictionary]`

## Phase 3: Core Services

- [ ] 3.1 Crear `apps/game/scripts/xapi/builder/xapi_builder_service.gd` — clase `XAPIBuilderService` con metodo `build(verb_key: String, object_data: Dictionary, actor_id: String, result: Dictionary, context_extensions: Dictionary) -> Dictionary` que construya un statement xAPI valido usando verbs.gd y lo guarde via XAPIStatementRepository. Retorna el statement creado con UUID
- [ ] 3.2 Crear `apps/game/scripts/xapi/sync/connection_detector.gd` — clase `ConnectionDetector` que extienda `Node`, tenga senal `connection_changed(is_online: bool)`, y un timer de polling. Usar HTTP request a `XAPIConfig.BASE_URL + "/health"` o similar para detectar conectividad
- [ ] 3.3 Crear `apps/game/scripts/xapi/sync/sync_batch_service.gd` — clase `SyncBatchService` que extienda `Node`, tenga senales `batch_sent(batch_id: String)`, `batch_failed(batch_id: String, error: String)`, `sync_completed()`. Reciba senal de ConnectionDetector. Implemente retry con backoff exponencial (1s, 2s, 4s, 8s...) usando XAPIConfig

## Phase 4: Integration

- [ ] 4.1 Modificar `apps/game/scripts/http/api_client.gd`: agregar metodo `sync_xapi_batch(session_id: String, batch_payload: Dictionary) -> Dictionary` que use `register_sync_event` con `event_type="xapi_statement"`
- [ ] 4.2 Modificar `apps/game/scripts/controllers/service/sync_service.gd`: crear nueva escena/autoload `XAPIService.gd` que use `XAPIBuilderService`, `ConnectionDetector` y `SyncBatchService` para coordinar el flujo completo. Integrar con `ApiClient` existente para el envio de batches
- [ ] 4.3 Crear escena `apps/game/scenes/services/xapi_service.tscn` que cargue y expose `XAPIService` como autoload o nodo singleton
- [ ] 4.4 Documentar en comentarios la API publica de `XAPIService` para que otros desarrolladores puedan usar `XAPIBuilderService.build()` facilmente

## Phase 5: Testing

- [ ] 5.1 Crear `apps/game/test/unit/xapi/test_xapi_builder_service.gd` — tests unitarios para XAPIBuilderService: test que verifique que build() retorna statement con campos obligatorios, test de verbos validos, test de timestamp ISO 8601
- [ ] 5.2 Crear `apps/game/test/unit/xapi/test_connection_detector.gd` — tests para ConnectionDetector: test de senal emitida cuando hay/sin conexion
- [ ] 5.3 Crear `apps/game/test/unit/xapi/test_sync_batch_service.gd` — tests para SyncBatchService: test de retry logic, test de backoff exponencial, test de senales batch_sent/batch_failed
- [ ] 5.4 Crear `apps/game/test/unit/xapi/test_xapi_statement_repository.gd` — tests para XAPIStatementRepository usando GutTest con mock de SQLite
- [ ] 5.5 Crear `apps/game/test/unit/xapi/test_pending_batch_repository.gd` — tests para PendingBatchRepository con mock de SQLite

## Phase 6: Cleanup

- [ ] 6.1 Verificar que todos los archivos usen type hints explicitos y `class_name` donde corresponde
- [ ] 6.2 Verificar que no haya hardcoded config values fuera de `xapi_config.gd` y `Env`
- [ ] 6.3 Agregar print statements de debug consistent con el resto del proyecto (formato `print("DEBUG [XAPIBuilderService]: mensaje")`)
