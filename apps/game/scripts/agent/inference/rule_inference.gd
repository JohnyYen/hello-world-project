## Implementation of a rule-based inference engine for the Adaptive Agent
## This class extends BaseInference and implements specific logic for
## deciding actions based on predefined rules. This serves as an example
## of how to extend the BaseInference class for different inference approaches.
extends BaseInference
class_name RuleBasedInference

## Array of rules to be used for decision making
## Each rule contains a condition, an associated action, and a weight
var rules = []

## Initializes the rule-based inference engine by loading the rules
func _init() -> void:
	print("DEBUG: RuleBasedInference initialized")
	_load_rules()

## Loads the rules for the inference engine
## These rules define the conditions under which actions should be taken
## In a real implementation, these might be loaded from a configuration file
func _load_rules() -> void:
	print("DEBUG: Loading rules for RuleBasedInference")
	# Cargar reglas desde un archivo JSON o definirlas aquí para pruebas
	# Cada regla ahora tiene un campo de peso para soportar reglas ponderadas

	# IMPORTANTE: Ahora se considera la magnitud de la desviación del umbral
	# para determinar la acción más adecuada
	rules = [
		{"condition": {"operator": ">", "value": 0.8}, "action": "increase", "weight": 3},  # Alta puntuación
		{"condition": {"operator": "<", "value": 0.5}, "action": "decrease", "weight": 2},  # Baja puntuación
		{"condition": {"operator": "<=", "value": 0.8}, "action": "keep", "weight": 1},    # Puntuación media (0.5 to 0.8)
	]
	print("DEBUG: Rules loaded: ", rules)

## Decides the appropriate action based on the provided performance data
## and the loaded rules. Iterates through the rules and applies the one
## with the highest weight among those whose condition is met.
## Additionally, considers the magnitude of deviation from the threshold
## to determine the most appropriate action.
## Additionally, considers the magnitude of deviation from the threshold
## to determine the most appropriate action.

## @param performance_data: Dictionary containing normalized performance metrics with keys:
##                         - "score": the normalized performance score (0.0-1.0)
##                         - "errors": the number of errors made
##                         - "avg_score": the average performance score
##                         - "time": the time taken (if applicable)
## @return: String representing the action to take ("increase", "decrease", or "keep")
func decide_action(performance_data: Dictionary) -> String:
	print("DEBUG: RuleBasedInference.decide_action called with data: ", performance_data)
	var metric_value = performance_data.get("avg_score", 0)
	print("DEBUG: Using avg_score value: ", metric_value)

	var best_action = "keep"
	var max_weight = 0
	var rules_matched = 0

	var all_rule_evaluations = []

	# Calculate deviation from thresholds to help determine the most appropriate action
	var deviation_from_high_threshold = 0.0
	var deviation_from_low_threshold = 0.0

	if metric_value > 0.8:
		deviation_from_high_threshold = metric_value - 0.8
	elif metric_value < 0.5:
		deviation_from_low_threshold = 0.5 - metric_value


	for rule in rules:
		var condition = rule["condition"]
		var condition_met = false

		var adjusted_weight = rule.get("weight", 1)  # Default weight is 1 if not specified

		# Check for potential conflicts with multiple threshold rules
		if rule == rules[2] and metric_value >= 0.5:  # Third rule (keep) should only apply when 0.5 <= metric_value <= 0.8
			condition_met = (metric_value <= condition["value"] and metric_value >= 0.5)
		else:
			# This is a simple condition
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


		# Apply weight adjustments based on magnitude of deviation from thresholds
		if condition_met:
			if rule["action"] == "increase" and deviation_from_high_threshold > 0:
				# Increase weight based on how much above the threshold the score is
				adjusted_weight += deviation_from_high_threshold * 10  # Amplify the effect
			elif rule["action"] == "decrease" and deviation_from_low_threshold > 0:
				# Increase weight based on how much below the threshold the score is
				adjusted_weight += deviation_from_low_threshold * 10  # Amplify the effect

		# Add detailed logging for each rule evaluation
		var rule_evaluation = {
			"condition": condition,
			"metric_value": metric_value,
			"condition_met": condition_met,
			"original_weight": rule.get("weight", 1),
			"adjusted_weight": adjusted_weight,
			"action": rule["action"]
		}
		all_rule_evaluations.append(rule_evaluation)

		print("DEBUG: Checking rule - condition: ", condition, " | metric_value: ", metric_value,
			" | condition_met: ", condition_met, " | original_weight: ", rule.get("weight", 1),
			" | adjusted_weight: ", adjusted_weight, " | action: ", rule["action"])

		if condition_met:
			rules_matched += 1
			print("DEBUG: Rule matched with adjusted weight: ", adjusted_weight, ", action: ", rule["action"])

			# Update the best action if this rule has a higher adjusted weight
			if adjusted_weight > max_weight:
				max_weight = adjusted_weight
				best_action = rule["action"]
				print("DEBUG: New best action selected: ", best_action, " with adjusted weight: ", max_weight)

	print("DEBUG: Total rules matched: ", rules_matched)

	# Print all rule evaluations for debugging
	print("DEBUG: All rule evaluations - ")
	for eval in all_rule_evaluations:
		print("DEBUG:   - Condition: ", eval["condition"], " | Met: ", eval["condition_met"],
			" | Original Weight: ", eval["original_weight"], " | Adjusted Weight: ", eval["adjusted_weight"],
			" | Action: ", eval["action"])

	if rules_matched > 0:
		print("DEBUG: Returning best action based on adjusted weight: ", best_action)
		return best_action
	else:
		print("DEBUG: No rules matched, returning default action: keep")
		return "keep"