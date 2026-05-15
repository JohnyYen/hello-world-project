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

## Estado
var _is_syncing: bool = false
var _retry_timer: Timer
var _pending_retry_batches: Array = []

func _init() -> void:
	_xapi_repository = XAPIStatementRepository.new()
	_batch_repository = PendingBatchRepository.new()
	_config = XAPIConfig.new()

func _ready() -> void:
	# Crear timer para reintentos
	_retry_timer = Timer.new()
	add_child(_retry_timer)
	_retry_timer.timeout.connect(_on_retry_timeout)
	
	print("DEBUG [SyncBatchService]: Inicializado")

## Inicializa con las dependencias (llamar después de crear el nodo)
func setup(api_client: ApiClient, connection_detector: ConnectionDetector) -> void:
	_api_client = api_client
	_connection_detector = connection_detector
	
	# Conectar señales del detector de conexión
	_connection_detector.connection_restored.connect(_on_connection_restored)
	_connection_detector.connection_lost.connect(_on_connection_lost)
	
	print("DEBUG [SyncBatchService]: Setup completo")

## Crea un nuevo batch con los statements pendientes
func create_batch() -> String:
	var statements := _xapi_repository.get_unbatched(_config.BATCH_SIZE)
	if statements.is_empty():
		print("DEBUG [SyncBatchService]: No hay statements pendientes")
		return ""
	
	# Generar payload para el backend
	var payload := _build_payload(statements)
	
	# Guardar batch
	var batch_id := _batch_repository.create({
		"statements": statements.map(func(s): return s.get("id", "")),
		"payload": payload
	})
	
	# Asignar batch_id a los statements
	var statement_ids: Array[String] = []
	for stmt in statements:
		statement_ids.append(stmt.get("id", ""))
	
	_xapi_repository.assign_to_batch(statement_ids, batch_id)
	
	print("DEBUG [SyncBatchService]: Batch %s creado con %d statements" % [batch_id, statements.size()])
	return batch_id

## Procesa un batch específico
func process_batch(batch_id: String) -> bool:
	if _is_syncing:
		print("DEBUG [SyncBatchService]: Sync en proceso, ignorando")
		return false
	
	var batch := _batch_repository.get_by_id(batch_id)
	if batch.is_empty():
		push_error("SyncBatchService: Batch no encontrado: %s" % batch_id)
		return false
	
	_is_syncing = true
	sync_started.emit()
	
	# Marcar como enviando
	_batch_repository.update_status(batch_id, PendingBatchRepository.STATUS_SENDING)
	
	# Parsear payload
	var payload := JSON.parse_string(batch.get("payload", "{}"))
	
	var result := await _send_to_backend(payload)
	
	_is_syncing = false
	
	if result:
		_batch_repository.update_status(batch_id, PendingBatchRepository.STATUS_COMPLETED)
		batch_sent.emit(batch_id, true)
		print("DEBUG [SyncBatchService]: Batch %s enviado exitosamente" % batch_id)
	else:
		_handle_batch_failure(batch_id, "Error al enviar al backend")
		batch_sent.emit(batch_id, false)
	
	sync_completed.emit(1 if result else 0, 0 if result else 1)
	return result

## Procesa todos los batches pendientes
func sync_all() -> void:
	if _is_syncing:
		print("DEBUG [SyncBatchService]: Sync en proceso, ignorando")
		return
	
	if not _connection_detector.is_online():
		print("DEBUG [SyncBatchService]: Sin conexión, no se puede sincronizar")
		return
	
	_is_syncing = true
	sync_started.emit()
	
	var success_count := 0
	var failed_count := 0
	
	# Procesar batches pendientes
	var pending_batches := _batch_repository.get_pending()
	for batch in pending_batches:
		var batch_id := batch.get("id", "")
		if process_batch(batch_id):
			success_count += 1
		else:
			failed_count += 1
	
	# Procesar batches que se pueden reintentar
	var retryable_batches := _batch_repository.get_retryable(_config.MAX_RETRIES)
	for batch in retryable_batches:
		var batch_id := batch.get("id", "")
		if process_batch(batch_id):
			success_count += 1
		else:
			failed_count += 1
	
	_is_syncing = false
	sync_completed.emit(success_count, failed_count)
	
	print("DEBUG [SyncBatchService]: Sync completo - Exitosos: %d, Fallidos: %d" % [success_count, failed_count])

## Construye el payload para el backend
func _build_payload(statements: Array[Dictionary]) -> Dictionary:
	var events: Array = []
	
	for stmt in statements:
		events.append({
			"event_type": "xapi_statement",
			"payload": {
				"statement_id": stmt.get("id", ""),
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
	
	# Iniciar sesión de sync
	var instance_id := Env.get_instance_id() if "get_instance_id" in Env else "default"
	var session_result := await _api_client.start_sync_session(instance_id)
	
	if not session_result.get("OK", false):
		push_error("SyncBatchService: Error al iniciar sesión: %s" % session_result.get("error", "unknown"))
		return false
	
	var session_id := session_result.get("session_id", "")
	
	# Enviar cada evento
	for event in events:
		var event_result := await _api_client.register_sync_event(
			session_id,
			event.get("event_type", "xapi_statement"),
			event.get("payload", {})
		)
		
		if not event_result.get("OK", false):
			push_error("SyncBatchService: Error al enviar evento: %s" % event_result.get("error", "unknown"))
			await _api_client.end_sync_session(session_id)
			return false
	
	# Cerrar sesión
	var end_result := await _api_client.end_sync_session(session_id)
	return end_result.get("OK", false)

## Maneja el fallo de un batch
func _handle_batch_failure(batch_id: String, error: String) -> void:
	_batch_repository.increment_retry(batch_id)
	var batch := _batch_repository.get_by_id(batch_id)
	var retry_count := int(batch.get("retry_count", 0))
	
	if retry_count >= _config.MAX_RETRIES:
		_batch_repository.update_status(batch_id, PendingBatchRepository.STATUS_FAILED, error)
		sync_failed.emit("Batch %s falló después de %d reintentos: %s" % [batch_id, retry_count, error])
	else:
		_batch_repository.update_status(batch_id, PendingBatchRepository.STATUS_PENDING, error)
		_schedule_retry(batch_id, retry_count)

## Programa un reintento con backoff exponencial
func _schedule_retry(batch_id: String, retry_count: int) -> void:
	var delay := _config.calculate_retry_delay(retry_count)
	print("DEBUG [SyncBatchService]: Reintentando batch %s en %f segundos" % [batch_id, delay])
	
	_retry_timer.start(delay)
	_pending_retry_batches.append(batch_id)

## Handler del timer de retry
func _on_retry_timeout() -> void:
	for batch_id in _pending_retry_batches:
		process_batch(batch_id)
	_pending_retry_batches.clear()

## Callbacks de conexión
func _on_connection_restored() -> void:
	print("DEBUG [SyncBatchService]: Conexión restaurada, iniciando sync...")
	sync_all()

func _on_connection_lost() -> void:
	print("DEBUG [SyncBatchService]: Conexión perdida, pausando sync")

## Obtiene estadísticas de sync
func get_stats() -> Dictionary:
	return {
		"pending_batches": _batch_repository.get_stats(),
		"unbatched_statements": _xapi_repository.count_unbatched(),
		"is_syncing": _is_syncing,
		"is_connected": _connection_detector.is_online() if _connection_detector else false
	}