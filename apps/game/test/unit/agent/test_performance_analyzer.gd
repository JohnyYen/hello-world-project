# test_performance_analyzer.gd
# Tests for PerformanceAnalyzer with enriched history tracking
extends GutTest

var PerformanceAnalyzer = load("res://scripts/agent/analizer/performance_analizer.gd")
var analyzer: PerformanceAnalyzer


func before_each() -> void:
	AttemptHistoryPersistence.clear_history()
	analyzer = PerformanceAnalyzer.new()


func test_initialization_defaults() -> void:
	assert_not_null(analyzer, "PerformanceAnalyzer debe ser no null")
	assert_eq(analyzer.avg_score, 0.7, "avg_score inicial debe ser 0.7")
	assert_eq(analyzer.history_size, 50, "history_size debe ser 50")
	assert_eq(analyzer.scores.size(), 0, "scores debe estar vacío")
	assert_eq(analyzer.smooth_alpha, 0.3, "smooth_alpha debe ser 0.3")


func test_normalize_clamps_high_score() -> void:
	var result := analyzer.normalize({"score": 1.5, "errors": 0})
	assert_eq(result.score, 1.0, "score > 1 debe clamp a 1")


func test_normalize_clamps_low_score() -> void:
	var result := analyzer.normalize({"score": -0.5, "errors": 5})
	assert_eq(result.score, 0.0, "score < 0 debe clamp a 0")


func test_normalize_tracks_scores() -> void:
	analyzer.normalize({"score": 0.6, "errors": 3})
	analyzer.normalize({"score": 0.8, "errors": 1})

	assert_eq(analyzer.scores.size(), 2, "debe tener 2 scores registrados")
	assert_eq(analyzer.scores[1], 0.8, "último score debe ser 0.8")


func test_normalize_returns_new_fields() -> void:
	var data := {"score": 0.7, "errors": 2, "time": 45.0, "hints_used": 3, "efficiency_rating": 80.0, "objectives_completed": 2, "blocks_count": 10}
	var result := analyzer.normalize(data)

	assert_eq(result.hints_used, 3, "normalize debe incluir hints_used")
	assert_eq(result.efficiency_rating, 80.0, "normalize debe incluir efficiency_rating")
	assert_eq(result.objectives_completed, 2, "normalize debe incluir objectives_completed")
	assert_eq(result.blocks_count, 10, "normalize debe incluir blocks_count")


func test_normalize_handles_missing_new_fields() -> void:
	var result := analyzer.normalize({"score": 0.8, "errors": 1})

	assert_eq(result.hints_used, 0, "hints_used faltante default 0")
	assert_eq(result.efficiency_rating, 0.0, "efficiency_rating faltante default 0.0")
	assert_eq(result.objectives_completed, 0, "objectives_completed faltante default 0")
	assert_eq(result.blocks_count, 0, "blocks_count faltante default 0")


func test_normalize_defaults_missing_score() -> void:
	var result := analyzer.normalize({"errors": 5})
	assert_eq(result.score, 0.0, "score faltante default 0.0")


func test_history_size_limit_50() -> void:
	analyzer.history_size = 3
	analyzer.normalize({"score": 0.6, "errors": 3})
	analyzer.normalize({"score": 0.8, "errors": 1})
	analyzer.normalize({"score": 0.4, "errors": 5})
	analyzer.normalize({"score": 0.9, "errors": 0})
	analyzer.normalize({"score": 0.3, "errors": 7})

	assert_eq(analyzer.scores.size(), 3, "history debe limitarse a 3")
	assert_eq(analyzer.scores[0], 0.4, "el más antiguo debe ser 0.4")
	assert_eq(analyzer.scores[2], 0.3, "el más reciente debe ser 0.3")


func test_record_attempt_trims_at_max() -> void:
	var count := 55
	for i in range(count):
		analyzer.record_attempt(AttemptData.new(0.5 + (i % 3) * 0.1, 1, 30.0))

	assert_eq(analyzer.get_attempt_count(), 50, "record_attempt debe mantener max 50")
	assert_eq(analyzer.get_attempts_history().size(), 50, "attempts_history debe tener 50")


func test_get_long_term_baseline_with_data() -> void:
	var scores := [0.6, 0.8, 0.9]
	for s in scores:
		analyzer.record_attempt(AttemptData.new(s, 1, 30.0))

	var baseline := analyzer.get_long_term_baseline()
	var expected := (0.6 + 0.8 + 0.9) / 3.0
	assert_eq(baseline, expected, "baseline debe ser promedio de scores")


func test_get_long_term_baseline_empty() -> void:
	assert_eq(analyzer.get_long_term_baseline(), 0.0, "baseline sin datos debe ser 0")


func test_get_average_hints_used() -> void:
	for hints in [2, 4, 6]:
		analyzer.record_attempt(AttemptData.new(0.7, 1, 30.0, hints, 50.0))

	var avg := analyzer.get_average_hints_used()
	assert_eq(avg, 4.0, "promedio de hints_used debe ser 4.0")


func test_get_average_hints_used_empty() -> void:
	assert_eq(analyzer.get_average_hints_used(), 0.0, "sin datos debe ser 0")


func test_get_average_efficiency() -> void:
	for eff in [60.0, 80.0, 100.0]:
		analyzer.record_attempt(AttemptData.new(0.7, 1, 30.0, 0, eff))

	var avg := analyzer.get_average_efficiency()
	assert_eq(avg, 80.0, "promedio efficiency debe ser 80.0")


func test_get_average_efficiency_empty() -> void:
	assert_eq(analyzer.get_average_efficiency(), 0.0, "sin datos debe ser 0")


func test_get_total_objectives() -> void:
	for obj in [1, 2, 3]:
		analyzer.record_attempt(AttemptData.new(0.7, 1, 30.0, 0, 0.0, obj))

	assert_eq(analyzer.get_total_objectives(), 6, "total objectives debe ser 6")


func test_get_total_objectives_empty() -> void:
	assert_eq(analyzer.get_total_objectives(), 0, "sin datos debe ser 0")


func test_get_average_errors() -> void:
	analyzer.record_attempt(AttemptData.new(0.7, 2, 30.0))
	analyzer.record_attempt(AttemptData.new(0.8, 4, 30.0))

	var avg := analyzer.get_average_errors()
	assert_eq(avg, 3.0, "promedio de errors debe ser 3.0")


func test_calculate_trend_with_multiple_attempts() -> void:
	analyzer.record_attempt(AttemptData.new(0.5, 5, 60.0))
	analyzer.record_attempt(AttemptData.new(0.8, 1, 30.0))

	var trend := analyzer.calculate_trend()
	assert_eq(trend, 0.3, "trend debe ser 0.3 (mejorando)")


func test_calculate_trend_with_single_attempt() -> void:
	analyzer.record_attempt(AttemptData.new(0.7, 1, 30.0))

	assert_eq(analyzer.calculate_trend(), 0.0, "trend con 1 intento debe ser 0")


func test_reset_attempts_history() -> void:
	analyzer.record_attempt(AttemptData.new(0.7, 1, 30.0))
	analyzer.reset_attempts_history()

	assert_eq(analyzer.get_attempt_count(), 0, "después de reset debe ser 0")
	assert_eq(analyzer.get_attempts_history().size(), 0, "history vacía después de reset")
