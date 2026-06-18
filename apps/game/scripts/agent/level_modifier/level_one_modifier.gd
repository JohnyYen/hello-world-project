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

# Default templates por dificultad (usan {segment_label} para mostrar bread-only/drink-only/mixed)
const DEFAULT_TEMPLATES := {
	"decrease_major": {
		"title": "Sirve {segment_label} a {student_count} estudiante{student_plural}",
		"description": "Prepara y sirve {segment_label} a {student_count} estudiante{student_plural}",
		"learning_objective": "Atender a {student_count} cliente{student_plural}"
	},
	"decrease_minor": {
		"title": "Sirve {segment_label} a {student_count} estudiante{student_plural}",
		"description": "Prepara {segment_label} y sirve a {student_count} estudiante{student_plural}",
		"learning_objective": "Atender a {student_count} cliente{student_plural}"
	},
	"keep": {
		"title": "Nivel - {segment_label}",
		"description": "Prepara y sirve {segment_label} a los estudiantes",
		"learning_objective": "Practica: {segment_label}"
	},
	"increase_minor": {
		"title": "Sirve {segment_label} a {student_count} estudiantes",
		"description": "Atiende a {student_count} estudiantes con pedidos de {segment_label}",
		"learning_objective": "Atender multiples pedidos de {segment_label}"
	},
	"increase_major": {
		"title": "Sirve {segment_label} a {student_count} estudiantes",
		"description": "Organiza las acciones para servir {segment_label} a {student_count} estudiantes",
		"learning_objective": "Gestionar multiples pedidos de {segment_label}"
	}
}

# Default templates per segment type (used as fallback when segment has no explicit templates)
const SEGMENT_TYPE_DEFAULT_TEMPLATES := {
	"bread-only": {
		"keep": {
			"title": "Sirve {bread_item} a {student_count} estudiante{student_plural}",
			"description": "Prepara y sirve {bread_item} a {student_count} estudiante{student_plural}",
			"learning_objective": "Atender pedidos de {bread_item}"
		}
	},
	"drink-only": {
		"keep": {
			"title": "Sirve {drink_item} a {student_count} estudiante{student_plural}",
			"description": "Prepara y sirve {drink_item} a {student_count} estudiante{student_plural}",
			"learning_objective": "Atender pedidos de {drink_item}"
		}
	},
	"mixed": {
		"keep": {
			"title": "Atiende a {student_count} estudiante{student_plural}",
			"description": "Atiende pedidos variados de {student_count} estudiante{student_plural}",
			"learning_objective": "Gestionar pedidos mixtos"
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
		self.modified_config = new_config

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

	_enforce_consistency(cfg, "increase_major")
	return cfg


func _build_template_context(cfg: Dictionary) -> Dictionary:
	var queue = cfg.get("initial_state", {}).get("student_queue", [])
	var count = queue.size()
	var ctx: Dictionary = {
		"student_count": count,
		"student_plural": "s" if count != 1 else "",
	}

	if count > 0:
		var names = queue.map(func(s): return s.get("nombre", ""))
		ctx["student_names"] = ", ".join(names)
	else:
		ctx["student_names"] = ""

	var has_bread = false
	var has_drink = false
	var bread_item = "pan"
	var drink_item = "cafe"
	var actions: Array = []
	var stations: Array = []

	var stations_dict = cfg.get("initial_state", {}).get("stations", {})
	if stations_dict.has("bread_dispenser"):
		stations.append("panaderia")
		has_bread = true
	if stations_dict.has("drink_dispenser"):
		stations.append("barra de bebidas")
		has_drink = true

	for student in queue:
		var pedido = student.get("pedido", "")
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

	var segment_type := cfg.get("segment_type", "mixed") as String
	var segment_labels := {
		"bread-only": "pan",
		"drink-only": "bebidas",
		"mixed": "pedidos mixtos"
	}
	ctx["segment_label"] = segment_labels.get(segment_type, "pedidos mixtos")

	return ctx


func _generate_title(cfg: Dictionary, tier: String) -> void:
	var templates_dict := cfg.get("templates", {}) as Dictionary
	var tier_templates := templates_dict.get(tier, {}) as Dictionary
	var template := tier_templates.get("title", "") as String

	if template.is_empty():
		var segment_type := cfg.get("segment_type", "mixed") as String
		var type_defaults := SEGMENT_TYPE_DEFAULT_TEMPLATES.get(segment_type, SEGMENT_TYPE_DEFAULT_TEMPLATES["mixed"]) as Dictionary

		template = type_defaults.get(tier, {}).get("title", "") as String

		if template.is_empty():
			template = type_defaults.get("keep", {}).get("title", "") as String

			if template.is_empty():
				var tier_default := DEFAULT_TEMPLATES.get(tier, DEFAULT_TEMPLATES["keep"]) as Dictionary
				template = tier_default.get("title", "") as String

	var ctx: Dictionary = _build_template_context(cfg)
	cfg.title = BaseLevelModifier.resolve_template(template, ctx)


func _generate_description(cfg: Dictionary, tier: String) -> void:
	var templates_dict := cfg.get("templates", {}) as Dictionary
	var tier_templates := templates_dict.get(tier, {}) as Dictionary
	var template := tier_templates.get("description", "") as String

	if template.is_empty():
		var segment_type := cfg.get("segment_type", "mixed") as String
		var type_defaults := SEGMENT_TYPE_DEFAULT_TEMPLATES.get(segment_type, SEGMENT_TYPE_DEFAULT_TEMPLATES["mixed"]) as Dictionary

		template = type_defaults.get(tier, {}).get("description", "") as String

		if template.is_empty():
			template = type_defaults.get("keep", {}).get("description", "") as String

			if template.is_empty():
				var tier_default := DEFAULT_TEMPLATES.get(tier, DEFAULT_TEMPLATES["keep"]) as Dictionary
				template = tier_default.get("description", "") as String

	var ctx: Dictionary = _build_template_context(cfg)
	cfg.description = BaseLevelModifier.resolve_template(template, ctx)


func _generate_learning_objective(cfg: Dictionary, tier: String) -> void:
	var templates_dict := cfg.get("templates", {}) as Dictionary
	var tier_templates := templates_dict.get(tier, {}) as Dictionary
	var template := tier_templates.get("learning_objective", "") as String

	if template.is_empty():
		var segment_type := cfg.get("segment_type", "mixed") as String
		var type_defaults := SEGMENT_TYPE_DEFAULT_TEMPLATES.get(segment_type, SEGMENT_TYPE_DEFAULT_TEMPLATES["mixed"]) as Dictionary

		template = type_defaults.get(tier, {}).get("learning_objective", "") as String

		if template.is_empty():
			template = type_defaults.get("keep", {}).get("learning_objective", "") as String

			if template.is_empty():
				var tier_default := DEFAULT_TEMPLATES.get(tier, DEFAULT_TEMPLATES["keep"]) as Dictionary
				template = tier_default.get("learning_objective", "") as String

	var ctx: Dictionary = _build_template_context(cfg)
	cfg.learning_objective = BaseLevelModifier.resolve_template(template, ctx)


func _sync_environment_with_segment(cfg: Dictionary) -> void:
	var segment_type = cfg.get("segment_type", "mixed")
	if typeof(cfg.get("environment_data")) == TYPE_DICTIONARY:
		cfg.environment_data.bread_station = (segment_type in ["bread-only", "mixed"])
		cfg.environment_data.drink_machine = (segment_type in ["drink-only", "mixed"])


func _filter_distractors_by_type(cfg: Dictionary) -> void:
	var segment_type = cfg.get("segment_type", "mixed")
	var allowlist = SEGMENT_TYPE_DISTRACTOR_ALLOWLIST.get(segment_type, SEGMENT_TYPE_DISTRACTOR_ALLOWLIST["mixed"])

	var filtered: Array = []
	for action in cfg.defined_actions:
		if action.value in allowlist:
			filtered.append(action)
	cfg.defined_actions = filtered


func _generate_validation_criteria(cfg: Dictionary) -> void:
	var criteria: Array = []
	
	# Convert existing string-format criteria to structured
	var existing = cfg.get("validation_criteria", [])
	for entry in existing:
		if typeof(entry) == TYPE_STRING:
			var parts = entry.split(" served", true)
			if parts.size() > 0 and not parts[0].is_empty():
				var name = parts[0].strip_edges()
				criteria.append({
					"condition": "orders_served",
					"target": [{"nombre": name, "pedido": ""}],
					"type": "all"
				})
				continue
		criteria.append(entry)
	
	# Generate new criteria from expected_outputs
	for expected in cfg.expected_outputs:
		if expected.has("orders_served"):
			var names = expected.orders_served.map(func(o): return o.nombre)
			var names_str = ", ".join(names)
			var desc = "Todos los estudiantes deben ser atendidos"
			if names.size() == 1:
				desc = "%s debe ser atendido" % names[0]
			criteria.append({
				"condition": "%s served" % names_str,
				"description": desc,
				"type": expected.get("type", "all"),
				"target": expected.orders_served.duplicate()
			})
		elif expected.has("inventory_contains"):
			var items = expected.inventory_contains
			criteria.append({
				"condition": "inventory contains %s" % ", ".join(items),
				"description": "El inventario debe contener los items requeridos",
				"type": expected.get("type", "all"),
				"target": items.duplicate()
			})
	
	cfg.validation_criteria = criteria


func _update_inventory_expected_outputs(cfg: Dictionary) -> void:
	for expected in cfg.expected_outputs:
		if expected.has("inventory_contains"):
			var items = _derive_expected_inventory(cfg)
			if not items.is_empty():
				expected.inventory_contains = _process_expected_items(cfg, items)


func _derive_expected_inventory(cfg: Dictionary) -> Array:
	var items: Array = []
	var stations = cfg.get("initial_state", {}).get("stations", {})
	for station_name in stations:
		var station_items = stations[station_name]
		if station_items is Array:
			for item in station_items:
				if item not in items:
					items.append(item)
	return items


# Si el segmento tiene required_actions que procesan items (prepare_bread,
# prepare_drink), los items de estaciones se transforman a su forma procesada.
# Ej: "pan" → "pan_preparado", "cafe" → "cafe_preparado"
func _process_expected_items(cfg: Dictionary, raw_items: Array) -> Array:
	var required = cfg.get("required_actions", [])
	if "prepare_bread" in required or "prepare_drink" in required:
		var processed: Array = []
		for item in raw_items:
			processed.append(item + "_preparado")
		return processed
	return raw_items


func _ensure_expected_outputs(cfg: Dictionary) -> void:
	var segment_type := cfg.get("segment_type", "mixed") as String
	var queue = cfg.get("initial_state", {}).get("student_queue", [])
	
	if segment_type == "bread-only" and queue.is_empty():
		var stations = cfg.get("initial_state", {}).get("stations", {})
		var items: Array = []
		for station_name in stations:
			var station_items = stations[station_name]
			if station_items is Array:
				for item in station_items:
					if item not in items:
						items.append(item)
		if not items.is_empty():
			cfg.expected_outputs = [{"inventory_contains": items}]
	else:
		var orders: Array = []
		for student in queue:
			orders.append({
				"nombre": student.get("nombre", "Estudiante"),
				"pedido": student.get("pedido", "pan")
			})
		cfg.expected_outputs = [{"orders_served": orders}]


func _sync_stations_with_segment(cfg: Dictionary) -> void:
	var segment_type = cfg.get("segment_type", "mixed")
	var stations = cfg.get("initial_state", {}).get("stations", {})
	
	match segment_type:
		"bread-only":
			if stations.has("drink_dispenser"):
				stations.drink_dispenser = []
			if stations.has("bread_dispenser") and stations.bread_dispenser.is_empty():
				stations.bread_dispenser = ["pan"]
		"drink-only":
			if stations.has("bread_dispenser"):
				stations.bread_dispenser = []
			if stations.has("drink_dispenser") and stations.drink_dispenser.is_empty():
				stations.drink_dispenser = ["cafe"]
		"mixed":
			if stations.has("bread_dispenser") and stations.bread_dispenser.is_empty():
				stations.bread_dispenser = ["pan"]
			if stations.has("drink_dispenser") and stations.drink_dispenser.is_empty():
				stations.drink_dispenser = ["cafe"]


# Garantiza que attend_next_student esté disponible si hay estudiantes en la cola
func ensure_attend_action_exists(cfg: Dictionary) -> void:
	var queue = cfg.get("initial_state", {}).get("student_queue", [])
	if queue.is_empty():
		return

	var actions = cfg.get("defined_actions", []) as Array
	for action in actions:
		if action.get("value", "") == "attend_next_student":
			return  # ya existe, no hace falta agregar

	# Si llegamos acá: hay estudiantes y NO existe attend_next_student → agregarlo
	actions.push_front({"name": "Atender estudiante", "value": "attend_next_student"})
	cfg.defined_actions = actions
	print("[LevelOneModifier] Attend action auto-agregada porque hay %d estudiantes en la cola" % queue.size())


func _ensure_required_actions_present(cfg: Dictionary) -> void:
	var required = cfg.get("required_actions", [])
	if required.is_empty():
		return
	
	var actions = cfg.get("defined_actions", []) as Array
	var existing_values := []
	for action in actions:
		existing_values.append(action.get("value", ""))
	
	var name_map := {
		"get_bread": "Tomar pan",
		"prepare_bread": "Preparar pan",
		"serve_bread": "Servir pan",
		"prepare_drink": "Preparar bebida",
		"serve_drink": "Servir bebida",
		"attend_next_student": "Atender estudiante"
	}
	
	for required_value in required:
		if required_value not in existing_values:
			actions.append({
				"name": name_map.get(required_value, required_value),
				"value": required_value
			})
			existing_values.append(required_value)
			print("[LevelOneModifier] Added required action: %s" % required_value)
	
	cfg.defined_actions = actions


func _ensure_student_orders_match_type(cfg: Dictionary) -> void:
	var segment_type = cfg.get("segment_type", "mixed") as String
	var queue = cfg.get("initial_state", {}).get("student_queue", [])
	if queue.is_empty():
		return
	
	match segment_type:
		"bread-only":
			var valid_orders := ["pan", "pan_con_queso", "tostada"]
			var filtered = queue.filter(func(s): return s.get("pedido", "") in valid_orders)
			if filtered.size() < queue.size():
				print("[LevelOneModifier] Filtrados %d estudiantes con pedidos no compatibles (bread-only)" % [queue.size() - filtered.size()])
				cfg.initial_state.student_queue = filtered
		"drink-only":
			var valid_orders := ["cafe", "te", "chocolate"]
			var filtered = queue.filter(func(s): return s.get("pedido", "") in valid_orders)
			if filtered.size() < queue.size():
				print("[LevelOneModifier] Filtrados %d estudiantes con pedidos no compatibles (drink-only)" % [queue.size() - filtered.size()])
				cfg.initial_state.student_queue = filtered
		"mixed":
			# Todos los pedidos son válidos
			pass


func _enforce_difficulty_bounds(cfg: Dictionary) -> void:
	var bounds = cfg.get("difficulty_bounds", {})
	if bounds.is_empty():
		return
	
	var min_students = bounds.get("min_students", 1)
	var max_students = bounds.get("max_students", 10)
	var queue = cfg.get("initial_state", {}).get("student_queue", [])
	
	while queue.size() < min_students:
		queue.append({"nombre": "Estudiante", "pedido": "pan"})
	
	while queue.size() > max_students:
		queue.pop_back()
	
	var min_blocks = bounds.get("min_blocks", 3)
	var max_blocks = bounds.get("max_blocks", 10)
	cfg.execution_rules.max_blocks = clampi(cfg.execution_rules.max_blocks, min_blocks, max_blocks)


func _enforce_consistency(cfg: Dictionary, tier: String) -> void:
	_ensure_student_orders_match_type(cfg)
	_ensure_expected_outputs(cfg)
	ensure_attend_action_exists(cfg)
	_ensure_required_actions_present(cfg)
	_generate_title(cfg, tier)
	_generate_description(cfg, tier)
	_generate_learning_objective(cfg, tier)
	_sync_environment_with_segment(cfg)
	_filter_distractors_by_type(cfg)
	_generate_validation_criteria(cfg)
	_sync_stations_with_segment(cfg)
	_update_inventory_expected_outputs(cfg)
	_enforce_difficulty_bounds(cfg)
