class_name LevelConfiguration

# =======================
# Campos según plantilla
# =======================
var segment_id : int

var initial_state : Dictionary = {}
var environment : Dictionary = {}
var goals : Array = []
var rules : Dictionary = {}
var access_blocks : Array = []
var defined_actions : Array = []
var expected_outputs : Array = []
var ui_config : Dictionary = {}
var feedback_messages : Dictionary = {}
var learning_objective : String = ""

var json_data: Dictionary = {}

func _init(segment_id : int):
	self.segment_id = segment_id


func load_from_dict(data : Dictionary) -> void:
	# ================
	# Mapeo de campos
	# ================

	initial_state = data.get("initial_state", {})
	print("DEBUG [LevelConfig]: initial_state => ", initial_state)

	environment = data.get("environment_data", {})
	print("DEBUG [LevelConfig]: environment => ", environment)

	expected_outputs = data.get("expected_outputs", [])
	print("DEBUG [LevelConfig]: expected_outputs => ", expected_outputs)

	goals = data.get("validation_criteria", [])
	print("DEBUG [LevelConfig]: validation_criteria => ", goals)

	rules = data.get("execution_rules", {})
	print("DEBUG [LevelConfig]: rules => ", rules)

	access_blocks = data.get("available_blocks", [])
	print("DEBUG [LevelConfig]: available_blocks => ", access_blocks)

	defined_actions = data.get("defined_actions", [])
	print("DEBUG [LevelConfig]: defined_actions => ", defined_actions)

	feedback_messages = data.get("feedback_messages", {})
	print("DEBUG [LevelConfig]: feedback_messages => ", feedback_messages)

	ui_config = data.get("ui_config", {})
	print("DEBUG [LevelConfig]: ui_config => ", ui_config)

	learning_objective = data.get("learning_objective", "")
	print("DEBUG [LevelConfig]: learning_objective => ", learning_objective)


func load_data() -> LevelConfiguration:
	push_error("METHOD_NOT_IMPLEMENTED (override expected in subclass)")
	return null
