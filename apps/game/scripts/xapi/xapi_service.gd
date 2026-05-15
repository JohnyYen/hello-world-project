# XAPIService.gd
# Servicio integrado que combina sync y xAPI para el juego
# Punto de entrada principal para tracking de learning events
class_name XAPIService
extends Node

## Servicios internos
var _builder: XAPIBuilderService
var _connection_detector: ConnectionDetector
var _batch_service: SyncBatchService

## API Client compartida
var _api_client: ApiClient

## Referencia al SyncService existente (para compatibilidad)
var _sync_service: SyncService

func _init() -> void:
	_builder = XAPIBuilderService.new()
	_connection_detector = ConnectionDetector.new()
	_batch_service = SyncBatchService.new()

func _ready() -> void:
	# Crear API client
	_api_client = ApiClient.new()
	add_child(_api_client)
	
	# Configurar batch service
	_batch_service.setup(_api_client, _connection_detector)
	
	print("DEBUG [XAPIService]: Inicializado")

## Configura el SyncService existente para mantener compatibilidad
func set_sync_service(sync_service: SyncService) -> void:
	_sync_service = sync_service
	print("DEBUG [XAPIService]: SyncService conectado")

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
