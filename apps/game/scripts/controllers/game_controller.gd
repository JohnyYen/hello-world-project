# Singleton Game Controller
class_name GameController
extends Node

var engine : ExecutionEngine
var agent : AdaptiveAgent
var feedback_controller : FeedbackController

static var _instance: GameController = null

func _ready() -> void:
	pass

static func create_level_controller(level) -> LevelController:
	return LevelStrategy.create_level(level)

static func get_instance():
	if _instance == null:
		_instance = GameController.new()
	return _instance

func _init():
	if _instance != null:
		push_error("GameController singleton already exists. Use get_instance() to access the singleton.")
		return
	
	self.engine = ExecutionEngine.new()
	print("DEBUG [Game Controller]: Crear un nuevo agente")
	self.agent = AdaptiveAgent.new()
	self.feedback_controller = FeedbackController.new()

func execute_solution(blocks : Array[BaseBlock], context : BaseProblemContext) -> BaseProblemContext:
	return self.engine.execute(blocks, context)
# static func run_code(blocks, context):
	# self.engine.execute(blocks, context)
	# pass
