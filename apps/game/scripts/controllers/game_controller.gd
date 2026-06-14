# Singleton Game Controller
class_name GameController
extends Node

var engine : ExecutionEngine
var agent : AdaptiveAgent
var feedback_controller : FeedbackController

var _current_level_id: int = 0
var _current_level_number: int = 0
var _current_actor_id: String = ""
var _is_retry_mode: bool = false
var _level_controller: LevelController
var _attempts_count: int = 0

static var _instance: GameController = null

func _ready() -> void:
	EventBus.level_loaded.connect(_on_level_loaded)

func _on_level_loaded(segment_id: int, level_number: int, actor_id: String) -> void:
	print("[GameController] Nivel cargado - segment_id=%d, level_number=%d, actor_id=%s" % [segment_id, level_number, actor_id])
	_current_level_number = level_number
	begin_segment(segment_id, actor_id)

static func create_level_controller(level) -> LevelController:
	var controller = LevelStrategy.create_level(level)
	get_instance()._level_controller = controller
	return controller

static func get_instance():
	if _instance == null:
		_instance = GameController.new()
	return _instance

func _init():
	if _instance != null:
		push_error("GameController singleton already exists. Use get_instance() to access the singleton.")
		return
	
	self.engine = ExecutionEngine.new()
	self.agent = AdaptiveAgent.new()
	self.feedback_controller = FeedbackController.new()

func execute_solution(blocks : Array[BaseBlock], context : BaseProblemContext) -> BaseProblemContext:
	return self.engine.execute(blocks, context)

## Placeholders rechazados por el guard de actor (REQ-P2-R3).
## Coincide con _XAPIService para que ambos límites fallen consistentemente.
const _INVALID_ACTOR_PLACEHOLDERS: Array[String] = [
	"player",
	"Leo",
	"estudiante1"
]

## Indica si el actor_id es vacío o es uno de los placeholders conocidos.
## Comparación case-sensitive según REQ-P2-R3.
func _is_invalid_actor(actor_id: String) -> bool:
	if actor_id.is_empty():
		return true
	return actor_id in _INVALID_ACTOR_PLACEHOLDERS

## Inicia tracking de segmento/nivel.
## @param segment_id: ID del segmento a trackear
## @param actor_id: ID del jugador (debe ser el UUID del usuario autenticado)
func begin_segment(segment_id: int, actor_id: String) -> void:
	if _is_invalid_actor(actor_id):
		push_error(
			"[GameController] begin_segment rechazado: actor_id inválido ('%s'). Se esperaba el UUID del usuario autenticado desde _GameConfig.user.id." % actor_id
		)
		return
	# Reset local state when beginning a new segment (singleton lifecycle)
	_attempts_count = 0
	print("[GameController] Segmento iniciado - level_id=%d, actor=%s" % [segment_id, actor_id])
	_XAPIService.start_segment_tracking(segment_id, actor_id)
	# Crear statement xAPI 'attempted' para tracking de sincronización
	_XAPIService.track_level_started(str(segment_id), "Level %d" % segment_id, actor_id, _current_level_number, segment_id)
	_current_level_id = segment_id
	_current_actor_id = actor_id

## Inicia un nuevo intento dentro del segmento actual.
func begin_attempt() -> void:
	_attempts_count += 1
	_XAPIService.increment_attempt()

## Registra un intento completado en el tracking.
## @param blocks_executed: Bloques utilizados
## @param success: Si el intento fue exitoso
## @param execution_time: Tiempo de ejecución en segundos
func record_attempt(blocks_executed: Array[String], success: bool, execution_time: float) -> void:
	_XAPIService.end_attempt(blocks_executed, success, execution_time)

## Completa el nivel: registra intento, finaliza tracking y notifica al LevelController.
## @param result: Dictionary con keys "blocks", "success", "time"
func complete_level(result: Dictionary) -> void:
	record_attempt(result.blocks, result.success, result.time)
	var analytics = _XAPIService.end_segment_tracking(result.success)
	var enriched = _enrich_level_data(analytics)
	
	# Crear xAPI statement para sincronización con backend
	# Captura el evento consolidado de nivel completado con score, errors, duration
	var summary = analytics.get("summary", {})
	var score := float(summary.get("score", 0.0))
	var time_sec := float(summary.get("time", 0.0))
	_XAPIService.track_level_completed(
		str(_current_level_id),
		"Level %d" % _current_level_id,
		_current_actor_id,
		score,
		score,
		result.success,
		"PT%fS" % time_sec,
		_current_level_number,
		_current_level_id
	)
	
	if _level_controller:
		print("[GameController] Enviando analytics al AdaptiveAgent - score=%.2f, errors=%d" % [enriched.get("score", 0.0), enriched.get("errors", 0)])
		_level_controller.finish_level(enriched)
	else:
		push_error("GameController: No hay _level_controller asignado")

## Enriquece datos analíticos con contexto del nivel (level_id, actor_id)
## y datos de raw_stats (hints_used, efficiency_rating, etc.).
## @param analytics: Diccionario de analytics desde end_segment_tracking
## @return Dictionary enriquecido con level_id, actor_id y campos extendidos
func _enrich_level_data(analytics: Dictionary) -> Dictionary:
	var enriched := analytics.duplicate()
	enriched["level_id"] = _current_level_id
	enriched["actor_id"] = _current_actor_id
	if analytics.has("summary"):
		var s = analytics["summary"]
		enriched["total_time"] = s.get("time", 0.0)
		# Flatten score and errors to top level for AdaptiveAgent compatibility
		enriched["score"] = s.get("score", 0.0)
		enriched["errors"] = s.get("errors", 0)
		enriched["time"] = s.get("time", 0.0)

	# Extract raw_stats enrichment data (safe access — may not exist)
	var raw_stats: Dictionary = analytics.get("raw_stats", {})
	enriched["hints_used"] = raw_stats.get("hints_used_count", 0)
	enriched["efficiency_rating"] = raw_stats.get("efficiency_rating", 0.0)
	enriched["objectives_completed"] = raw_stats.get("objectives_completed", 0)

	# Error details — raw_stats uses "errors_details" internally
	var error_details_key := "errors_details" if raw_stats.has("errors_details") else "error_details"
	enriched["error_details"] = raw_stats.get(error_details_key, {})

	# Custom events — prefer raw_stats if present, fall back to top-level analytics
	if raw_stats.has("custom_events"):
		enriched["custom_events"] = raw_stats["custom_events"]
	elif analytics.has("custom_events"):
		enriched["custom_events"] = analytics["custom_events"]
	else:
		enriched["custom_events"] = []

	# Blocks count from last attempt
	var attempts: Array = analytics.get("attempts", [])
	enriched["blocks_count"] = 0
	if not attempts.is_empty():
		var last_attempt: Dictionary = attempts[-1]
		enriched["blocks_count"] = last_attempt.get("blocks_count", 0)

	return enriched

## Agrega un evento de tracking personalizado.
## @param event_name: Nombre del evento
## @param event_data: Datos adicionales del evento
func add_tracking_event(event_name: String, event_data: Dictionary = {}) -> void:
	_XAPIService.track_event(event_name, event_data)

## Resetea el tracking del nivel actual.
## Limpia contadores locales y delega a XAPIService.reset_tracking().
func reset_level_tracking() -> void:
	_XAPIService.reset_tracking()
	_attempts_count = 0
	_is_retry_mode = false
