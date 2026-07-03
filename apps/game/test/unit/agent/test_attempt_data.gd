# test_attempt_data.gd
# Tests for AttemptData with enriched fields and validation
extends GutTest

const EPSILON := 0.0001


func test_from_dictionary_with_all_fields() -> void:
	var raw := {
		"score": 0.85,
		"errors": 2,
		"time": 45.0,
		"level_id": 1,
		"actor_id": "test-actor-uuid",
		"timestamp": "2026-06-14T12:00:00",
		"hints_used": 3,
		"efficiency_rating": 72.5,
		"objectives_completed": 4,
		"blocks_count": 12,
		"error_details": {"attempt_1": {"msg": "timeout"}},
		"custom_events": [{"type": "hint", "index": 0}]
	}

	var attempt := AttemptData.from_dictionary(raw)

	assert_eq(attempt.score, 0.85, "score debe coincidir")
	assert_eq(attempt.errors, 2, "errors debe coincidir")
	assert_eq(attempt.time, 45.0, "time debe coincidir")
	assert_eq(attempt.level_id, 1, "level_id debe coincidir")
	assert_eq(attempt.actor_id, "test-actor-uuid", "actor_id debe coincidir")
	assert_eq(attempt.hints_used, 3, "hints_used debe coincidir")
	assert_eq(attempt.efficiency_rating, 72.5, "efficiency_rating debe coincidir")
	assert_eq(attempt.objectives_completed, 4, "objectives_completed debe coincidir")
	assert_eq(attempt.blocks_count, 12, "blocks_count debe coincidir")
	assert_eq(attempt.error_details, {"attempt_1": {"msg": "timeout"}}, "error_details debe coincidir")
	assert_eq(attempt.custom_events, [{"type": "hint", "index": 0}], "custom_events debe coincidir")


func test_from_dictionary_with_only_required_fields() -> void:
	var raw := {"score": 0.6, "errors": 1, "time": 30.0}

	var attempt := AttemptData.from_dictionary(raw)

	assert_eq(attempt.hints_used, 0, "hints_used default debe ser 0")
	assert_eq(attempt.efficiency_rating, 0.0, "efficiency_rating default debe ser 0.0")
	assert_eq(attempt.objectives_completed, 0, "objectives_completed default debe ser 0")
	assert_eq(attempt.blocks_count, 0, "blocks_count default debe ser 0")
	assert_eq(attempt.error_details, {}, "error_details default debe ser {}")
	assert_eq(attempt.custom_events, [], "custom_events default debe ser []")
	assert_eq(attempt.level_id, 0, "level_id default debe ser 0")
	assert_eq(attempt.actor_id, "", "actor_id default debe ser vacío")


func test_validation_clamps_efficiency_rating() -> void:
	var raw := {"score": 0.7, "errors": 0, "time": 20.0, "efficiency_rating": 150.0}

	var attempt := AttemptData.from_dictionary(raw)

	assert_eq(attempt.efficiency_rating, 100.0, "efficiency_rating > 100 debe clamp a 100")


func test_validation_clamps_negative_efficiency_rating() -> void:
	var raw := {"score": 0.7, "errors": 0, "time": 20.0, "efficiency_rating": -10.0}

	var attempt := AttemptData.from_dictionary(raw)

	assert_eq(attempt.efficiency_rating, 0.0, "efficiency_rating < 0 debe clamp a 0")


func test_validation_clamps_hints_used_negative() -> void:
	var raw := {"score": 0.5, "errors": 0, "time": 10.0, "hints_used": -5}

	var attempt := AttemptData.from_dictionary(raw)

	assert_eq(attempt.hints_used, 0, "hints_used negativo debe ser 0")


func test_validation_clamps_score() -> void:
	var raw := {"score": 1.5, "errors": 0, "time": 10.0}

	var attempt := AttemptData.from_dictionary(raw)

	assert_eq(attempt.score, 1.0, "score > 1 debe clamp a 1")


func test_to_dictionary_round_trip() -> void:
	var raw := {
		"score": 0.75,
		"errors": 3,
		"time": 60.0,
		"level_id": 2,
		"actor_id": "actor-roundtrip",
		"hints_used": 5,
		"efficiency_rating": 88.0,
		"objectives_completed": 6,
		"blocks_count": 15,
		"error_details": {"err": "test"},
		"custom_events": [{"custom": "event"}]
	}

	var attempt := AttemptData.from_dictionary(raw)
	var output := attempt.to_dictionary()

	assert_eq(output.score, 0.75, "to_dictionary score debe coincidir")
	assert_eq(output.errors, 3, "to_dictionary errors debe coincidir")
	assert_eq(output.time, 60.0, "to_dictionary time debe coincidir")
	assert_eq(output.level_id, 2, "to_dictionary level_id debe coincidir")
	assert_eq(output.actor_id, "actor-roundtrip", "to_dictionary actor_id debe coincidir")
	assert_eq(output.hints_used, 5, "to_dictionary hints_used debe coincidir")
	assert_eq(output.efficiency_rating, 88.0, "to_dictionary efficiency_rating debe coincidir")
	assert_eq(output.objectives_completed, 6, "to_dictionary objectives_completed debe coincidir")
	assert_eq(output.blocks_count, 15, "to_dictionary blocks_count debe coincidir")
	assert_eq(output.error_details, {"err": "test"}, "to_dictionary error_details debe coincidir")
	assert_eq(output.custom_events, [{"custom": "event"}], "to_dictionary custom_events debe coincidir")
	assert_eq(output.has("timestamp"), true, "to_dictionary debe incluir timestamp")
