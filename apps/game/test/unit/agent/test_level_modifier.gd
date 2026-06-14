# test_level_modifier.gd
# Tests for LevelOneModifier proportional modifications
extends GutTest

var LevelOneModifier = load("res://scripts/agent/level_modifier/level_one_modifier.gd")
var modifier
var base_config: Dictionary


func before_each() -> void:
	modifier = LevelOneModifier.new()
	base_config = {
		"execution_rules": {"max_blocks": 10},
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
		"version": "1.0"
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
		"decrease_major: hints +2 → 3 total")


func test_decrease_major_stations() -> void:
	var result := modifier.modify_level("decrease_major", 0.8)
	assert_eq(result.initial_state.stations.bread_dispenser, ["pan"],
		"decrease_major: bread_dispenser refill")
	assert_eq(result.initial_state.stations.drink_dispenser, ["cafe"],
		"decrease_major: drink_dispenser refill")


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
	assert_eq(result.feedback_messages.hints.size(), 2,
		"decrease_minor: hints +1 → 2 total")


func test_decrease_minor_stations() -> void:
	var result := modifier.modify_level("decrease_minor", 0.9)
	assert_eq(result.initial_state.stations.bread_dispenser, ["pan"],
		"decrease_minor: bread_dispenser refill")


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
	# Same size but order may differ (shuffle)
	assert_eq(result.initial_state.student_queue.size(), original_queue.size(),
		"keep: student_queue mismo tamaño")
	# Ensure version was bumped as mark of keep
	assert_eq(result.version, "1.0.maintained",
		"keep: version debe marcar .maintained")


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
	assert_eq(result.feedback_messages.hints.size(), 0,
		"increase_minor: hints -1 → 0")


func test_increase_minor_stations() -> void:
	var result := modifier.modify_level("increase_minor", 1.1)
	assert_eq(result.initial_state.stations.drink_dispenser, [],
		"increase_minor: drink_dispenser vaciado")


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
		"increase_major: hints -2 (min 0) → 0")


func test_increase_major_stations() -> void:
	var result := modifier.modify_level("increase_major", 1.2)
	assert_eq(result.initial_state.stations.drink_dispenser, [],
		"increase_major: drink_dispenser vaciado")


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
