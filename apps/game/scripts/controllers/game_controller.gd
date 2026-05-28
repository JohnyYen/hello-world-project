# Singleton Game Controller
class_name GameController
extends Node

var engine : ExecutionEngine
var agent : AdaptiveAgent
var feedback_controller : FeedbackController

var _current_level_id: int = 0
var _current_actor_id: String = ""
var _is_retry_mode: bool = false
var _level_controller: LevelController
var _attempts_count: int = 0

static var _instance: GameController = null

func _ready() -> void:
	EventBus.level_loaded.connect(_on_level_loaded)

func _on_level_loaded(segment_id: int, actor_id: String) -> void:
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

## Inicia tracking de segmento/nivel.
## @param segment_id: ID del segmento a trackear
## @param actor_id: ID del jugador
func begin_segment(segment_id: int, actor_id: String) -> void:
	_XAPIService.start_segment_tracking(segment_id, actor_id)
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
	var analytics := _XAPIService.end_segment_tracking(result.success)
	var enriched := _enrich_level_data(analytics)
	if _level_controller:
		_level_controller.finish_level(enriched)
	else:
		push_error("GameController: No hay _level_controller asignado")

## Enriquece datos analíticos con contexto del nivel (level_id, actor_id).
## @param analytics: Diccionario de analytics desde end_segment_tracking
## @return Dictionary enriquecido con level_id y actor_id
func _enrich_level_data(analytics: Dictionary) -> Dictionary:
	var enriched := analytics.duplicate()
	enriched["level_id"] = _current_level_id
	enriched["actor_id"] = _current_actor_id
	if analytics.has("summary"):
		enriched["total_time"] = analytics["summary"].get("time", 0.0)
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
