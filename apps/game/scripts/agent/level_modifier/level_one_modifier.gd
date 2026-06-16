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

# Default per-segment_type templates (used when seed data has no templates)
const DEFAULT_TEMPLATES := {
	"bread-only": {
		"decrease_major": {
			"title": "Sirve pan a {student_count} estudiante{student_plural}",
			"description": "Prepara y sirve pan a {student_count} estudiante{student_plural}",
			"learning_objective": "Atender a {student_count} cliente{student_plural}"
		},
		"decrease_minor": {
			"title": "Sirve pan a {student_count} estudiante{student_plural}",
			"description": "Toma, prepara y sirve pan a {student_count} estudiante{student_plural}",
			"learning_objective": "Atender a {student_count} cliente{student_plural}"
		},
		"keep": {
			"title": "Nivel - Sirve pan",
			"description": "Prepara y sirve pan a los estudiantes",
			"learning_objective": "Practicar secuencia de servicio"
		},
		"increase_minor": {
			"title": "Sirve pan a {student_count} estudiantes",
			"description": "Atiende a {student_count} estudiantes con pedidos de pan",
			"learning_objective": "Atender multiples clientes con pan"
		},
		"increase_major": {
			"title": "Sirve pan a {student_count} estudiantes",
			"description": "Organiza las acciones para servir a {student_count} estudiantes",
			"learning_objective": "Gestionar multiples pedidos de pan"
		}
	},
	"drink-only": {
		"decrease_major": {
			"title": "Sirve bebida a {student_count} estudiante{student_plural}",
			"description": "Prepara y sirve bebida a {student_count} estudiante{student_plural}",
			"learning_objective": "Atender a {student_count} cliente{student_plural} con bebidas"
		},
		"decrease_minor": {
			"title": "Sirve bebida a {student_count} estudiante{student_plural}",
			"description": "Prepara y sirve una bebida a {student_count} estudiante{student_plural}",
			"learning_objective": "Servir bebidas a {student_count} cliente{student_plural}"
		},
		"keep": {
			"title": "Nivel - Sirve bebida",
			"description": "Prepara y sirve una bebida a los estudiantes",
			"learning_objective": "Practicar servicio de bebidas"
		},
		"increase_minor": {
			"title": "Sirve bebidas a {student_count} estudiantes",
			"description": "Prepara y sirve bebidas a {student_count} estudiantes",
			"learning_objective": "Atender multiples pedidos de bebida"
		},
		"increase_major": {
			"title": "Sirve bebidas a {student_count} estudiantes",
			"description": "Organiza las acciones para servir bebidas a {student_count} estudiantes",
			"learning_objective": "Gestionar multiples pedidos de bebida"
		}
	},
	"mixed": {
		"decrease_major": {
			"title": "Atiende a {student_count} estudiante{student_plural}",
			"description": "Los estudiantes tienen distintos pedidos. Atiende a {student_count} estudiante{student_plural}",
			"learning_objective": "Atender pedidos mixtos de {student_count} cliente{student_plural}"
		},
		"decrease_minor": {
			"title": "Atiende a {student_count} estudiante{student_plural}",
			"description": "Cada estudiante tiene un pedido especifico. Sirve a {student_count} estudiante{student_plural}",
			"learning_objective": "Atender {student_count} cliente{student_plural} correctamente"
		},
		"keep": {
			"title": "Nivel - Atencion multiple",
			"description": "Atiende a los estudiantes con sus pedidos",
			"learning_objective": "Practicar atencion multiple"
		},
		"increase_minor": {
			"title": "Atiende a {student_count} estudiantes",
			"description": "{student_count} estudiantes esperan. Identifica cada pedido y sirve correctamente",
			"learning_objective": "Gestionar multiples pedidos variados"
		},
		"increase_major": {
			"title": "Atiende a {student_count} estudiantes",
			"description": "{student_count} estudiantes con pedidos variados. Usa las acciones correctas para cada uno",
			"learning_objective": "Resolver secuencia compleja de {student_count} pasos"
		}
	}
}

# Distractor allowlist per segment type
const SEGMENT_TYPE_DISTRACTOR_ALLOWLIST := {
	"bread-only": [
		"prepare_bread",
		"serve_bread",
		"get_bread",
		"attend_next_student"
	],
	"drink-only": [
		"prepare_drink",
		"serve_drink",
		"attend_next_student"
	],
	"mixed": [
		"prepare_drink",
		"serve_drink",
		"prepare_bread",
		"get_bread",
		"serve_bread",
		"attend_next_student"
	]
}

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

# Note: available_blocks variation is reserved for when Condition/Loop blocks
# are implemented in the game. Currently only Start/Execute/End exist.

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
	
	var existing = cfg.defined_actions
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


func _apply_expected_outputs_for_students(cfg: Dictionary, students: Array) -> void:
	# Add students to expected_outputs so validation expects them
	for expected in cfg.expected_outputs:
		if expected.has("orders_served"):
			for student in students:
				expected.orders_served.append({
					"nombre": student.nombre,
					"pedido": student.pedido
				})


func _remove_students_from_expected_outputs(cfg: Dictionary, count: int) -> void:
	# Remove students from expected_outputs when they're removed from queue
	for expected in cfg.expected_outputs:
		if expected.has("orders_served"):
			var removed := 0
			while removed < count and expected.orders_served.size() > 0:
				expected.orders_served.pop_back()
				removed += 1


func _apply_decrease_major() -> Dictionary:
	var cfg = self.original_config.duplicate(true)

	cfg.execution_rules.max_blocks += DECREASE_MAJOR_BLOCKS_INC
	print("DECREASE_MAJOR: Blocks +", DECREASE_MAJOR_BLOCKS_INC)

	var remove_count := mini(DECREASE_MAJOR_STUDENTS_REDUCE, maxi(0, cfg.initial_state.student_queue.size() - 1))
	_remove_students_from_expected_outputs(cfg, remove_count)
	for i in range(remove_count):
		cfg.initial_state.student_queue.pop_back()

	cfg.initial_state.inventory = ["pan", "cafe", "leche"]

	cfg.feedback_messages.hints = _decrease_major_hints.duplicate()

	cfg.initial_state.stations.bread_dispenser = ["pan"]
	cfg.initial_state.stations.drink_dispenser = ["cafe"]

	# Environment: all stations visible
	cfg.environment_data = _decrease_environment.duplicate()
	# Time: no limit
	cfg.execution_rules.time_limit = DECREASE_MAJOR_TIME_LIMIT
	# Actions: no distractors
	_apply_actions_with_distractors(cfg, 0)

	_enforce_consistency(cfg, "decrease_major")
	return cfg


func _apply_decrease_minor() -> Dictionary:
	var cfg = self.original_config.duplicate(true)

	cfg.execution_rules.max_blocks += DECREASE_MINOR_BLOCKS_INC
	print("DECREASE_MINOR: Blocks +", DECREASE_MINOR_BLOCKS_INC)

	var remove_count := mini(DECREASE_MINOR_STUDENTS_REDUCE, maxi(0, cfg.initial_state.student_queue.size() - 1))
	_remove_students_from_expected_outputs(cfg, remove_count)
	for i in range(remove_count):
		cfg.initial_state.student_queue.pop_back()

	cfg.initial_state.inventory = ["pan"]

	cfg.feedback_messages.hints = [_decrease_minor_hint]

	cfg.initial_state.stations.bread_dispenser = ["pan"]

	cfg.environment_data = _decrease_environment.duplicate()
	cfg.execution_rules.time_limit = DECREASE_MINOR_TIME_LIMIT
	_apply_actions_with_distractors(cfg, 0)

	_enforce_consistency(cfg, "decrease_minor")
	return cfg


func _apply_keep() -> Dictionary:
	var cfg = self.original_config.duplicate(true)

	cfg.execution_rules.max_blocks += KEEP_BLOCKS_DELTA

	cfg.initial_state.student_queue.shuffle()
	cfg.feedback_messages.hints.shuffle()

	cfg.version = str(cfg.version) + ".maintained"

	cfg.execution_rules.time_limit = KEEP_TIME_LIMIT
	cfg.environment_data = _decrease_environment.duplicate()
	_apply_actions_with_distractors(cfg, 0)

	_enforce_consistency(cfg, "keep")
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
	cfg.execution_rules.time_limit = INCREASE_MINOR_TIME_LIMIT
	_apply_actions_with_distractors(cfg, 2)
	_apply_expected_outputs_for_students(cfg, [_extra_students[0]])

	_enforce_consistency(cfg, "increase_minor")
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
	cfg.execution_rules.time_limit = INCREASE_MAJOR_TIME_LIMIT
	_apply_actions_with_distractors(cfg, 5)
	_apply_expected_outputs_for_students(cfg, _extra_students)

	_enforce_consistency(cfg, "increase_major")
	return cfg


func _build_template_context(cfg: Dictionary) -> Dictionary:
	var queue := cfg.get("initial_state", {}).get("student_queue", [])
	var count := queue.size()
	var ctx := {
		"student_count": count,
		"student_plural": "s" if count != 1 else "",
	}

	if count > 0:
		var names := queue.map(func(s): return s.get("nombre", ""))
		ctx["student_names"] = ", ".join(names)
	else:
		ctx["student_names"] = ""

	var has_bread := false
	var has_drink := false
	var bread_item := "pan"
	var drink_item := "cafe"
	var actions: Array = []
	var stations: Array = []

	var stations_dict := cfg.get("initial_state", {}).get("stations", {})
	if stations_dict.has("bread_dispenser"):
		stations.append("panaderia")
		has_bread = true
	if stations_dict.has("drink_dispenser"):
		stations.append("barra de bebidas")
		has_drink = true

	for student in queue:
		var pedido := student.get("pedido", "")
		if pedido in ["cafe", "te", "chocolate"]:
			has_drink = true
			drink_item = pedido
		elif pedido in ["pan", "pan_con_queso", "tostada"]:
			has_bread = true

	if has_bread:
		actions.append("tomar/preparar pan")
	if has_drink:
		actions.append("preparar/servir bebida")

	ctx["action_list"] = ", ".join(actions) if not actions.is_empty() else "acciones disponibles"
	ctx["station_list"] = ", ".join(stations) if not stations.is_empty() else "estaciones"
	ctx["bread_item"] = bread_item
	ctx["drink_item"] = drink_item

	return ctx


func _generate_title(cfg: Dictionary, tier: String) -> void:
	var segment_type := cfg.get("segment_type", "mixed")
	var templates_dict := cfg.get("templates", {})
	var tier_templates := templates_dict.get(tier, {})
	var template := tier_templates.get("title", "")

	if template.is_empty():
		var defaults := DEFAULT_TEMPLATES.get(segment_type, DEFAULT_TEMPLATES["mixed"])
		var tier_default := defaults.get(tier, defaults["keep"])
		template = tier_default.get("title", "")

	var ctx := _build_template_context(cfg)
	cfg.title = BaseLevelModifier.resolve_template(template, ctx)


func _generate_description(cfg: Dictionary, tier: String) -> void:
	var segment_type := cfg.get("segment_type", "mixed")
	var templates_dict := cfg.get("templates", {})
	var tier_templates := templates_dict.get(tier, {})
	var template := tier_templates.get("description", "")

	if template.is_empty():
		var defaults := DEFAULT_TEMPLATES.get(segment_type, DEFAULT_TEMPLATES["mixed"])
		var tier_default := defaults.get(tier, defaults["keep"])
		template = tier_default.get("description", "")

	var ctx := _build_template_context(cfg)
	cfg.description = BaseLevelModifier.resolve_template(template, ctx)


func _generate_learning_objective(cfg: Dictionary, tier: String) -> void:
	var segment_type := cfg.get("segment_type", "mixed")
	var templates_dict := cfg.get("templates", {})
	var tier_templates := templates_dict.get(tier, {})
	var template := tier_templates.get("learning_objective", "")

	if template.is_empty():
		var defaults := DEFAULT_TEMPLATES.get(segment_type, DEFAULT_TEMPLATES["mixed"])
		var tier_default := defaults.get(tier, defaults["keep"])
		template = tier_default.get("learning_objective", "")

	var ctx := _build_template_context(cfg)
	cfg.learning_objective = BaseLevelModifier.resolve_template(template, ctx)


func _sync_environment_with_segment(cfg: Dictionary) -> void:
	var segment_type := cfg.get("segment_type", "mixed")
	if typeof(cfg.get("environment_data")) == TYPE_DICTIONARY:
		cfg.environment_data.bread_station = (segment_type in ["bread-only", "mixed"])
		cfg.environment_data.drink_machine = (segment_type in ["drink-only", "mixed"])


func _filter_distractors_by_type(cfg: Dictionary) -> void:
	var segment_type := cfg.get("segment_type", "mixed")
	var allowlist := SEGMENT_TYPE_DISTRACTOR_ALLOWLIST.get(segment_type, SEGMENT_TYPE_DISTRACTOR_ALLOWLIST["mixed"])

	var filtered: Array = []
	for action in cfg.defined_actions:
		if action.value in allowlist:
			filtered.append(action)
	cfg.defined_actions = filtered


func _generate_validation_criteria(cfg: Dictionary) -> void:
	var criteria: Array = []
	for expected in cfg.expected_outputs:
		if expected.has("orders_served"):
			var names := expected.orders_served.map(func(o): return o.nombre)
			var names_str := ", ".join(names)
			var desc := "Todos los estudiantes deben ser atendidos"
			if names.size() == 1:
				desc = "%s debe ser atendido" % names[0]
			criteria.append({
				"condition": "%s served" % names_str,
				"description": desc
			})
		elif expected.has("inventory_contains"):
			var items := expected.inventory_contains
			criteria.append({
				"condition": "inventory contains %s" % ", ".join(items),
				"description": "El inventario debe contener los items requeridos"
			})
	cfg.validation_criteria = criteria


func _update_inventory_expected_outputs(cfg: Dictionary) -> void:
	for expected in cfg.expected_outputs:
		if expected.has("inventory_contains"):
			var items := _derive_expected_inventory(cfg)
			if not items.is_empty():
				expected.inventory_contains = items


func _derive_expected_inventory(cfg: Dictionary) -> Array:
	var items: Array = []
	var stations := cfg.get("initial_state", {}).get("stations", {})
	for station_name in stations:
		var station_items = stations[station_name]
		if station_items is Array:
			for item in station_items:
				if item not in items:
					items.append(item)
	return items


func _enforce_consistency(cfg: Dictionary, tier: String) -> void:
	_generate_title(cfg, tier)
	_generate_description(cfg, tier)
	_generate_learning_objective(cfg, tier)
	_sync_environment_with_segment(cfg)
	_filter_distractors_by_type(cfg)
	_generate_validation_criteria(cfg)
	_update_inventory_expected_outputs(cfg)
