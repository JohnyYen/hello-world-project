# test_trend_calculator.gd
# Tests for TrendCalculator with long-term baseline and blend
extends GutTest

const EPSILON := 0.0001

var calc: TrendCalculator


func before_each() -> void:
	calc = TrendCalculator.new()


func _make_history(scores: Array[float]) -> Array[AttemptData]:
	var history: Array[AttemptData] = []
	for s in scores:
		history.append(AttemptData.new(s, 1, 30.0))
	return history


# =============================================================================
# calculate() — existing functionality
# =============================================================================

func test_calculate_simple_returns_zero_with_single_attempt() -> void:
	var history := _make_history([0.7])
	assert_eq(calc.calculate(history, TrendCalculator.TrendMode.SIMPLE), 0.0,
		"1 intento debe dar trend 0")


func test_calculate_simple_positive_trend() -> void:
	var history := _make_history([0.5, 0.9])
	assert_eq(calc.calculate(history, TrendCalculator.TrendMode.SIMPLE), 0.4,
		"mejora de 0.5 a 0.9 debe dar trend 0.4")


func test_calculate_simple_negative_trend() -> void:
	var history := _make_history([0.9, 0.4])
	assert_eq(calc.calculate(history, TrendCalculator.TrendMode.SIMPLE), -0.5,
		"empeora de 0.9 a 0.4 debe dar trend -0.5")


func test_calculate_weighted_with_3_attempts() -> void:
	var history := _make_history([0.5, 0.7, 0.9])
	var trend := calc.calculate(history, TrendCalculator.TrendMode.WEIGHTED)
	assert_ne(trend, 0.0, "WEIGHTED con 3 intentos debe calcular trend")


# =============================================================================
# calculate_long_term_baseline()
# =============================================================================

func test_long_term_baseline_empty() -> void:
	assert_eq(calc.calculate_long_term_baseline([]), 0.0,
		"historial vacío debe dar 0")


func test_long_term_baseline_single_entry() -> void:
	var history := _make_history([0.7])
	var baseline := calc.calculate_long_term_baseline(history)
	assert_eq(baseline, 0.7, "1 entry: baseline = score")


func test_long_term_baseline_three_entries() -> void:
	var history := _make_history([0.6, 0.8, 0.9])
	var baseline := calc.calculate_long_term_baseline(history)
	# weighted: (0.6*1 + 0.8*2 + 0.9*3) / (1+2+3) = (0.6+1.6+2.7)/6 = 4.9/6 = 0.8166...
	var expected := (0.6 * 1.0 + 0.8 * 2.0 + 0.9 * 3.0) / 6.0
	assert_gt(baseline, 0.8, "baseline debe favorecer scores recientes > 0.8")
	assert_eq(baseline, expected, "baseline debe ser %.4f" % expected)


func test_long_term_baseline_five_entries() -> void:
	var history := _make_history([0.5, 0.6, 0.7, 0.8, 0.9])
	var baseline := calc.calculate_long_term_baseline(history)
	var expected := (0.5*1 + 0.6*2 + 0.7*3 + 0.8*4 + 0.9*5) / (1+2+3+4+5)
	assert_eq(baseline, expected, "baseline con 5 entradas ponderado correctamente")


func test_long_term_baseline_50_entries() -> void:
	var scores: Array[float] = []
	for i in range(50):
		scores.append(0.5 + (i % 10) * 0.05)
	var history := _make_history(scores)
	var baseline := calc.calculate_long_term_baseline(history)
	assert_gt(baseline, 0.0, "baseline con 50 entradas debe ser > 0")
	assert_lt(baseline, 1.0, "baseline con 50 entradas debe ser < 1")


# =============================================================================
# blend_scores()
# =============================================================================

func test_blend_scores_with_both_values() -> void:
	var blended := calc.blend_scores(0.7, 0.5)
	var expected := 0.7 * 0.6 + 0.5 * 0.4
	assert_eq(blended, expected, "blend 0.7*0.6 + 0.5*0.4 = %.2f" % expected)


func test_blend_scores_fallback_no_long_term() -> void:
	var blended := calc.blend_scores(0.7, 0.0)
	assert_eq(blended, 0.7, "sin long_term debe usar short_term directamente")


func test_blend_scores_equal_weights() -> void:
	var blended := calc.blend_scores(1.0, 0.0)
	assert_eq(blended, 1.0, "score perfecto sin long_term debe ser 1.0")


func test_blend_scores_extreme_values() -> void:
	var blended := calc.blend_scores(0.0, 0.0)
	assert_eq(blended, 0.0, "ambos 0 debe dar 0")


func test_blend_scores_short_term_dominates() -> void:
	var blended := calc.blend_scores(0.9, 0.1)
	var expected := 0.9 * 0.6 + 0.1 * 0.4
	assert_eq(blended, expected, "short_term 0.9 domina sobre long_term 0.1")


# =============================================================================
# calculate_hybrid_metric()
# =============================================================================

func test_calculate_hybrid_metric_default_weights() -> void:
	var hybrid := calc.calculate_hybrid_metric(0.7, 0.0)
	var expected := 0.7 * 0.7 + 0.5 * 0.3
	assert_eq(hybrid, expected, "hybrid con trend=0: %.4f" % expected)


func test_calculate_hybrid_metric_positive_trend() -> void:
	var hybrid := calc.calculate_hybrid_metric(0.8, 0.5)
	var norm_trend := 0.75
	var expected := 0.8 * 0.7 + norm_trend * 0.3
	assert_eq(hybrid, expected, "hybrid con trend positivo")


func test_calculate_hybrid_metric_negative_trend() -> void:
	var hybrid := calc.calculate_hybrid_metric(0.4, -0.5)
	var norm_trend := 0.25
	var expected := 0.4 * 0.7 + norm_trend * 0.3
	assert_eq(hybrid, expected, "hybrid con trend negativo")


func test_calculate_hybrid_metric_custom_weights() -> void:
	var hybrid := calc.calculate_hybrid_metric(0.9, 0.0, 0.5, 0.5)
	var expected := 0.9 * 0.5 + 0.5 * 0.5
	assert_eq(hybrid, expected, "hybrid con weights 50/50")


# =============================================================================
# get_trend_description()
# =============================================================================

func test_trend_description_improving() -> void:
	assert_eq(calc.get_trend_description(0.2), "Mejorando",
		"trend > 0.1 debe ser Mejorando")


func test_trend_description_worsening() -> void:
	assert_eq(calc.get_trend_description(-0.2), "Empeorando",
		"trend < -0.1 debe ser Empeorando")


func test_trend_description_stable() -> void:
	assert_eq(calc.get_trend_description(0.0), "Estable",
		"trend entre -0.1 y 0.1 debe ser Estable")


# =============================================================================
# set_weighted_mode_weights() / set_max_history_length()
# =============================================================================

func test_set_weighted_mode_weights() -> void:
	calc.set_weighted_mode_weights([1.0, 0.0])
	assert_eq(calc.weighted_mode_weights, [1.0, 0.0],
		"weights deben actualizarse")


func test_set_weighted_mode_weights_empty() -> void:
	var original := calc.weighted_mode_weights.duplicate()
	calc.set_weighted_mode_weights([])
	assert_eq(calc.weighted_mode_weights, original,
		"weights vacíos no deben cambiar")


func test_set_max_history_length() -> void:
	calc.set_max_history_length(10)
	assert_eq(calc.max_history_length, 10,
		"max_history_length debe ser 10")


func test_set_max_history_length_zero() -> void:
	var original := calc.max_history_length
	calc.set_max_history_length(0)
	assert_eq(calc.max_history_length, original,
		"max_history_length 0 no debe cambiar")
