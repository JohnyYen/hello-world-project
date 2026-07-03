## Implementation of a graduated multi-threshold inference engine
## This class extends BaseInference and implements decision logic using
## multiple threshold levels for granular difficulty adjustment.
## Replaces the previous 3-action rule system with 5-action graduated inference.
extends BaseInference
class_name RuleBasedInference

## Umbrales para decisión multi-nivel
const THRESHOLD_MAJOR_LOW := 0.3
const THRESHOLD_MINOR_LOW := 0.5
const THRESHOLD_KEEP := 0.8
const THRESHOLD_MINOR_HIGH := 0.9

## Deltas asociados a cada acción (usados por LevelModifier)
const DELTA_DECREASE_MAJOR := -0.2
const DELTA_DECREASE_MINOR := -0.1
const DELTA_KEEP := 0.0
const DELTA_INCREASE_MINOR := 0.1
const DELTA_INCREASE_MAJOR := 0.2

## TrendCalculator para calcular métricas híbridas
var trend_calculator: TrendCalculator

## Pesos para la métrica híbrida: score y tendencia
var score_weight: float = 0.7
var trend_weight: float = 0.3

## Initializes the inference engine
func _init() -> void:
	trend_calculator = TrendCalculator.new()

## Aplica lógica multi-umbral para determinar la acción graduada
## @param hybrid_metric: float entre 0.0 y 1.0
## @return String: acción ("decrease_major", "decrease_minor", "keep", "increase_minor", "increase_major")
func _calculate_multi_threshold(hybrid_metric: float) -> String:
	var action: String
	if hybrid_metric < THRESHOLD_MAJOR_LOW:
		action = "decrease_major"
	elif hybrid_metric < THRESHOLD_MINOR_LOW:
		action = "decrease_minor"
	elif hybrid_metric <= THRESHOLD_KEEP:
		action = "keep"
	elif hybrid_metric <= THRESHOLD_MINOR_HIGH:
		action = "increase_minor"
	else:
		action = "increase_major"
	print("[ADAPT_TRACE] multi_threshold: hybrid=%.4f, thresholds=[%.1f, %.1f, %.1f, %.1f] → action='%s'" % [
		hybrid_metric, THRESHOLD_MAJOR_LOW, THRESHOLD_MINOR_LOW, THRESHOLD_KEEP, THRESHOLD_MINOR_HIGH, action
	])
	return action

## Decides the appropriate action based on the provided performance data
## using graduated multi-threshold logic.
##
## @param performance_data: Dictionary with keys:
##                         - "score": normalized score (0.0-1.0)
##                         - "trend": trend value (-1.0 to 1.0)
##                         - "hints_used": number of hints used (optional)
##                         - "efficiency_rating": efficiency rating (optional)
##                         - "objectives_completed": objectives completed (optional)
## @return: String: "decrease_major", "decrease_minor", "keep", "increase_minor", "increase_major"
func decide_action(performance_data: Dictionary) -> String:
	var current_score = performance_data.get("score", 0.0)
	var trend = performance_data.get("trend", 0.0)

	var hybrid_metric = trend_calculator.calculate_hybrid_metric(
		current_score,
		trend,
		score_weight,
		trend_weight
	)

	var action = _calculate_multi_threshold(hybrid_metric)

	print("[RuleBasedInference] score=%.2f, trend=%.2f, hybrid_metric=%.2f, action=%s" % [
		current_score, trend, hybrid_metric, action
	])

	return action

## Configura los pesos de la métrica híbrida
## @param new_score_weight: Peso para el score (0.0 a 1.0)
## @param new_trend_weight: Peso para la tendencia (0.0 a 1.0)
func set_hybrid_weights(new_score_weight: float, new_trend_weight: float) -> void:
	var total = new_score_weight + new_trend_weight
	if total <= 0.0:
		push_warning("RuleBasedInference: Pesos inválidos, no se actualizan")
		return
	
	score_weight = new_score_weight / total
	trend_weight = new_trend_weight / total
