extends BaseLevelModifier
class_name LevelOneModifier

# Proportional modification constants
const DECREASE_MAJOR_BLOCKS_INC := 3
const DECREASE_MINOR_BLOCKS_INC := 1
const KEEP_BLOCKS_DELTA := 0
const INCREASE_MINOR_BLOCKS_DEC := 1
const INCREASE_MAJOR_BLOCKS_DEC := 3
const DECREASE_MAJOR_STUDENTS_REDUCE := 3
const DECREASE_MINOR_STUDENTS_REDUCE := 1
const INCREASE_MINOR_STUDENTS_ADD := 1
const INCREASE_MAJOR_STUDENTS_ADD := 2
const DECREASE_MAJOR_HINTS_ADD := 2
const DECREASE_MINOR_HINTS_ADD := 1
const INCREASE_MINOR_HINTS_REMOVE := 1
const INCREASE_MAJOR_HINTS_REMOVE := 2
const DECREASE_MAJOR_STATIONS_REFILL := 2
const DECREASE_MINOR_STATIONS_REFILL := 1
const INCREASE_MINOR_STATIONS_EMPTY := 1
const INCREASE_MAJOR_STATIONS_EMPTY := 1

# Time limit per difficulty (0 = no limit)
const DECREASE_MAJOR_TIME_LIMIT := 0
const DECREASE_MINOR_TIME_LIMIT := 0
const KEEP_TIME_LIMIT := 0
const INCREASE_MINOR_TIME_LIMIT := 90
const INCREASE_MAJOR_TIME_LIMIT := 60

var _decrease_major_hints := [
	"Recuerda revisar el pedido antes de ejecutarlo.",
	"Piensa en el orden de las acciones.",
	"Cada estudiante tiene un pedido específico."
]
var _decrease_minor_hint := "No necesitas usar todos los bloques."
var _cryptic_hints := [
	"Revisa la secuencia.",
	"Observa los pedidos.",
	"Los recursos son limitados."
]
var _extra_students := [
	{"nombre": "Luisa", "pedido": "pan"},
	{"nombre": "Carlos", "pedido": "cafe"},
]

# Environment visibility per difficulty
var _decrease_environment := {
	"bread_station": true,
	"drink_machine": true,
	"cash_register": true
}
var _increase_minor_environment := {
	"bread_station": true,
	"drink_machine": false,
	"cash_register": true
}
var _increase_major_environment := {
	"bread_station": true,
	"drink_machine": false,
	"cash_register": false
}

# Available blocks per difficulty
var _decrease_blocks := ["Start", "Execute", "End"]
var _increase_minor_blocks := ["Start", "Execute", "End", "Condition"]
var _increase_major_blocks := ["Start", "Execute", "End", "Condition", "Loop"]

# Distractor actions for harder difficulties (all valid in ActionFactory)
var _distractor_actions := [
	{"name": "Preparar bebida", "value": "prepare_drink"},
	{"name": "Servir bebida", "value": "serve_drink"},
	{"name": "Preparar pan", "value": "prepare_bread"},
	{"name": "Tomar pan", "value": "get_bread"},
	{"name": "Servir pan", "value": "serve_bread"},
	{"name": "Atender estudiante", "value": "attend_next_student"},
]


func _init() -> void:
	super()


func modify_level(state: String, difficulty: float) -> Dictionary:
	print("LevelOneModifier.modify_level called with state = ", state)
	var new_config: Dictionary = {}
	match state:
		"decrease_major":
			new_config = _apply_decrease_major()
		"decrease_minor":
			new_config = _apply_decrease_minor()
		"keep":
			new_config = _apply_keep()
		"increase_minor":
			new_config = _apply_increase_minor()
		"increase_major":
			new_config = _apply_increase_major()
		_:
			push_error("Invalid difficulty state: ", state)

	if not new_config.is_empty():
		var result = repo.update_configuration_segment(1, self.segment_id, new_config)
		print("DEBUG [Level One Modifier]: Result of Query: ", result)
		if result:
			print("DEBUG [Level One Modifier]: Guardando nueva configuracion")

	print("LevelOneModifier.modify_level finished")
	return new_config


func _apply_actions_with_distractors(cfg: Dictionary, max_distractors: int) -> void:
	# Add distractor actions to defined_actions for harder difficulties
	if max_distractors <= 0:
		return
	
	var existing := cfg.defined_actions
	var existing_values := []
	for action in existing:
		existing_values.append(action.value)
	
	var added := 0
	for distractor in _distractor_actions:
		if added >= max_distractors:
			break
		if distractor.value not in existing_values:
			existing.append(distractor)
			existing_values.append(distractor.value)
			added += 1


func _apply_hints(cfg: Dictionary, tier: String) -> void:
	# Set hints based on verbosity tier
	match tier:
		"verbose":
			cfg.feedback_messages.hints = _decrease_major_hints.duplicate()
		"normal":
			if cfg.feedback_messages.hints.is_empty():
				cfg.feedback_messages.hints = ["Piensa en el orden de las acciones."]
		"minimal":
			cfg.feedback_messages.hints = _cryptic_hints.duplicate()
		"none":
			cfg.feedback_messages.hints = []


func _apply_decrease_major() -> Dictionary:
	var cfg = self.original_config.duplicate(true)

	cfg.execution_rules.max_blocks += DECREASE_MAJOR_BLOCKS_INC
	print("DECREASE_MAJOR: Blocks +", DECREASE_MAJOR_BLOCKS_INC)

	var remove_count := mini(DECREASE_MAJOR_STUDENTS_REDUCE, maxi(0, cfg.initial_state.student_queue.size() - 1))
	for i in range(remove_count):
		cfg.initial_state.student_queue.pop_back()

	cfg.initial_state.inventory = ["pan", "cafe", "leche"]

	cfg.feedback_messages.hints = _decrease_major_hints.duplicate()

	cfg.initial_state.stations.bread_dispenser = ["pan"]
	cfg.initial_state.stations.drink_dispenser = ["cafe"]

	# Environment: all stations visible
	cfg.environment_data = _decrease_environment.duplicate()
	# Blocks: basic set
	cfg.available_blocks = _decrease_blocks.duplicate()
	# Time: no limit
	cfg.execution_rules.time_limit = DECREASE_MAJOR_TIME_LIMIT
	# Actions: no distractors
	_apply_actions_with_distractors(cfg, 0)

	return cfg


func _apply_decrease_minor() -> Dictionary:
	var cfg = self.original_config.duplicate(true)

	cfg.execution_rules.max_blocks += DECREASE_MINOR_BLOCKS_INC
	print("DECREASE_MINOR: Blocks +", DECREASE_MINOR_BLOCKS_INC)

	var remove_count := mini(DECREASE_MINOR_STUDENTS_REDUCE, maxi(0, cfg.initial_state.student_queue.size() - 1))
	for i in range(remove_count):
		cfg.initial_state.student_queue.pop_back()

	cfg.initial_state.inventory = ["pan"]

	cfg.feedback_messages.hints = [_decrease_minor_hint]

	cfg.initial_state.stations.bread_dispenser = ["pan"]

	cfg.environment_data = _decrease_environment.duplicate()
	cfg.available_blocks = _decrease_blocks.duplicate()
	cfg.execution_rules.time_limit = DECREASE_MINOR_TIME_LIMIT
	_apply_actions_with_distractors(cfg, 0)

	return cfg


func _apply_keep() -> Dictionary:
	var cfg = self.original_config.duplicate(true)

	cfg.execution_rules.max_blocks += KEEP_BLOCKS_DELTA

	cfg.initial_state.student_queue.shuffle()
	cfg.feedback_messages.hints.shuffle()

	cfg.version = str(cfg.version) + ".maintained"

	cfg.execution_rules.time_limit = KEEP_TIME_LIMIT
	cfg.available_blocks = _decrease_blocks.duplicate()
	cfg.environment_data = _decrease_environment.duplicate()
	_apply_actions_with_distractors(cfg, 0)

	return cfg


func _apply_increase_minor() -> Dictionary:
	var cfg = self.original_config.duplicate(true)

	cfg.execution_rules.max_blocks = max(
		6,
		cfg.execution_rules.max_blocks - INCREASE_MINOR_BLOCKS_DEC
	)
	print("INCREASE_MINOR: Blocks -", INCREASE_MINOR_BLOCKS_DEC)

	cfg.initial_state.student_queue.append(_extra_students[0])

	if cfg.initial_state.inventory.size() > 0:
		cfg.initial_state.inventory.pop_back()

	_apply_hints(cfg, "minimal")

	cfg.initial_state.stations.drink_dispenser = []

	cfg.environment_data = _increase_minor_environment.duplicate()
	cfg.available_blocks = _increase_minor_blocks.duplicate()
	cfg.execution_rules.time_limit = INCREASE_MINOR_TIME_LIMIT
	_apply_actions_with_distractors(cfg, 2)

	return cfg


func _apply_increase_major() -> Dictionary:
	var cfg = self.original_config.duplicate(true)

	cfg.execution_rules.max_blocks = max(
		6,
		cfg.execution_rules.max_blocks - INCREASE_MAJOR_BLOCKS_DEC
	)
	print("INCREASE_MAJOR: Blocks -", INCREASE_MAJOR_BLOCKS_DEC)

	for student in _extra_students:
		cfg.initial_state.student_queue.append(student)

	cfg.initial_state.inventory = []

	_apply_hints(cfg, "none")

	cfg.initial_state.stations.drink_dispenser = []

	cfg.environment_data = _increase_major_environment.duplicate()
	cfg.available_blocks = _increase_major_blocks.duplicate()
	cfg.execution_rules.time_limit = INCREASE_MAJOR_TIME_LIMIT
	_apply_actions_with_distractors(cfg, 5)

	return cfg
