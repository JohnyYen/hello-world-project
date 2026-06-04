# XAPIService.gd
# Servicio integrado que combina sync y xAPI para el juego
# Punto de entrada principal para tracking de learning events
class_name XAPIService
extends Node

## Señales
signal segment_analytics_ready(analytics_dict: Dictionary)

## Servicios internos
var _builder: XAPIBuilderService
var _connection_detector: ConnectionDetector
var _batch_service: SyncBatchService

## API Client compartida
var _api_client: ApiClient

## Referencia al SyncService existente (para compatibilidad)
var _sync_service: SyncService

## Analytics tracking para segmento actual
var _current_segment_id := 0
var _current_actor_id := ""
var _segment_start_time := 0.0
var _blocks_executed := []
var _attempts_count := 0
var _is_tracking := false
var _attempts_history: Array[Dictionary] = []
var _custom_events: Array[Dictionary] = []
var _is_new_attempt := false
var _is_retry_mode := false

func _init() -> void:
	_builder = XAPIBuilderService.new()
	_connection_detector = ConnectionDetector.new()
	_batch_service = SyncBatchService.new()
	
	# Initialize analytics tracking variables
	_current_segment_id = 0
	_current_actor_id = ""
	_segment_start_time = 0.0
	_blocks_executed = []
	_attempts_count = 0
	_is_tracking = false
	_attempts_history = []
	_custom_events = []
	_is_new_attempt = false
	_is_retry_mode = false
	
func _ready() -> void:
	_api_client = ApiClient.new()
	add_child(_api_client)
	
	add_child(_batch_service)
	_batch_service.setup(_api_client, _connection_detector)

## Configura el SyncService existente para mantener compatibilidad
func set_sync_service(sync_service: SyncService) -> void:
	_sync_service = sync_service

## === Métodos de tracking xAPI ===

## Registra que un nivel comenzó
func track_level_started(level_id: String, level_name: String, actor_id: String) -> Dictionary:
	var statement := _builder.on_level_started(level_id, level_name, actor_id)
	_notify_pending_update()
	return statement

## Registra que un nivel fue completado
func track_level_completed(
	level_id: String,
	level_name: String,
	actor_id: String,
	score_raw: float,
	score_scaled: float,
	success: bool,
	duration: String
) -> Dictionary:
	var statement := _builder.on_level_completed(
		level_id, level_name, actor_id, score_raw, score_scaled, success, duration
	)
	_notify_pending_update()
	return statement

## Registra que una pregunta fue respondida
func track_assessment_answered(
	assessment_id: String,
	assessment_name: String,
	actor_id: String,
	correct: bool,
	response_time: String = ""
) -> Dictionary:
	var statement := _builder.on_assessment_answered(
		assessment_id, assessment_name, actor_id, correct, response_time
	)
	_notify_pending_update()
	return statement

## Registra que el juego inició
func track_game_started(game_id: String, game_name: String, actor_id: String) -> Dictionary:
	var statement := _builder.on_game_started(game_id, game_name, actor_id)
	_notify_pending_update()
	return statement

## Registra que el juego terminó
func track_game_ended(game_id: String, game_name: String, actor_id: String) -> Dictionary:
	var statement := _builder.on_game_ended(game_id, game_name, actor_id)
	_notify_pending_update()
	return statement

## Registra un evento custom
func track_custom(
	verb_key: String,
	object_type: String,
	object_id: String,
	object_name: String,
	actor_id: String,
	result: Dictionary = {},
	context: Dictionary = {}
) -> Dictionary:
	var statement := _builder.build(
		verb_key, object_type, object_id, object_name, actor_id, result, context
	)
	_notify_pending_update()
	return statement

## === Tracking de analytics para segmento ===

## Inicia tracking de un segmento/nivel.
## @param segment_id: ID del segmento a trackear
## @param actor_id: ID del jugador
func start_segment_tracking(segment_id: int, actor_id: String) -> void:
	_current_segment_id = segment_id
	_current_actor_id = actor_id
	_segment_start_time = Time.get_ticks_msec()
	_blocks_executed = []
	_attempts_count = 0
	_attempts_history = []
	_custom_events = []
	_is_new_attempt = false
	_is_retry_mode = false
	_is_tracking = true

## Registra un bloque ejecutado en el intento actual.
## @param block_name: Nombre del bloque ejecutado
func block_executed(block_name: String) -> void:
	if _is_tracking:
		if _is_new_attempt:
			_blocks_executed.clear()
			_is_new_attempt = false
		_blocks_executed.append(block_name)

## Incrementa el contador de intentos del segmento actual.
func increment_attempt() -> void:
	if _is_tracking:
		_attempts_count += 1

## Finaliza un intento registrando los datos de ejecución.
## @param blocks_executed: Bloques utilizados en el intento
## @param success: Si el intento fue exitoso
## @param execution_time: Tiempo de ejecución en segundos
func end_attempt(blocks_executed: Array[String], success: bool, execution_time: float) -> void:
	if not _is_tracking:
		return
	var attempt_number := _attempts_history.size() + 1
	var attempt_data := {
		"attempt_number": attempt_number,
		"blocks": blocks_executed,
		"blocks_count": blocks_executed.size(),
		"success": success,
		"time": execution_time,
		"timestamp": Time.get_datetime_string_from_system()
	}
	_attempts_history.append(attempt_data)
	_is_new_attempt = true

## Registra un evento personalizado dentro del segmento actual.
## @param event_name: Nombre del evento
## @param event_data: Datos adicionales del evento
func track_event(event_name: String, event_data: Dictionary = {}) -> void:
	if not _is_tracking:
		return
	var event := {
		"event_name": event_name,
		"event_data": event_data,
		"timestamp": Time.get_datetime_string_from_system()
	}
	_custom_events.append(event)

## Resetea el tracking del segmento actual.
## En modo retry (set_retry_mode), preserva el historial de intentos previos.
func reset_tracking() -> void:
	_is_tracking = true
	_blocks_executed.clear()
	_attempts_count = 0
	_is_new_attempt = false
	if not _is_retry_mode:
		_attempts_history.clear()
		_custom_events.clear()

## Activa/desactiva el modo retry.
## Cuando está activo, reset_tracking preserva el historial de intentos.
## @param enabled: true para activar modo retry
func set_retry_mode(enabled: bool) -> void:
	_is_retry_mode = enabled

## Finaliza el tracking del segmento actual y emite segment_analytics_ready.
## @param success: Si el jugador completó el segmento exitosamente
## @return Dictionary con analytics del segmento (segment_id, summary, attempts, custom_events)
func end_segment_tracking(success: bool) -> Dictionary:
	if not _is_tracking:
		return {}
	var elapsed_msec = Time.get_ticks_msec() - _segment_start_time
	var elapsed_sec = elapsed_msec / 1000.0

	var errors := _attempts_count
	if success and _attempts_count > 0:
		errors = _attempts_count - 1

	var score := 1.0
	if errors > 0:
		score = max(0.1, 1.0 - (float(errors) * 0.25))
	if not success:
		score = 0.0

	var analytics = {
		"segment_id": _current_segment_id,
		"actor_id": _current_actor_id,
		"timestamp": Time.get_datetime_string_from_system(),
		"summary": {
			"time": elapsed_sec,
			"errors": errors,
			"score": score,
			"success": success,
			"attempts": _attempts_count,
			"blocks_count": _blocks_executed.size()
		},
		"attempts": _attempts_history.duplicate(),
		"custom_events": _custom_events.duplicate(),
		"retry_count": _attempts_count
	}
	_is_tracking = false
	print("[XAPIService] Segmento completado - segment_id=%d, score=%.2f, errors=%d, tiempo=%.2fs" % [
		_current_segment_id, score, errors, elapsed_sec
	])
	emit_signal("segment_analytics_ready", analytics)
	return analytics

## === Métodos de sincronización ===

## Fuerza la sincronización ahora
func sync_now() -> void:
	_batch_service.sync_all()

## Crea un batch con los statements pendientes
func create_batch() -> String:
	return _batch_service.create_batch()

## Procesa un batch específico (envía al backend)
func process_batch(batch_id: String) -> bool:
	return await _batch_service.process_batch(batch_id)

## Obtiene los statements pendientes de sincronizar
func get_pending_statements(limit: int = 50) -> Array[Dictionary]:
	return _builder.get_pending_statements(limit)

## Obtiene estadísticas del sistema xAPI
func get_stats() -> Dictionary:
	return _batch_service.get_stats()

## Verifica si hay conexión
func is_online() -> bool:
	return _connection_detector.is_online()

## Fuerza verificación de conexión
func check_connection() -> void:
	_connection_detector.check_now()

## === Métodos de compatibilidad con SyncService ===

## Agrega un evento legacy (compatibilidad hacia atrás)
func add_legacy_event(event_type: String, payload: Dictionary) -> void:
	if _sync_service:
		_sync_service.add_event(event_type, payload)

## Sincroniza eventos legacy
func sync_legacy_events(instance_id: String) -> void:
	if _sync_service:
		_sync_service.sync_all_pending(instance_id)

## Notifica actualización de statements pendientes
func _notify_pending_update() -> void:
	var count := _builder.get_pending_statements().size()
	_batch_service.pending_count_updated.emit(count)
