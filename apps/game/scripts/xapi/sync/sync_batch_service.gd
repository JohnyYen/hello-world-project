# SyncBatchService.gd
# Gestiona el envío de batches xAPI al backend con soporte offline
class_name SyncBatchService
extends Node

## Señales
signal sync_started()
signal sync_completed(success_count: int, failed_count: int)
signal sync_failed(error: String)
signal batch_sent(batch_id: String, success: bool)
signal pending_count_updated(count: int)

## Dependencias
var _xapi_repository: XAPIStatementRepository
var _batch_repository: PendingBatchRepository
var _connection_detector: ConnectionDetector
var _api_client: ApiClient
var _config: XAPIConfig
var _session_repository: GameSessionRepository  # Cache local de game_id e instance_id
var _raw_stats_repository: RawStatsRepository  # Offline-first raw stats persistence

## Estado
var _is_syncing: bool = false
var _is_processing_batch: bool = false  # Lock interno para process_batch
var _retry_timer: Timer
var _periodic_timer: Timer
var _debounce_timer: Timer
var _debounce_guard: bool = false
var _pending_retry_batches: Array = []

func _init() -> void:
	_xapi_repository = XAPIStatementRepository.new()
	_batch_repository = PendingBatchRepository.new()
	_config = XAPIConfig.new()
	_session_repository = GameSessionRepository.new()
	_raw_stats_repository = RawStatsRepository.new()

func _ready() -> void:
	# Crear timer para reintentos
	_retry_timer = Timer.new()
	add_child(_retry_timer)
	_retry_timer.timeout.connect(_on_retry_timeout)

	# Timer periódico para sync de respaldo (60s)
	_periodic_timer = Timer.new()
	add_child(_periodic_timer)
	_periodic_timer.wait_time = _config.PERIODIC_SYNC_INTERVAL_SECONDS
	_periodic_timer.one_shot = false
	_periodic_timer.timeout.connect(_on_periodic_timeout)

	# Timer para debounce de señal pending_count_updated
	_debounce_timer = Timer.new()
	add_child(_debounce_timer)
	_debounce_timer.one_shot = true
	_debounce_timer.timeout.connect(_on_debounce_timeout)

	print("DEBUG [SyncBatchService | _ready]: Inicializado - batch_size=%d, max_retries=%d" % [_config.BATCH_SIZE, _config.MAX_RETRIES])

## Inicializa con las dependencias (llamar después de crear el nodo)
func setup(api_client: ApiClient, connection_detector: ConnectionDetector, xapi_service: XAPIService = null) -> void:
	_api_client = api_client
	_connection_detector = connection_detector
	
	# Migraciones locales (idempotente, corre una vez por versión de schema).
	var migration_result = _batch_repository.run_migrations()
	print("DEBUG [SyncBatchService | setup]: Migraciones ejecutadas - applied=%s" % str(migration_result.get("applied", false)))

	# Re-encolar batches 'failed' con retry_count >= threshold (one-shot deliberado).
	# Solo corre acá, NO en sync_all(): llamarlo en cada sync enmascararía fallos persistentes
	# reseteando retry_count antes de que llegue al threshold.
	var requeued = _batch_repository.requeue_failed(5)
	if requeued > 0:
		print("DEBUG [SyncBatchService | setup]: Re-encolados %d batches previously failed" % requeued)

	# Conectar señales del detector de conexión
	_connection_detector.connection_restored.connect(_on_connection_restored)
	_connection_detector.connection_lost.connect(_on_connection_lost)

	# Si ya estamos online, disparar sync inmediatamente.
	# El signal connection_restored pudo haberse emitido ANTES de conectar,
	# por lo que _on_connection_restored() no se habría ejecutado.
	if _connection_detector.is_online():
		print("DEBUG [SyncBatchService | setup]: Ya online, disparando sync_all()")
		sync_all()

	# Conectar señal de auto-batch ante nuevos statements
	pending_count_updated.connect(_on_pending_statements_changed)
	
	# Conectar raw_stats_ready signal para sync automático (Phase 2.1)
	if xapi_service != null:
		xapi_service.raw_stats_ready.connect(sync_raw_stats)
		print("DEBUG [SyncBatchService | setup]: Conectado raw_stats_ready -> sync_raw_stats")
	
	# Iniciar timer periódico de sync como fallback
	_periodic_timer.start()

	print("DEBUG [SyncBatchService | setup]: Dependencias conectadas - ApiClient y ConnectionDetector listos")

## Obtiene IDs de statements como Array[String]
func _get_statement_ids(statements: Array) -> Array[String]:
	var ids: Array[String] = []
	for stmt in statements:
		ids.append(stmt.get("id", ""))
	return ids

## Crea un nuevo batch con los statements pendientes
func create_batch() -> String:
	var statements := _xapi_repository.get_unbatched(_config.BATCH_SIZE)
	if statements.is_empty():
		print("DEBUG [SyncBatchService | create_batch]: No hay statements pendientes para batchear")
		return ""

	# Generar payload para el backend
	var payload := _build_payload(statements)

	# Guardar batch
	var batch_id := _batch_repository.create({
		"statements": _get_statement_ids(statements),
		"payload": payload
	})

	# Asignar batch_id a los statements
	var statement_ids: Array[String] = []
	for stmt in statements:
		statement_ids.append(stmt.get("id", ""))

	_xapi_repository.assign_to_batch(statement_ids, batch_id)

	print("DEBUG [SyncBatchService | create_batch]: Batch %s creado con %d statements" % [batch_id, statements.size()])
	return batch_id

## Procesa un batch específico (público, emite señales)
func process_batch(batch_id: String) -> bool:
	if _is_processing_batch:
		print("DEBUG [SyncBatchService | process_batch]: Procesando batch, ignorando batch %s" % batch_id)
		return false

	var result := await _process_single_batch(batch_id)
	
	if result:
		batch_sent.emit(batch_id, true)
	else:
		batch_sent.emit(batch_id, false)
	
	sync_completed.emit(1 if result else 0, 0 if result else 1)
	return result

## Procesa un batch individual sin emitir señales (usado por sync_all)
func _process_single_batch(batch_id: String) -> bool:
	var batch := _batch_repository.get_by_id(batch_id)
	if batch.is_empty():
		push_error("SyncBatchService: Batch no encontrado: %s" % batch_id)
		return false

	_is_processing_batch = true

	# Marcar como enviando
	_batch_repository.update_status(batch_id, PendingBatchRepository.STATUS_SENDING)

	# Parsear payload
	var payload = JSON.parse_string(batch.get("payload", "{}"))

	print("DEBUG [SyncBatchService | _process_single_batch]: Enviando batch %s al backend..." % batch_id)
	var result := await _send_to_backend(payload)

	_is_processing_batch = false

	if result:
		_batch_repository.update_status(batch_id, PendingBatchRepository.STATUS_COMPLETED)
		print("DEBUG [SyncBatchService | _process_single_batch]: Batch %s enviado EXITOSAMENTE" % batch_id)
	else:
		var error_info: Dictionary = {
			"error_message": "No se pudo enviar el batch al backend",
			"status_code": 0,
			"body": "",
			"url": "",
			"method": "",
			"timestamp": Time.get_datetime_string_from_system()
		}
		_handle_batch_failure(batch_id, error_info)

	return result

## Procesa todos los batches pendientes
func sync_all() -> void:
	if _is_syncing:
		print("DEBUG [SyncBatchService | sync_all]: Sync en proceso, ignorando llamada")
		return

	if not _connection_detector.is_online():
		print("DEBUG [SyncBatchService | sync_all]: Sin conexión, no se puede sincronizar")
		return

	# Guard defensivo: recupera batches 'sending' stale (proceso crasheado después de setup()).
	# NO llama requeue_failed() — eso es one-shot en setup() y resetearía retry_count=0
	# enmascarando fallos persistentes en cada sync.
	var recovered = _batch_repository.recover_sending(5)
	if recovered > 0:
		print("DEBUG [SyncBatchService | sync_all]: Recuperados %d sending batches stale" % recovered)

	_is_syncing = true
	sync_started.emit()

	var success_count := 0
	var failed_count := 0

	# Procesar batches pendientes
	var pending_batches := _batch_repository.get_pending()
	print("DEBUG [SyncBatchService | sync_all]: Procesando %d batches pendientes" % pending_batches.size())
	for batch in pending_batches:
		var batch_id = batch.get("id", "")
		if await _process_single_batch(batch_id):
			batch_sent.emit(batch_id, true)
			success_count += 1
		else:
			batch_sent.emit(batch_id, false)
			failed_count += 1

	# Procesar batches que se pueden reintentar
	var retryable_batches := _batch_repository.get_retryable(_config.MAX_RETRIES)
	print("DEBUG [SyncBatchService | sync_all]: Procesando %d batches reintentables" % retryable_batches.size())
	for batch in retryable_batches:
		var batch_id = batch.get("id", "")
		if await _process_single_batch(batch_id):
			batch_sent.emit(batch_id, true)
			success_count += 1
		else:
			batch_sent.emit(batch_id, false)
			failed_count += 1

	_is_syncing = false
	sync_completed.emit(success_count, failed_count)

	print("DEBUG [SyncBatchService | sync_all]: Sync completo - Exitosos: %d, Fallidos: %d" % [success_count, failed_count])

## Construye el payload para el backend
func _build_payload(statements: Array[Dictionary]) -> Dictionary:
	var events: Array = []
	
	for stmt in statements:
		var statement_id: String = stmt.get("id", "")
		events.append({
			"event_type": "xapi_statement",
			"client_event_id": statement_id,
			"payload": {
				"statement_id": statement_id,
				"verb_id": stmt.get("verb_id", ""),
				"verb_display": stmt.get("verb_display", ""),
				"object_type": stmt.get("object_type", ""),
				"object_id": stmt.get("object_id", ""),
				"object_name": stmt.get("object_name", ""),
				"actor_id": stmt.get("actor_id", ""),
				"result": {
					"score_raw": stmt.get("result_score_raw"),
					"score_scaled": stmt.get("result_score_scaled"),
					"success": stmt.get("result_success") == 1,
					"completion": stmt.get("result_completion") == 1,
					"duration": stmt.get("result_duration", "")
				},
				"timestamp": stmt.get("timestamp", "")
			}
		})
	
	return {"events": events}

## Envía el payload al backend
## OPTIMIZACIÓN: game_id e instance_id se cachean localmente.
## Se obtienen UNA vez del backend y se reutilizan en todos los syncs subsiguientes.
## Esto evita spam de GameInstance rows en la DB del backend.
func _send_to_backend(payload: Dictionary) -> bool:
	if _api_client == null:
		push_error("SyncBatchService: ApiClient no configurado")
		return false

	# Obtener statements del payload
	var statements: Array = payload.get("statements", [])
	var events: Array = payload.get("events", [])

	# Si no hay eventos, crear batch nuevo
	if events.is_empty():
		statements = _xapi_repository.get_unbatched(_config.BATCH_SIZE)
		if statements.is_empty():
			return true  # No hay nada que sincronizar
		events = _build_payload(statements).get("events", [])

	# PASO 1: Obtener o usar game_id cacheado
	var game_id: String = await _get_or_fetch_game_id()
	if game_id.is_empty():
		push_error("SyncBatchService: No se pudo obtener game_id")
		return false

	# PASO 2: Obtener o usar instance_id cacheado
	var instance_id: String = await _get_or_create_instance_id(game_id)
	if instance_id.is_empty():
		push_error("SyncBatchService: No se pudo obtener instance_id")
		return false

	print("DEBUG [SyncBatchService | _send_to_backend]: Usando instance_id=%s del cache/backend" % instance_id)

	# PASO 3: Iniciar sesión de sync (esto SÍ se hace cada vez)
	print("DEBUG [SyncBatchService | _send_to_backend]: Iniciando sesión de sync - eventos=%d" % events.size())
	var session_result := await _api_client.start_sync_session(instance_id)

	if not session_result.get("OK", false):
		push_error("SyncBatchService: Error al iniciar sesión: %s" % session_result.get("error", "unknown"))
		return false

	var session_id = session_result.get("session_id", "")
	print("DEBUG [SyncBatchService | _send_to_backend]: Sesión %s iniciada, enviando %d eventos..." % [session_id, events.size()])

	# PASO 4: Enviar cada evento con client_event_id para idempotencia
	for event in events:
		var event_result := await _api_client.register_sync_event(
			session_id,
			event.get("event_type", "xapi_statement"),
			event.get("payload", {}),
			event.get("client_event_id", "")
		)

		if not event_result.get("OK", false):
			push_error("SyncBatchService: Error al enviar evento: %s" % event_result.get("error", "unknown"))
			print("DEBUG [SyncBatchService | _send_to_backend]: Error enviando evento, abortando sesión")
			await _api_client.end_sync_session(session_id)
			return false

	# PASO 5: Cerrar sesión
	var end_result := await _api_client.end_sync_session(session_id)
	print("DEBUG [SyncBatchService | _send_to_backend]: Sesión %s cerrada - resultado=%s" % [session_id, str(end_result.get("OK", false))])
	return end_result.get("OK", false)


## Devuelve el game_id cacheado, o lo busca en el backend si no hay cache.
## Resultado: UUID string del juego, o "" si falla.
func _get_or_fetch_game_id() -> String:
	# Intentar usar el cache primero
	var cached := _session_repository.get_session()
	if cached != null and cached.game_id != "":
		print("DEBUG [SyncBatchService | _get_or_fetch_game_id]: Usando game_id del cache: %s" % cached.game_id)
		return cached.game_id

	# No hay cache, buscar en el backend
	var game_title: String = Env.GAME_TITLE
	print("DEBUG [SyncBatchService | _get_or_fetch_game_id]: No hay cache, buscando juego '%s' en backend..." % game_title)
	var game_result: Dictionary = await _api_client.get_game_by_name(game_title)

	if not game_result.get("OK", false):
		push_error("SyncBatchService: Error al obtener juego '%s': %s" % [game_title, game_result.get("error", "unknown")])
		return ""

	var game_id: String = game_result.get("game_id", "")
	if game_id.is_empty():
		push_error("SyncBatchService: No se encontró game_id para '%s'" % game_title)
		return ""

	# Si ya hay instance_id cacheado pero no game_id (caso raro), cachear el game_id
	if cached != null and cached.instance_id != "":
		_session_repository.save_session(game_id, cached.instance_id, cached.student_id)
	# Si no, no guardamos nada todavía - esperaremos a tener instance_id también

	print("DEBUG [SyncBatchService | _get_or_fetch_game_id]: game_id=%s obtenido del backend" % game_id)
	return game_id


## Devuelve el instance_id cacheado, o crea uno nuevo en el backend si no hay cache.
## Este método cachea TANTO game_id como instance_id después de la primera llamada.
## Resultado: UUID string de la instancia, o "" si falla.
func _get_or_create_instance_id(game_id: String) -> String:
	# Intentar usar el cache primero
	var cached := _session_repository.get_session()
	if cached != null and cached.instance_id != "" and cached.game_id == game_id:
		if cached.student_id != str(_GameConfig.user.get("id", "")):
			_session_repository.clear_session()
			print("DEBUG [SyncBatchService | _get_or_create_instance_id]: student_id cache mismatch, recreating instance")
		else:
			print("DEBUG [SyncBatchService | _get_or_create_instance_id]: Usando instance_id del cache: %s" % cached.instance_id)
			return cached.instance_id

	# No hay cache válido, crear nueva instancia en el backend
	print("DEBUG [SyncBatchService | _get_or_create_instance_id]: No hay cache válido, creando instancia para game_id=%s..." % game_id)
	var instance_result: Dictionary = await _api_client.create_game_instance(game_id)

	if not instance_result.get("OK", false):
		push_error("SyncBatchService: Error al crear instancia: %s" % instance_result.get("error", "unknown"))
		return ""

	var instance_id: String = instance_result.get("instance_id", "")
	if instance_id.is_empty():
		push_error("SyncBatchService: No se obtuvo instance_id del backend")
		return ""

	# Cachear TANTO game_id como instance_id
	var student_id := str(_GameConfig.user.get("id", ""))

	_session_repository.save_session(game_id, instance_id, student_id)
	print("DEBUG [SyncBatchService | _get_or_create_instance_id]: instance_id=%s creado y cacheado" % instance_id)
	return instance_id


## Limpia el cache de sesión. Útil cuando el usuario cierra sesión o reinicia el juego.
func clear_session_cache() -> void:
	_session_repository.clear_session()
	print("DEBUG [SyncBatchService | clear_session_cache]: Cache de sesión limpiado")

## Maneja el fallo de un batch
## @param error: Dictionary con la forma {error_message, status_code, body, url, method, timestamp}.
##               Si falta `error_message`, se usa `str(error)` como fallback.
func _handle_batch_failure(batch_id: String, error: Dictionary) -> void:
	_batch_repository.increment_retry(batch_id)
	var batch := _batch_repository.get_by_id(batch_id)
	var retry_count := int(batch.get("retry_count", 0))

	var error_message: String = str(error.get("error_message", str(error)))

	if retry_count >= _config.MAX_RETRIES:
		_batch_repository.update_status(batch_id, PendingBatchRepository.STATUS_FAILED, error_message)
		sync_failed.emit("Batch %s falló después de %d reintentos: %s" % [batch_id, retry_count, error_message])
		print("DEBUG [SyncBatchService | _handle_batch_failure]: Batch %s FALLÓ DEFINITIVAMENTE tras %d reintentos" % [batch_id, retry_count])
	else:
		_batch_repository.update_status(batch_id, PendingBatchRepository.STATUS_PENDING, error_message)
		print("DEBUG [SyncBatchService | _handle_batch_failure]: Batch %s falló, reintento %d/%d programado" % [batch_id, retry_count, _config.MAX_RETRIES])
		_schedule_retry(batch_id, retry_count)

## Programa un reintento con backoff exponencial
func _schedule_retry(batch_id: String, retry_count: int) -> void:
	var delay := _config.calculate_retry_delay(retry_count)
	print("DEBUG [SyncBatchService | _schedule_retry]: Batch %s se reintentará en %.1fs (backoff exponencial)" % [batch_id, delay])

	_retry_timer.start(delay)
	_pending_retry_batches.append(batch_id)

## Handler del timer de retry
func _on_retry_timeout() -> void:
	print("DEBUG [SyncBatchService | _on_retry_timeout]: Timer de retry disparado, procesando %d batches pendientes" % _pending_retry_batches.size())
	# Procesar batches uno por uno usando un timer para cada uno
	_retry_timer.stop()
	_process_next_retry_batch()

	# Procesa el siguiente batch de retry de forma asíncrona
func _process_next_retry_batch() -> void:
	if _pending_retry_batches.is_empty():
		print("DEBUG [SyncBatchService | _process_next_retry_batch]: No quedan batches por reintentar")
		return
	
	var batch_id = _pending_retry_batches.pop_front()
	if batch_id is String:
		await _process_single_batch(batch_id)
		# Programar siguiente batch después de un frame
		_retry_timer.start(0.1)

	## Callbacks de conexión
func _on_connection_restored() -> void:
	print("DEBUG [SyncBatchService | _on_connection_restored]: 🔄 Señal recibida - disparando sync_all() automático")
	sync_all()

func _on_connection_lost() -> void:
	print("DEBUG [SyncBatchService | _on_connection_lost]: ⚠️ Señal recibida - conexión perdida, sync en pausa")

## Handler para pending_count_updated: crea batch y dispara sync si hay conexión.
## Usa debounce de 300ms para evitar duplicados por emisiones rápidas consecutivas.
func _on_pending_statements_changed(count: int) -> void:
	if _debounce_guard:
		return
	_debounce_guard = true
	_debounce_timer.start(0.3)  # 300ms debounce

	# Crear batch con los statements pendientes (ya están en SQLite)
	var batch_id := create_batch()
	if batch_id.is_empty():
		_debounce_guard = false
		return

	# Si hay conexión y no estamos ya sincronizando, disparar sync
	if _connection_detector.is_online() and not _is_syncing:
		sync_all()

## Timer periódico: sync de respaldo cada 60s (solo si hay conexión).
func _on_periodic_timeout() -> void:
	if _connection_detector.is_online():
		sync_all()

## Libera el guard de debounce después de 300ms.
func _on_debounce_timeout() -> void:
	_debounce_guard = false

## Obtiene estadísticas de sync
func get_stats() -> Dictionary:
	return {
		"pending_batches": _batch_repository.get_stats(),
		"unbatched_statements": _xapi_repository.count_unbatched(),
		"is_syncing": _is_syncing,
		"is_connected": _connection_detector.is_online() if _connection_detector else false,
		"raw_stats": _raw_stats_repository.get_stats()
	}

## Sincroniza los raw stats pendientes al backend
## Usa una única sesión de sync para todos los registros
func sync_raw_stats() -> void:
	if not _connection_detector.is_online():
		print("DEBUG [SyncBatchService | sync_raw_stats]: Sin conexión, saltando sync de raw stats")
		return
	
	var pending: Array[Dictionary] = _raw_stats_repository.get_pending_all(50)
	if pending.is_empty():
		print("DEBUG [SyncBatchService | sync_raw_stats]: No hay raw stats pendientes")
		return
	
	print("DEBUG [SyncBatchService | sync_raw_stats]: Sincronizando %d raw stats..." % pending.size())
	
	# Marcar todos como sending antes de iniciar sync
	for record in pending:
		_raw_stats_repository.update_status(record.get("id", ""), "sending")
	
	# Usar sesión única para todos los raw stats
	var game_id: String = await _get_or_fetch_game_id()
	var instance_id: String = await _get_or_create_instance_id(game_id)
	var session_result: Dictionary = await _api_client.start_sync_session(instance_id)
	var session_id: String = session_result.get("session_id", "")
	
	if session_id.is_empty():
		push_error("SyncBatchService: No se pudo iniciar sesión para raw stats")
		for record in pending:
			_raw_stats_repository.mark_failed(record.get("id", ""), 5)
		return
	
	# Enviar cada raw stat como evento
	for record in pending:
		var stats_id: String = record.get("id", "")
		
		# Construir payload con game_id para resolver segment_level_id en el backend
		var payload: Dictionary = {
			"segment_id": record.get("segment_id", 0),
			"actor_id": record.get("actor_id", ""),
			"game_id": game_id,
			"attempt_count": record.get("attempt_count", 0),
			"error_count": record.get("error_count", 0),
			"hints_used_count": record.get("hints_used_count", 0),
			"errors_details": JSON.parse_string(record.get("errors_details", "{}")),
			"efficiency_rating": record.get("efficiency_rating", 0),
			"objectives_completed": record.get("objectives_completed", 0),
			"timestamp": record.get("created_at", "")
		}
		
		var event_result: Dictionary = await _api_client.register_sync_event(
			session_id,
			"raw_stats",
			payload,
			stats_id
		)
		
		if event_result.get("OK", false):
			_raw_stats_repository.mark_completed(stats_id)
			print("DEBUG [SyncBatchService | sync_raw_stats]: Raw stats %s sincronizado OK" % stats_id)
		else:
			_raw_stats_repository.mark_failed(stats_id, 5)
			print("DEBUG [SyncBatchService | sync_raw_stats]: Raw stats %s falló: %s" % [stats_id, event_result.get("error", "")])
	
	# Cerrar sesión
	await _api_client.end_sync_session(session_id)
	print("DEBUG [SyncBatchService | sync_raw_stats]: Sync completado - %d registros procesados" % pending.size())
