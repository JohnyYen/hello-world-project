# test_rule_based_inference.gd
# Tests for RuleBasedInference with graduated multi-threshold actions
extends GutTest

var RuleBasedInference = load("res://scripts/agent/inference/rule_inference.gd")
var engine


func before_each() -> void:
	engine = RuleBasedInference.new()
	# Force pure score-based decisions (no trend contribution)
	engine.set_hybrid_weights(1.0, 0.0)


# =============================================================================
# Initialization
# =============================================================================

func test_initialization() -> void:
	assert_not_null(engine, "engine debe ser no null")
	assert_not_null(engine.trend_calculator, "trend_calculator debe ser no null")
	assert_eq(engine.score_weight, 1.0, "score_weight debe ser 1.0 tras set_hybrid_weights(1,0)")
	assert_eq(engine.trend_weight, 0.0, "trend_weight debe ser 0.0 tras set_hybrid_weights(1,0)")


# =============================================================================
# Threshold map (with trend_weight=0, hybrid == score):
#   [0.0, 0.3) → decrease_major
#   [0.3, 0.5) → decrease_minor
#   [0.5, 0.8] → keep
#   (0.8, 0.9] → increase_minor
#   (0.9, 1.0] → increase_major
# =============================================================================

func test_score_02_returns_decrease_major() -> void:
	var action := engine.decide_action({"score": 0.2, "trend": 0.0})
	assert_eq(action, "decrease_major", "score=0.2 → decrease_major")


func test_score_04_returns_decrease_minor() -> void:
	var action := engine.decide_action({"score": 0.4, "trend": 0.0})
	assert_eq(action, "decrease_minor", "score=0.4 → decrease_minor")


func test_score_06_returns_keep() -> void:
	var action := engine.decide_action({"score": 0.6, "trend": 0.0})
	assert_eq(action, "keep", "score=0.6 → keep")


func test_score_085_returns_increase_minor() -> void:
	# With trend=0: hybrid = 0.85*1.0 + 0.5*0.0 = 0.85, which is > 0.8 and <= 0.9
	var action := engine.decide_action({"score": 0.85, "trend": 0.0})
	assert_eq(action, "increase_minor", "score=0.85 → increase_minor")


func test_score_095_returns_increase_major() -> void:
	# With trend=0.8: normalized_trend = (0.8+1)/2 = 0.9
	# hybrid = 0.95*1.0 + 0.9*0.0 = 0.95, which is > 0.9
	# But wait - with trend_weight=0, trend doesn't matter
	# hybrid = 0.95 * 1.0 = 0.95 > 0.9 → increase_major ✓
	var action := engine.decide_action({"score": 0.95, "trend": 0.0})
	assert_eq(action, "increase_major", "score=0.95 → increase_major")


# =============================================================================
# Boundary values
# =============================================================================

func test_boundary_03_returns_decrease_minor() -> void:
	# hybrid = 0.3, NOT < 0.3, next: 0.3 < 0.5 → decrease_minor
	var action := engine.decide_action({"score": 0.3, "trend": 0.0})
	assert_eq(action, "decrease_minor", "score=0.3 (boundary) → decrease_minor")


func test_boundary_05_returns_keep() -> void:
	# hybrid = 0.5, NOT < 0.3, NOT < 0.5, 0.5 <= 0.8 → keep
	var action := engine.decide_action({"score": 0.5, "trend": 0.0})
	assert_eq(action, "keep", "score=0.5 (boundary) → keep")


func test_boundary_08_returns_keep() -> void:
	# hybrid = 0.8, <= 0.8 → keep
	var action := engine.decide_action({"score": 0.8, "trend": 0.0})
	assert_eq(action, "keep", "score=0.8 (boundary) → keep")


func test_boundary_09_returns_increase_major() -> void:
	# hybrid = 0.9, NOT <= 0.8, NOT <= 0.9... wait
	# 0.9 <= 0.9 in the elif → increase_minor
	var action := engine.decide_action({"score": 0.9, "trend": 0.0})
	assert_eq(action, "increase_minor", "score=0.9 (boundary) → increase_minor")


func test_boundary_min_score() -> void:
	var action := engine.decide_action({"score": 0.0, "trend": 0.0})
	assert_eq(action, "decrease_major", "score=0.0 → decrease_major")


func test_boundary_max_score() -> void:
	var action := engine.decide_action({"score": 1.0, "trend": 0.0})
	assert_eq(action, "increase_major", "score=1.0 → increase_major")


# =============================================================================
# With hints_used and efficiency_rating (these shouldn't affect the decision)
# =============================================================================

func test_hints_used_passed_through() -> void:
	var action := engine.decide_action({
		"score": 0.6, "trend": 0.0,
		"hints_used": 5, "efficiency_rating": 70.0
	})
	assert_eq(action, "keep", "hints_used no debe afectar la acción")


# =============================================================================
# set_hybrid_weights()
# =============================================================================

func test_set_hybrid_weights_normalization() -> void:
	engine.set_hybrid_weights(0.8, 0.2)
	var total := engine.score_weight + engine.trend_weight
	assert_gt(total, 0.99, "pesos deben sumar ~1.0")
	assert_lt(total, 1.01, "pesos deben sumar ~1.0")


func test_set_hybrid_weights_invalid() -> void:
	# Should not change weights if both are 0
	var orig_score := engine.score_weight
	var orig_trend := engine.trend_weight
	engine.set_hybrid_weights(0.0, 0.0)
	assert_eq(engine.score_weight, orig_score, "pesos inválidos no deben cambiar score_weight")
	assert_eq(engine.trend_weight, orig_trend, "pesos inválidos no deben cambiar trend_weight")


# =============================================================================
# Edge cases
# =============================================================================

func test_negative_trend_pulls_down() -> void:
	engine.set_hybrid_weights(0.7, 0.3)
	# score=0.7, trend=-0.5 → norm_trend=(−0.5+1)/2=0.25
	# hybrid = 0.7*0.7 + 0.25*0.3 = 0.49+0.075 = 0.565 → keep
	var action := engine.decide_action({"score": 0.7, "trend": -0.5})
	assert_eq(action, "keep", "trend negativo con score moderado debe dar keep")


func test_strong_positive_trend_triggers_increase_major() -> void:
	engine.set_hybrid_weights(0.7, 0.3)
	# score=0.95, trend=0.8 → norm_trend=(0.8+1)/2=0.9
	# hybrid = 0.95*0.7 + 0.9*0.3 = 0.665+0.27 = 0.935 > 0.9 → increase_major
	var action := engine.decide_action({"score": 0.95, "trend": 0.8})
	assert_eq(action, "increase_major", "score alto + trend fuerte → increase_major")
