## Implementation of a rule-based inference engine for the Adaptive Agent
## This class extends BaseInference and implements specific logic for
## deciding actions based on predefined rules with support for hybrid metrics
## (combining score and trend).
extends BaseInference
class_name RuleBasedInference

## Array of rules to be used for decision making
## Each rule contains a condition, an associated action, and a weight
var rules = []

## TrendCalculator para calcular métricas híbridas
var trend_calculator: TrendCalculator

## Pesos para la métrica híbrida: score y tendencia
var score_weight: float = 0.7
var trend_weight: float = 0.3

## Initializes the rule-based inference engine by loading the rules
func _init() -> void:
	_load_rules()
	trend_calculator = TrendCalculator.new()

## Loads the rules for the inference engine
## These rules define the conditions under which actions should be taken
func _load_rules() -> void:
	rules = [
		{"condition": {"operator": ">", "value": 0.8}, "action": "increase", "weight": 3},
		{"condition": {"operator": "<", "value": 0.5}, "action": "decrease", "weight": 2},
		{"condition": {"operator": "<=", "value": 0.8}, "action": "keep", "weight": 1},
	]

## Decides the appropriate action based on the provided performance data
## and the loaded rules. Evaluates rules using hybrid metric (70% score + 30% trend).
##
## @param performance_data: Dictionary containing normalized performance metrics with keys:
##                         - "score": the normalized performance score (0.0-1.0)
##                         - "avg_score": the average performance score
##                         - "trend": the trend value (-1.0 to 1.0), optional
##                         - "errors": the number of errors made
##                         - "time": the time taken (if applicable)
## @return: String representing the action to take ("increase", "decrease", or "keep")
func decide_action(performance_data: Dictionary) -> String:
	var current_score = performance_data.get("avg_score", 0.0)
	var trend = performance_data.get("trend", 0.0)
	
	# Calcular métrica híbrida: 70% score + 30% tendencia
	var metric_value = trend_calculator.calculate_hybrid_metric(
		current_score, 
		trend, 
		score_weight, 
		trend_weight
	)
	
	var best_action = "keep"
	var max_weight = 0
	
	# Calcular desviación del umbral para ajuste de peso
	var deviation_from_high_threshold = 0.0
	var deviation_from_low_threshold = 0.0
	
	if metric_value > 0.8:
		deviation_from_high_threshold = metric_value - 0.8
	elif metric_value < 0.5:
		deviation_from_low_threshold = 0.5 - metric_value
	
	for rule in rules:
		var condition = rule["condition"]
		var condition_met = false
		var adjusted_weight = rule.get("weight", 1)
		
		# Evaluar condición
		if rule == rules[2] and metric_value >= 0.5:
			condition_met = (metric_value <= condition["value"] and metric_value >= 0.5)
		else:
			match condition["operator"]:
				"<":
					condition_met = metric_value < condition["value"]
				">":
					condition_met = metric_value > condition["value"]
				"<=":
					condition_met = metric_value <= condition["value"]
				">=":
					condition_met = metric_value >= condition["value"]
				"==":
					condition_met = metric_value == condition["value"]
		
		# Ajustar peso basado en magnitud de desviación
		if condition_met:
			if rule["action"] == "increase" and deviation_from_high_threshold > 0:
				adjusted_weight += deviation_from_high_threshold * 10
			elif rule["action"] == "decrease" and deviation_from_low_threshold > 0:
				adjusted_weight += deviation_from_low_threshold * 10
			
			# Actualizar mejor acción si tiene mayor peso
			if adjusted_weight > max_weight:
				max_weight = adjusted_weight
				best_action = rule["action"]
	
	print("[RuleBasedInference] score=%.2f, trend=%.2f, hybrid_metric=%.2f, action=%s" % [
		current_score, trend, metric_value, best_action
	])
	
	return best_action

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
