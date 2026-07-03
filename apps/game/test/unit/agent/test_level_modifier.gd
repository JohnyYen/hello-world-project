# test_level_modifier.gd
# Tests for LevelOneModifier proportional modifications
extends GutTest

var LevelOneModifier = load("res://scripts/agent/level_modifier/level_one_modifier.gd")
var BaseLevelModifier = load("res://scripts/agent/level_modifier/base_level_modifier.gd")
var modifier
var base_config: Dictionary


func before_each() -> void:
	modifier = LevelOneModifier.new()
	base_config = {
		"execution_rules": {"max_blocks": 10, "time_limit": 0},
		"initial_state": {
			"student_queue": [
				{"nombre": "Ana", "pedido": "cafe"},
				{"nombre": "Luis", "pedido": "te"},
				{"nombre": "Maria", "pedido": "pan"}
			],
			"inventory": [],
			"stations": {
				"bread_dispenser": [],
				"drink_dispenser": []
			}
		},
		"feedback_messages": {"hints": ["Pista inicial"]},
		"version": "1.0",
		"defined_actions": [
			{"name": "Tomar pan", "value": "get_bread"},
			{"name": "Servir pan", "value": "serve_bread"}
		],
		"environment_data": {
			"bread_station": true,
			"drink_machine": true,
			"cash_register": true
		},
		"available_blocks": ["Start", "Execute", "End"],
		"expected_outputs": [
			{"orders_served": [
				{"nombre": "Ana", "pedido": "cafe"},
				{"nombre": "Luis", "pedido": "te"},
				{"nombre": "Maria", "pedido": "pan"}
			]}
		]
	}
	modifier.set_level_segment({
		"segment_id": 0,
		"configuration": base_config.duplicate(true)
	})


# =============================================================================
# resolve_template (static)
# =============================================================================

func test_resolve_template_basic() -> void:
	var result = BaseLevelModifier.resolve_template("Atiende a {count} estudiante{plural}", {"count": 3, "plural": "s"})
	assert_eq(result, "Atiende a 3 estudiantes", "template: basic substitution")

func test_resolve_template_singular() -> void:
	var result = BaseLevelModifier.resolve_template("Atiende a {count} estudiante{plural}", {"count": 1, "plural": ""})
	assert_eq(result, "Atiende a 1 estudiante", "template: singular")

func test_resolve_template_missing_var() -> void:
	var result = BaseLevelModifier.resolve_template("Test {exists} y {missing}", {"exists": "ok"})
	assert_eq(result, "Test ok y ", "template: missing var stripped to empty")

func test_resolve_template_no_placeholders() -> void:
	var result = BaseLevelModifier.resolve_template("Texto sin placeholders", {})
	assert_eq(result, "Texto sin placeholders", "template: unchanged when no placeholders")


# =============================================================================
# decrease_major
# =============================================================================

func test_decrease_major_blocks() -> void:
	var result = modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.execution_rules.max_blocks, 13,
		"decrease_major: max_blocks debe aumentar 3 → 13")


func test_decrease_major_students() -> void:
	var result = modifier.modify_level("decrease_major", 0.8)
	var queue = result.initial_state.student_queue
	assert_eq(queue.size(), 1,
		"decrease_major: debe quedar 1 estudiante (remove 2)")
	assert_eq(queue[0].nombre, "Ana",
		"debe mantener el primer estudiante, remove últimos")


func test_decrease_major_inventory() -> void:
	var result = modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.initial_state.inventory, ["pan", "cafe", "leche"],
		"decrease_major: inventory 3 items")


func test_decrease_major_hints() -> void:
	var result = modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.feedback_messages.hints.size(), 3,
		"decrease_major: hints reemplazados por 3 hints verbose")


func test_decrease_major_stations() -> void:
	var result = modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.initial_state.stations.bread_dispenser, ["pan"],
		"decrease_major: bread_dispenser refill")
	assert_eq(result.initial_state.stations.drink_dispenser, ["cafe"],
		"decrease_major: drink_dispenser refill")


func test_decrease_major_environment() -> void:
	var result = modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.environment_data.bread_station, true,
		"decrease_major: bread_station visible")
	assert_eq(result.environment_data.drink_machine, true,
		"decrease_major: drink_machine visible")
	assert_eq(result.environment_data.cash_register, true,
		"decrease_major: cash_register visible")


func test_decrease_major_time_limit() -> void:
	var result = modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.execution_rules.time_limit, 0,
		"decrease_major: sin time limit")


func test_decrease_major_expected_outputs_removed() -> void:
	var result = modifier.modify_level("decrease_major", 0.8)
	for expected in result.expected_outputs:
		if expected.has("orders_served"):
			var names := expected.orders_served.map(func(o): return o.nombre)
			assert_eq(expected.orders_served.size(), 1,
				"decrease_major: expected_outputs remueve 2 (queda 1)")
			assert_eq(names[0], "Ana",
				"decrease_major: expected_outputs mantiene primer estudiante")


# =============================================================================
# decrease_minor
# =============================================================================

func test_decrease_minor_blocks() -> void:
	var result = modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.execution_rules.max_blocks, 11,
		"decrease_minor: max_blocks +1 → 11")


func test_decrease_minor_students() -> void:
	var result = modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.initial_state.student_queue.size(), 2,
		"decrease_minor: remove 1 estudiante → 2 quedan")


func test_decrease_minor_inventory() -> void:
	var result = modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.initial_state.inventory, ["pan"],
		"decrease_minor: inventory 1 item")


func test_decrease_minor_hints() -> void:
	var result = modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.feedback_messages.hints.size(), 1,
		"decrease_minor: hints reemplazados por 1 hint")


func test_decrease_minor_stations() -> void:
	var result = modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.initial_state.stations.bread_dispenser, ["pan"],
		"decrease_minor: bread_dispenser refill")


func test_decrease_minor_environment() -> void:
	var result = modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.environment_data.bread_station, true,
		"decrease_minor: bread_station visible")


func test_decrease_minor_time_limit() -> void:
	var result = modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.execution_rules.time_limit, 0,
		"decrease_minor: sin time limit")


func test_decrease_minor_expected_outputs_removed() -> void:
	var result = modifier.modify_level("decrease_minor", 0.9)
	for expected in result.expected_outputs:
		if expected.has("orders_served"):
			assert_eq(expected.orders_served.size(), 2,
				"decrease_minor: expected_outputs remueve 1 (quedan 2)")


# =============================================================================
# keep
# =============================================================================

func test_keep_blocks() -> void:
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.execution_rules.max_blocks, 10,
		"keep: max_blocks sin cambio")


func test_keep_inventory() -> void:
	var original_inv := base_config.initial_state.inventory.duplicate()
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.initial_state.inventory, original_inv,
		"keep: inventory sin cambio")


func test_keep_queue_shuffled() -> void:
	var original_queue := base_config.initial_state.student_queue.duplicate()
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.initial_state.student_queue.size(), original_queue.size(),
		"keep: student_queue mismo tamaño")
	assert_eq(result.version, "1.0",
		"keep: version debe ser la del seed (sin acumulación)")


func test_keep_time_limit() -> void:
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.execution_rules.time_limit, 0,
		"keep: sin time limit")


func test_keep_expected_outputs_unchanged() -> void:
	var result = modifier.modify_level("keep", 1.0)
	for expected in result.expected_outputs:
		if expected.has("orders_served"):
			assert_eq(expected.orders_served.size(), 3,
				"keep: expected_outputs sin cambios (3 ordenes)")


# =============================================================================
# increase_minor
# =============================================================================

func test_increase_minor_blocks() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.execution_rules.max_blocks, 9,
		"increase_minor: max_blocks -1 → 9")


func test_increase_minor_students() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.initial_state.student_queue.size(), 4,
		"increase_minor: +1 estudiante → 4")


func test_increase_minor_inventory_empty() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.initial_state.inventory.size(), 0,
		"increase_minor: inventory vacío (pop no-op desde vacío)")


func test_increase_minor_hints() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.feedback_messages.hints.size(), 3,
		"increase_minor: hints reemplazados por 3 hints crípticos")


func test_increase_minor_stations() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.initial_state.stations.drink_dispenser, [],
		"increase_minor: drink_dispenser vaciado")


func test_increase_minor_environment() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.environment_data.bread_station, true,
		"increase_minor: bread_station visible")
	assert_eq(result.environment_data.drink_machine, false,
		"increase_minor: drink_machine oculta")
	assert_eq(result.environment_data.cash_register, true,
		"increase_minor: cash_register visible")


func test_increase_minor_time_limit() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.execution_rules.time_limit, 90,
		"increase_minor: time limit 90s")


func test_increase_minor_distractor_actions() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_gt(result.defined_actions.size(), 2,
		"increase_minor: debe tener distractors agregados")


func test_increase_minor_expected_outputs_added() -> void:
	var result = modifier.modify_level("increase_minor", 1.1)
	for expected in result.expected_outputs:
		if expected.has("orders_served"):
			var names := expected.orders_served.map(func(o): return o.nombre)
			assert_eq(expected.orders_served.size(), 4,
				"increase_minor: expected_outputs +1 estudiante → 4")
			assert_eq(names[3], "Luisa",
				"increase_minor: expected_outputs agrega a Luisa al final")


# =============================================================================
# increase_major
# =============================================================================

func test_increase_major_blocks() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.execution_rules.max_blocks, 7,
		"increase_major: max_blocks -3 → 7")


func test_increase_major_students() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.initial_state.student_queue.size(), 5,
		"increase_major: +2 estudiantes → 5")


func test_increase_major_inventory() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.initial_state.inventory, [],
		"increase_major: inventory vaciado completo")


func test_increase_major_hints() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.feedback_messages.hints.size(), 0,
		"increase_major: hints vacío (tier none)")


func test_increase_major_stations() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.initial_state.stations.drink_dispenser, [],
		"increase_major: drink_dispenser vaciado")


func test_increase_major_environment() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.environment_data.bread_station, true,
		"increase_major: bread_station visible")
	assert_eq(result.environment_data.drink_machine, false,
		"increase_major: drink_machine oculta")
	assert_eq(result.environment_data.cash_register, false,
		"increase_major: cash_register oculto")


func test_increase_major_time_limit() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.execution_rules.time_limit, 60,
		"increase_major: time limit 60s")


func test_increase_major_distractor_actions() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	assert_gt(result.defined_actions.size(), 5,
		"increase_major: debe tener distractors agregados")


func test_increase_major_expected_outputs_added() -> void:
	var result = modifier.modify_level("increase_major", 1.2)
	for expected in result.expected_outputs:
		if expected.has("orders_served"):
			var names := result.expected_outputs[0].orders_served.map(func(o): return o.nombre)
			assert_eq(expected.orders_served.size(), 5,
				"increase_major: expected_outputs +2 estudiantes → 5")
			assert_eq(names[3], "Luisa",
				"increase_major: expected_outputs agrega a Luisa")
			assert_eq(names[4], "Carlos",
				"increase_major: expected_outputs agrega a Carlos")


# =============================================================================
# blocks minimum floor (max_blocks no baja de 6)
# =============================================================================

func test_blocks_floor_increase_minor() -> void:
	var low_config = base_config.duplicate(true)
	low_config.execution_rules.max_blocks = 6
	modifier.set_level_segment({
		"segment_id": 0,
		"configuration": low_config
	})
	var result = modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.execution_rules.max_blocks, 6,
		"increase_minor: max_blocks no debe bajar de 6")


func test_blocks_floor_increase_major() -> void:
	var low_config = base_config.duplicate(true)
	low_config.execution_rules.max_blocks = 7
	modifier.set_level_segment({
		"segment_id": 0,
		"configuration": low_config
	})
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.execution_rules.max_blocks, 6,
		"increase_major: max_blocks no debe bajar de 6 (7-3=6 OK)")


# =============================================================================
# Immutability: multiple calls must not corrupt
# =============================================================================

func test_immutability_after_multiple_calls() -> void:
	for i in range(5):
		modifier.modify_level("decrease_major", 0.8)
		modifier.modify_level("increase_major", 1.2)
		modifier.modify_level("keep", 1.0)
	
	var fresh_modifier = LevelOneModifier.new()
	fresh_modifier.set_level_segment({
		"segment_id": 0,
		"configuration": base_config.duplicate(true)
	})
	var result := fresh_modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.execution_rules.max_blocks, 13,
		"despues de ciclos: max_blocks correcto")
	assert_eq(result.feedback_messages.hints.size(), 3,
		"despues de ciclos: hints size correcto")


# =============================================================================
# defined_actions: distractors no duplican acciones existentes
# =============================================================================

func test_distractors_no_duplicates() -> void:
	var single_action_config = base_config.duplicate(true)
	single_action_config.defined_actions = [
		{"name": "Tomar pan", "value": "get_bread"}
	]
	modifier.set_level_segment({
		"segment_id": 0,
		"configuration": single_action_config
	})
	var result = modifier.modify_level("increase_major", 1.2)
	
	var value_count := 0
	for action in result.defined_actions:
		if action.value == "get_bread":
			value_count += 1
	assert_eq(value_count, 1,
		"distractors: get_bread no debe duplicarse")


# =============================================================================
# expected_outputs: no se actualiza si no hay orders_served
# =============================================================================

func test_expected_outputs_inventory_format_ignored() -> void:
	# Segments 1-2 use inventory_contains, not orders_served
	var inv_config = base_config.duplicate(true)
	inv_config.expected_outputs = [
		{"inventory_contains": ["pan"]}
	]
	modifier.set_level_segment({
		"segment_id": 0,
		"configuration": inv_config
	})
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.expected_outputs[0].inventory_contains, ["pan"],
		"inventory_contains: no debe modificarse con estudiantes")


# =============================================================================
# validation criteria generation
# =============================================================================

func test_validation_criteria_orders_served() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.expected_outputs = [{"orders_served": [{"nombre": "Ana", "pedido": "pan"}]}]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.validation_criteria.size(), 1,
		"validation: debe generar 1 criterio")
	assert_true(result.validation_criteria[0].condition.contains("Ana"),
		"validation: condicion debe mencionar a Ana")


func test_validation_criteria_inventory_contains() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.expected_outputs = [{"inventory_contains": ["pan"]}]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_true(result.validation_criteria.size() > 0,
		"validation: debe generar criterio para inventory_contains")


# =============================================================================
# distractor filtering per segment_type
# =============================================================================

func test_distractor_filtering_bread_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_major", 1.2)
	for action in result.defined_actions:
		var is_drink = action.value in ["prepare_drink", "serve_drink"]
		assert_false(is_drink,
			"distractors: bread-only NO debe tener drink actions. Found: %s" % action.value)


func test_distractor_filtering_drink_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "drink-only"
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_major", 1.2)
	for action in result.defined_actions:
		var is_bread = action.value in ["get_bread", "prepare_bread", "serve_bread"]
		assert_false(is_bread,
			"distractors: drink-only NO debe tener bread actions. Found: %s" % action.value)


func test_distractor_filtering_mixed_allows_all() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "mixed"
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_major", 1.2)
	assert_gt(result.defined_actions.size(), 2,
		"distractors: mixed debe tener distractors")


# =============================================================================
# environment-action consistency
# =============================================================================

func test_environment_bread_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.environment_data = {"bread_station": false, "drink_machine": false, "cash_register": false}
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.environment_data.bread_station, true,
		"env: bread-only bread_station debe ser true")
	assert_eq(result.environment_data.drink_machine, false,
		"env: bread-only drink_machine debe ser false")


func test_environment_drink_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "drink-only"
	cfg.environment_data = {"bread_station": true, "drink_machine": false, "cash_register": true}
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.environment_data.bread_station, false,
		"env: drink-only bread_station debe ser false")
	assert_eq(result.environment_data.drink_machine, true,
		"env: drink-only drink_machine debe ser true")


func test_environment_mixed() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "mixed"
	cfg.environment_data = {"bread_station": false, "drink_machine": false, "cash_register": false}
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.environment_data.bread_station, true,
		"env: mixed bread_station debe ser true")
	assert_eq(result.environment_data.drink_machine, true,
		"env: mixed drink_machine debe ser true")


# =============================================================================
# inventory_contains sync
# =============================================================================

func test_inventory_contains_unchanged_by_students() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.expected_outputs = [{"inventory_contains": ["pan"]}]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_major", 1.2)
	assert_eq(result.expected_outputs[0].inventory_contains, ["pan"],
		"inventory: no debe modificarse por cambios de estudiantes")


# =============================================================================
# backward compat (no metadata)
# =============================================================================

func test_backward_compat_no_segment_type() -> void:
	var cfg = base_config.duplicate(true)
	cfg.erase("segment_type")
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.execution_rules.max_blocks, 10,
		"backward: max_blocks unchanged without metadata")
	assert_eq(result.initial_state.student_queue.size(), 3,
		"backward: students unchanged without metadata")


func test_backward_compat_all_states() -> void:
	var cfg = base_config.duplicate(true)
	cfg.erase("segment_type")
	cfg.erase("templates")
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	
	var states = ["decrease_major", "decrease_minor", "keep", "increase_minor", "increase_major"]
	var difficulties = [0.8, 0.9, 1.0, 1.1, 1.2]
	for i in range(states.size()):
		var result = modifier.modify_level(states[i], difficulties[i])
		assert_false(result.is_empty(),
			"backward: %s debe retornar config no vacia sin metadata" % states[i])


# =============================================================================
# difficulty_bounds enforcement (Fix 1)
# =============================================================================

func test_difficulty_bounds_clamps_students() -> void:
	var cfg = base_config.duplicate(true)
	cfg.difficulty_bounds = {"min_students": 1, "max_students": 2, "min_blocks": 3, "max_blocks": 5}
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.initial_state.student_queue.size(), 2,
		"difficulty_bounds: student_queue clamped from 3 to max 2")
	assert_eq(result.execution_rules.max_blocks, 5,
		"difficulty_bounds: max_blocks clamped from 10 to max 5")


func test_difficulty_bounds_pads_students() -> void:
	var cfg = base_config.duplicate(true)
	cfg.initial_state.student_queue = []
	cfg.difficulty_bounds = {"min_students": 2, "max_students": 5, "min_blocks": 3, "max_blocks": 10}
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.initial_state.student_queue.size(), 2,
		"difficulty_bounds: student_queue padded from 0 to min 2")


# =============================================================================
# validation_criteria se genera FRESCO desde expected_outputs (no acumula)
# =============================================================================

func test_validation_criteria_no_accumulation() -> void:
	# Los validation_criteria viejos en el cfg (del adaptation_state persistido)
	# NO deben heredarse — se regeneran completos desde expected_outputs.
	var cfg = base_config.duplicate(true)
	cfg.validation_criteria = ["Ana served"]  # viejo criterio legacy
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.validation_criteria.size(), 1,
		"validation: ignora criteria legacy, genera 1 fresco desde expected_outputs")


# =============================================================================
# validation_criteria type field (Fix 4)
# =============================================================================

func test_validation_criteria_type_min() -> void:
	var cfg = base_config.duplicate(true)
	cfg.expected_outputs = [{"orders_served": [{"nombre": "Ana", "pedido": "pan"}], "type": "min"}]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.validation_criteria[0].get("type", ""), "min",
		"type min: criteria has type field set to min")


# =============================================================================
# station inventory consistency (Fix 5)
# =============================================================================

func test_station_sync_bread_only_clears_drink() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.initial_state.stations.drink_dispenser = ["cafe"]
	cfg.initial_state.stations.bread_dispenser = []
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.initial_state.stations.drink_dispenser, [],
		"station_sync: bread-only clears drink_dispenser")
	assert_eq(result.initial_state.stations.bread_dispenser, ["pan"],
		"station_sync: bread-only fills bread_dispenser")


func test_station_sync_drink_only_clears_bread() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "drink-only"
	cfg.initial_state.stations.bread_dispenser = ["pan"]
	cfg.initial_state.stations.drink_dispenser = []
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_eq(result.initial_state.stations.bread_dispenser, [],
		"station_sync: drink-only clears bread_dispenser")
	assert_eq(result.initial_state.stations.drink_dispenser, ["cafe"],
		"station_sync: drink-only fills drink_dispenser")


# =============================================================================
# auto-detect expected_outputs format (Fix 6)
# =============================================================================

func test_auto_expected_outputs_with_students() -> void:
	var cfg = base_config.duplicate(true)
	cfg.erase("expected_outputs")
	cfg.initial_state.student_queue = [{"nombre": "Ana", "pedido": "pan"}]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_true(result.has("expected_outputs"),
		"auto: expected_outputs should be generated")
	assert_eq(result.expected_outputs[0].orders_served[0].nombre, "Ana",
		"auto: should contain Ana in orders_served")


func test_auto_expected_outputs_empty_queue_inventory() -> void:
	var cfg = base_config.duplicate(true)
	cfg.erase("expected_outputs")
	cfg.initial_state.student_queue = []
	cfg.initial_state.stations.bread_dispenser = ["pan"]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	assert_true(result.has("expected_outputs"),
		"auto: expected_outputs should be generated for empty queue")
	assert_true(result.expected_outputs[0].has("inventory_contains"),
		"auto: empty queue should use inventory_contains format")


# =============================================================================
# integration - full modifier flow with metadata
# =============================================================================

func test_integration_full_flow_bread_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.required_actions = ["get_bread", "prepare_bread", "serve_bread"]
	cfg.templates = {
		"keep": {
			"title": "Test {student_count} estudiante{student_plural}",
			"description": "Descripcion test",
			"learning_objective": "Objetivo test"
		}
	}
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	
	assert_eq(result.title, "Test 3 estudiantes",
		"integration: title debe usar template con student_count")
	
	assert_eq(result.environment_data.bread_station, true,
		"integration: bread_station visible")
	assert_eq(result.environment_data.drink_machine, false,
		"integration: drink_machine oculta")
	
	assert_true(result.has("validation_criteria"),
		"integration: debe tener validation_criteria")
	
	assert_false(result.get("title", "").is_empty(),
		"integration: title no debe estar vacio")
	assert_false(result.get("description", "").is_empty(),
		"integration: description no debe estar vacio")


# =============================================================================
# chain action inference (_ensure_chain_actions_present)
# =============================================================================

func test_chain_inference_bread_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.defined_actions = [
		{"name": "Tomar pan", "value": "get_bread"}
	]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	var values := result.defined_actions.map(func(a): return a.value)
	assert_true("prepare_bread" in values,
		"chain: bread-only debe agregar prepare_bread")
	assert_true("serve_bread" in values,
		"chain: bread-only debe agregar serve_bread")


func test_chain_inference_drink_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "drink-only"
	cfg.defined_actions = [
		{"name": "Servir bebida", "value": "serve_drink"}
	]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	var values := result.defined_actions.map(func(a): return a.value)
	assert_true("prepare_drink" in values,
		"chain: drink-only debe agregar prepare_drink")


func test_chain_inference_no_duplicates() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.defined_actions = [
		{"name": "Tomar pan", "value": "get_bread"},
		{"name": "Preparar pan", "value": "prepare_bread"},
		{"name": "Servir pan", "value": "serve_bread"}
	]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	var count := 0
	for action in result.defined_actions:
		if action.value == "prepare_bread":
			count += 1
	assert_eq(count, 1,
		"chain: no debe duplicar prepare_bread si ya existe")


func test_chain_inference_empty_queue_skips() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	cfg.initial_state.student_queue = []
	cfg.defined_actions = [
		{"name": "Tomar pan", "value": "get_bread"}
	]
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("keep", 1.0)
	var count := 0
	for action in result.defined_actions:
		if action.value in ["prepare_bread", "serve_bread"]:
			count += 1
	assert_eq(count, 0,
		"chain: sin estudiantes no debe agregar acciones de cadena")


# =============================================================================
# segment-aware student adding
# =============================================================================

func test_increase_minor_student_bread_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_minor", 1.1)
	var queue = result.initial_state.student_queue
	var last = queue[queue.size() - 1]
	assert_eq(last.pedido, "pan",
		"increase_minor bread-only: estudiante agregado debe pedir pan")


func test_increase_minor_student_drink_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "drink-only"
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_minor", 1.1)
	var queue = result.initial_state.student_queue
	var last = queue[queue.size() - 1]
	assert_eq(last.pedido, "cafe",
		"increase_minor drink-only: estudiante agregado debe pedir cafe")


func test_increase_major_students_bread_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_major", 1.2)
	var queue = result.initial_state.student_queue
	# Los últimos 2 son los agregados (increase_major agrega 2)
	var last = queue[queue.size() - 1]
	var second_last = queue[queue.size() - 2]
	assert_eq(last.pedido, "pan",
		"increase_major bread-only: ultimo estudiante agregado debe pedir pan")
	assert_eq(second_last.pedido, "pan",
		"increase_major bread-only: penultimo estudiante agregado debe pedir pan")


func test_increase_major_students_drink_only() -> void:
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "drink-only"
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	var result = modifier.modify_level("increase_major", 1.2)
	var queue = result.initial_state.student_queue
	var last = queue[queue.size() - 1]
	var second_last = queue[queue.size() - 2]
	assert_eq(last.pedido, "cafe",
		"increase_major drink-only: ultimo estudiante agregado debe pedir cafe")
	assert_eq(second_last.pedido, "cafe",
		"increase_major drink-only: penultimo estudiante agregado debe pedir cafe")


func test_increase_all_student_count_unchanged() -> void:
	# Verificar que los count de estudiantes no cambian con los nuevos cambios
	var cfg = base_config.duplicate(true)
	cfg.segment_type = "bread-only"
	modifier.set_level_segment({"segment_id": 0, "configuration": cfg})
	
	var minor = modifier.modify_level("increase_minor", 1.1)
	assert_eq(minor.initial_state.student_queue.size(), 4,
		"increase_minor bread-only: debe tener 4 estudiantes (3+1)")
	
	var major = modifier.modify_level("increase_major", 1.2)
	assert_eq(major.initial_state.student_queue.size(), 5,
		"increase_major bread-only: debe tener 5 estudiantes (3+2)")
