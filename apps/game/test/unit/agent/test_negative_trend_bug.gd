# test_negative_trend_bug.gd
# Test to verify that negative trend (declining performance) DECREASES difficulty
extends GutTest

const EPSILON := 0.001

var agent: AdaptiveAgent


func before_each() -> void:
	AttemptHistoryPersistence.clear_history()
	agent = AdaptiveAgent.new()


# =============================================================================
# Helper: Trace hybrid metric calculation manually
# =============================================================================

func _calculate_expected_hybrid(score: float, trend: float) -> float:
	# Same logic as TrendCalculator.calculate_hybrid_metric
	var norm_score := clamp(score, 0.0, 1.0)
	var norm_trend := clamp((trend + 1.0) / 2.0, 0.0, 1.0)
	return norm_score * 0.7 + norm_trend * 0.3


func _expected_action_from_hybrid(hybrid: float) -> String:
	# Same logic as RuleBasedInference._calculate_multi_threshold
	if hybrid < 0.3:
		return "decrease_major"
	elif hybrid < 0.5:
		return "decrease_minor"
	elif hybrid <= 0.8:
		return "keep"
	elif hybrid <= 0.9:
		return "increase_minor"
	else:
		return "increase_major"


# =============================================================================
# Bug verification: negative trend should decrease difficulty
# =============================================================================

func test_negative_trend_declining_scores_should_decrease_difficulty() -> void:
	# Starting difficulty
	agent.difficulty = 1.0
	
	# Add 5 attempts with DECREASING scores (clearly worsening trend)
	# [0.9, 0.7, 0.5, 0.3, 0.2] - the student is getting worse each time
	for score in [0.9, 0.7, 0.5, 0.3, 0.2]:
		agent.analyze_and_decide({"score": score, "errors": 2, "time": 60.0})
	
	# MANUAL CALCULATION:
	# blended_score = (0.9+0.7+0.5+0.3+0.2)/5 = 0.52
	# For WEIGHTED trend with 5 attempts:
	#   recent_avg = (0.2 + 0.3) / 2 = 0.25
	#   old_avg = (0.9 + 0.7) / 2 = 0.8
	#   trend = 0.25 - 0.8 = -0.55
	# normalized_trend = (-0.55 + 1) / 2 = 0.225
	# hybrid = 0.52 * 0.7 + 0.225 * 0.3 = 0.364 + 0.0675 = 0.4315
	# action = "decrease_minor" (since 0.3 < 0.4315 < 0.5)
	
	# VERIFICATION: With negative trend, difficulty should DECREASE
	assert_lt(agent.difficulty, 1.0, 
		"BUG DETECTADO: trend negativo debe BAJAR difficulty (0.4315 → decrease_minor). Final=%.2f" % agent.difficulty)


func test_positive_trend_improving_scores_should_increase_difficulty() -> void:
	# Starting difficulty
	agent.difficulty = 1.0
	
	# Add 5 attempts with INCREASING scores (clearly improving trend)
	# [0.2, 0.3, 0.5, 0.7, 0.9] - the student is getting better each time
	for score in [0.2, 0.3, 0.5, 0.7, 0.9]:
		agent.analyze_and_decide({"score": score, "errors": 1, "time": 30.0})
	
	# MANUAL CALCULATION:
	# blended_score = 0.52
	# trend = 0.55 (positive)
	# normalized_trend = (0.55 + 1) / 2 = 0.775
	# hybrid = 0.52 * 0.7 + 0.775 * 0.3 = 0.364 + 0.2325 = 0.5965
	# action = "keep" or "increase_minor" (since 0.5 < 0.5965 <= 0.8)
	
	# With positive trend, difficulty should INCREASE or stay
	assert_gt(agent.difficulty, 0.9, 
		"trend positivo debe SUBIR difficulty. Final=%.2f (expected > 0.9)" % agent.difficulty)


func test_trace_hybrid_metric_calculation_for_negative_trend() -> void:
	# Isolate the TrendCalculator to verify hybrid metric math
	var calc := TrendCalculator.new()
	
	# Simulate declining scores: [0.9, 0.7, 0.5, 0.3, 0.2]
	var history := []
	for s in [0.9, 0.7, 0.5, 0.3, 0.2]:
		history.append(AttemptData.new(s, 1, 30.0))
	
	# Calculate trend
	var trend := calc.calculate(history, TrendCalculator.TrendMode.WEIGHTED)
	
	# Blended score used in decide_action is short_term_avg (average of all 5)
	var blended_score := history.map(func(a): return a.score).reduce(func(accum, s): return accum + s, 0.0) / 5.0
	
	# Calculate hybrid metric
	var hybrid := calc.calculate_hybrid_metric(blended_score, trend)
	
	# Manual calculation
	var expected_hybrid := _calculate_expected_hybrid(blended_score, trend)
	var expected_action := _expected_action_from_hybrid(expected_hybrid)
	
	print("[TEST] Blended score: %.4f" % blended_score)
	print("[TEST] Trend: %.4f" % trend)
	print("[TEST] Hybrid metric: %.4f (expected: %.4f)" % [hybrid, expected_hybrid])
	print("[TEST] Expected action: %s" % expected_action)
	
	# Trend MUST be negative for declining scores
	assert_lt(trend, 0.0, "Declining scores must produce negative trend, got: %.4f" % trend)
	
	# Hybrid MUST be low (< 0.5) to trigger decrease action
	assert_lt(hybrid, 0.5, "Hybrid metric with negative trend must be < 0.5. Got: %.4f" % hybrid)