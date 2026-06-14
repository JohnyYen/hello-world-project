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

var _decrease_major_hints := [
	"Recuerda revisar el pedido antes de ejecutarlo.",
	"Piensa en el orden de las acciones."
]
var _decrease_minor_hint := "No necesitas usar todos los bloques."
var _extra_students := [
	{"nombre": "Luisa", "pedido": "pan"},
	{"nombre": "Carlos", "pedido": "cafe"},
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


func _apply_decrease_major() -> Dictionary:
	var cfg = self.original_config

	cfg.execution_rules.max_blocks += DECREASE_MAJOR_BLOCKS_INC
	print("DECREASE_MAJOR: Blocks +", DECREASE_MAJOR_BLOCKS_INC)

	var remove_count := mini(DECREASE_MAJOR_STUDENTS_REDUCE, maxi(0, cfg.initial_state.student_queue.size() - 1))
	for i in range(remove_count):
		cfg.initial_state.student_queue.pop_back()

	cfg.initial_state.inventory = ["pan", "cafe", "leche"]

	for hint in _decrease_major_hints:
		cfg.feedback_messages.hints.append(hint)

	cfg.initial_state.stations.bread_dispenser = ["pan"]
	cfg.initial_state.stations.drink_dispenser = ["cafe"]

	return cfg


func _apply_decrease_minor() -> Dictionary:
	var cfg = self.original_config

	cfg.execution_rules.max_blocks += DECREASE_MINOR_BLOCKS_INC
	print("DECREASE_MINOR: Blocks +", DECREASE_MINOR_BLOCKS_INC)

	var remove_count := mini(DECREASE_MINOR_STUDENTS_REDUCE, maxi(0, cfg.initial_state.student_queue.size() - 1))
	for i in range(remove_count):
		cfg.initial_state.student_queue.pop_back()

	cfg.initial_state.inventory = ["pan"]

	cfg.feedback_messages.hints.append(_decrease_minor_hint)

	cfg.initial_state.stations.bread_dispenser = ["pan"]

	return cfg


func _apply_keep() -> Dictionary:
	var cfg = self.original_config

	cfg.execution_rules.max_blocks += KEEP_BLOCKS_DELTA

	cfg.initial_state.student_queue.shuffle()

	cfg.feedback_messages.hints.shuffle()

	cfg.version = str(cfg.version) + ".maintained"

	return cfg


func _apply_increase_minor() -> Dictionary:
	var cfg = self.original_config

	cfg.execution_rules.max_blocks = max(
		6,
		cfg.execution_rules.max_blocks - INCREASE_MINOR_BLOCKS_DEC
	)
	print("INCREASE_MINOR: Blocks -", INCREASE_MINOR_BLOCKS_DEC)

	cfg.initial_state.student_queue.append(_extra_students[0])

	if cfg.initial_state.inventory.size() > 0:
		cfg.initial_state.inventory.pop_back()

	if cfg.feedback_messages.hints.size() > 0:
		cfg.feedback_messages.hints.pop_back()

	cfg.initial_state.stations.drink_dispenser = []

	return cfg


func _apply_increase_major() -> Dictionary:
	var cfg = self.original_config

	cfg.execution_rules.max_blocks = max(
		6,
		cfg.execution_rules.max_blocks - INCREASE_MAJOR_BLOCKS_DEC
	)
	print("INCREASE_MAJOR: Blocks -", INCREASE_MAJOR_BLOCKS_DEC)

	for student in _extra_students:
		cfg.initial_state.student_queue.append(student)

	cfg.initial_state.inventory = []

	var remove_count := mini(cfg.feedback_messages.hints.size(), INCREASE_MAJOR_HINTS_REMOVE)
	for i in range(remove_count):
		cfg.feedback_messages.hints.pop_back()

	cfg.initial_state.stations.drink_dispenser = []

	return cfg
