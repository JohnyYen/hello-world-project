# test_level_modifier.gd
# Tests for LevelOneModifier proportional modifications
extends GutTest

var LevelOneModifier = load("res://scripts/agent/level_modifier/level_one_modifier.gd")
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
# decrease_major
# =============================================================================

func test_decrease_major_blocks() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.execution_rules.max_blocks, 13,
		"decrease_major: max_blocks debe aumentar 3 → 13")


func test_decrease_major_students() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
	var queue = result.initial_state.student_queue
	assert_eq(queue.size(), 1,
		"decrease_major: debe quedar 1 estudiante (remove 2)")
	assert_eq(queue[0].nombre, "Ana",
		"debe mantener el primer estudiante, remove últimos")


func test_decrease_major_inventory() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.initial_state.inventory, ["pan", "cafe", "leche"],
		"decrease_major: inventory 3 items")


func test_decrease_major_hints() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.feedback_messages.hints.size(), 3,
		"decrease_major: hints reemplazados por 3 hints verbose")


func test_decrease_major_stations() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.initial_state.stations.bread_dispenser, ["pan"],
		"decrease_major: bread_dispenser refill")
	assert_eq(result.initial_state.stations.drink_dispenser, ["cafe"],
		"decrease_major: drink_dispenser refill")


func test_decrease_major_environment() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.environment_data.bread_station, true,
		"decrease_major: bread_station visible")
	assert_eq(result.environment_data.drink_machine, true,
		"decrease_major: drink_machine visible")
	assert_eq(result.environment_data.cash_register, true,
		"decrease_major: cash_register visible")


func test_decrease_major_time_limit() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.execution_rules.time_limit, 0,
		"decrease_major: sin time limit")


func test_decrease_major_expected_outputs_removed() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
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
	var result := modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.execution_rules.max_blocks, 11,
		"decrease_minor: max_blocks +1 → 11")


func test_decrease_minor_students() -> void:
	var result := modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.initial_state.student_queue.size(), 2,
		"decrease_minor: remove 1 estudiante → 2 quedan")


func test_decrease_minor_inventory() -> void:
	var result := modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.initial_state.inventory, ["pan"],
		"decrease_minor: inventory 1 item")


func test_decrease_minor_hints() -> void:
	var result := modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.feedback_messages.hints.size(), 1,
		"decrease_minor: hints reemplazados por 1 hint")


func test_decrease_minor_stations() -> void:
	var result := modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.initial_state.stations.bread_dispenser, ["pan"],
		"decrease_minor: bread_dispenser refill")


func test_decrease_minor_environment() -> void:
	var result := modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.environment_data.bread_station, true,
		"decrease_minor: bread_station visible")


func test_decrease_minor_time_limit() -> void:
	var result := modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.execution_rules.time_limit, 0,
		"decrease_minor: sin time limit")


func test_decrease_minor_expected_outputs_removed() -> void:
	var result := modifier.modify_level("decrease_minor", 0.9)
	for expected in result.expected_outputs:
		if expected.has("orders_served"):
			assert_eq(expected.orders_served.size(), 2,
				"decrease_minor: expected_outputs remueve 1 (quedan 2)")


# =============================================================================
# keep
# =============================================================================

func test_keep_blocks() -> void:
	var result := modifier.modify_level("keep", 1.0)
	assert_eq(result.execution_rules.max_blocks, 10,
		"keep: max_blocks sin cambio")


func test_keep_inventory() -> void:
	var original_inv := base_config.initial_state.inventory.duplicate()
	var result := modifier.modify_level("keep", 1.0)
	assert_eq(result.initial_state.inventory, original_inv,
		"keep: inventory sin cambio")


func test_keep_queue_shuffled() -> void:
	var original_queue := base_config.initial_state.student_queue.duplicate()
	var result := modifier.modify_level("keep", 1.0)
	assert_eq(result.initial_state.student_queue.size(), original_queue.size(),
		"keep: student_queue mismo tamaño")
	assert_eq(result.version, "1.0.maintained",
		"keep: version debe marcar .maintained")


func test_keep_time_limit() -> void:
	var result := modifier.modify_level("keep", 1.0)
	assert_eq(result.execution_rules.time_limit, 0,
		"keep: sin time limit")


func test_keep_expected_outputs_unchanged() -> void:
	var result := modifier.modify_level("keep", 1.0)
	for expected in result.expected_outputs:
		if expected.has("orders_served"):
			assert_eq(expected.orders_served.size(), 3,
				"keep: expected_outputs sin cambios (3 ordenes)")


# =============================================================================
# increase_minor
# =============================================================================

func test_increase_minor_blocks() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.execution_rules.max_blocks, 9,
		"increase_minor: max_blocks -1 → 9")


func test_increase_minor_students() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.initial_state.student_queue.size(), 4,
		"increase_minor: +1 estudiante → 4")


func test_increase_minor_inventory_empty() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.initial_state.inventory.size(), 0,
		"increase_minor: inventory vacío (pop no-op desde vacío)")


func test_increase_minor_hints() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.feedback_messages.hints.size(), 3,
		"increase_minor: hints reemplazados por 3 hints crípticos")


func test_increase_minor_stations() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.initial_state.stations.drink_dispenser, [],
		"increase_minor: drink_dispenser vaciado")


func test_increase_minor_environment() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.environment_data.bread_station, true,
		"increase_minor: bread_station visible")
	assert_eq(result.environment_data.drink_machine, false,
		"increase_minor: drink_machine oculta")
	assert_eq(result.environment_data.cash_register, true,
		"increase_minor: cash_register visible")


func test_increase_minor_time_limit() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.execution_rules.time_limit, 90,
		"increase_minor: time limit 90s")


func test_increase_minor_distractor_actions() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_gt(result.defined_actions.size(), 2,
		"increase_minor: debe tener distractors agregados")


func test_increase_minor_expected_outputs_added() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
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
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.execution_rules.max_blocks, 7,
		"increase_major: max_blocks -3 → 7")


func test_increase_major_students() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.initial_state.student_queue.size(), 5,
		"increase_major: +2 estudiantes → 5")


func test_increase_major_inventory() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.initial_state.inventory, [],
		"increase_major: inventory vaciado completo")


func test_increase_major_hints() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.feedback_messages.hints.size(), 0,
		"increase_major: hints vacío (tier none)")


func test_increase_major_stations() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.initial_state.stations.drink_dispenser, [],
		"increase_major: drink_dispenser vaciado")


func test_increase_major_environment() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.environment_data.bread_station, true,
		"increase_major: bread_station visible")
	assert_eq(result.environment_data.drink_machine, false,
		"increase_major: drink_machine oculta")
	assert_eq(result.environment_data.cash_register, false,
		"increase_major: cash_register oculto")


func test_increase_major_time_limit() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.execution_rules.time_limit, 60,
		"increase_major: time limit 60s")


func test_increase_major_distractor_actions() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
	assert_gt(result.defined_actions.size(), 5,
		"increase_major: debe tener distractors agregados")


func test_increase_major_expected_outputs_added() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
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
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.execution_rules.max_blocks, 6,
		"increase_minor: max_blocks no debe bajar de 6")


func test_blocks_floor_increase_major() -> void:
	var low_config = base_config.duplicate(true)
	low_config.execution_rules.max_blocks = 7
	modifier.set_level_segment({
		"segment_id": 0,
		"configuration": low_config
	})
	var result := modifier.modify_level("increase_major", 1.2)
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
	var result := modifier.modify_level("increase_major", 1.2)
	
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
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.expected_outputs[0].inventory_contains, ["pan"],
		"inventory_contains: no debe modificarse con estudiantes")
