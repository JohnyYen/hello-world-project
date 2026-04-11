## The AdaptiveAgent class monitors student performance and adjusts
## difficulty levels in the educational game accordingly.
## It uses a performance analyzer to process raw data and an inference
## engine to decide on appropriate actions for difficulty modification.
class_name AdaptiveAgent

## Emitted when the agent decides on an action to adjust difficulty
## @param action: String representing the action taken ("increase", "decrease", or "keep")
## @param new_difficulty: Float representing the new difficulty level after the action
signal action_decided(action: String, new_difficulty: float)

## The inference engine used to determine what action to take based on performance data
var inference_engine: BaseInference

## The performance analyzer that normalizes raw performance data
var analyzer: PerformanceAnalyzer

## Current difficulty level, ranging from min_difficulty to max_difficulty
var difficulty := 1.0

## Minimum allowed difficulty level
var min_difficulty := 0.5

## Maximum allowed difficulty level  
var max_difficulty := 2.0

## The amount by which difficulty changes when increase/decrease actions are taken
var delta := 0.1

## Initializes the adaptive agent with required components
func _init() -> void:
	print("DEBUG: AdaptiveAgent initialized")
	inference_engine = RuleBasedInference.new();
	analyzer = PerformanceAnalyzer.new()
	print("DEBUG: AdaptiveAgent components created - inference_engine: ", inference_engine, ", analyzer: ", analyzer)

## Analyzes raw performance data and decides on an action to adjust difficulty
## @param raw_data: Dictionary containing raw performance metrics with keys:
##                  - "score": float between 0.0 and 1.0 representing performance
##                  - "errors": integer number of errors made
##                  - "time": float representing time taken (optional)
func analyze_and_decide(raw_data : Dictionary) -> void:
	print("DEBUG: AdaptiveAgent.analyze_and_decide called with raw_data: ", raw_data)
	# Normalize the raw performance data using the analyzer
	var processed_data = analyzer.normalize(raw_data);
	print("DEBUG: Normalized data to: ", processed_data)
	# Determine the appropriate action based on the processed data
	var action = inference_engine.decide_action(processed_data);
	print("DEBUG: Inference engine decided action: ", action)
	# Apply the decided action to adjust difficulty
	_apply_action(action);

## Applies the specified action to adjust the difficulty level
## @param action: String representing the action to take ("increase", "decrease", or "keep")
func _apply_action(action: String) -> void:
	print("DEBUG: Applying action: ", action, " to current difficulty: ", difficulty)
	var old_difficulty = difficulty
	# Apply the action to adjust difficulty accordingly
	match action:
		"increase":
			# Increase difficulty, but ensure it doesn't exceed the maximum
			difficulty = min(difficulty + delta, max_difficulty)
			print("DEBUG: Increased difficulty from ", old_difficulty, " to ", difficulty)
		"decrease":
			# Decrease difficulty, but ensure it doesn't go below the minimum
			difficulty = max(difficulty - delta, min_difficulty)
			print("DEBUG: Decreased difficulty from ", old_difficulty, " to ", difficulty)
		"keep":
			# No change to difficulty
			print("DEBUG: Kept difficulty at ", difficulty)
			pass
		_:
			# Handle unexpected actions with a warning
			push_warning("Unknown action: %s" % action)
			print("DEBUG: Unknown action received: ", action)
	
	# Ensure difficulty is clamped between min and max values as an extra safety measure
	difficulty = clamp(difficulty, min_difficulty, max_difficulty)
	print("DEBUG: Final difficulty after clamping: ", difficulty, " (was: ", old_difficulty, ")")
	
	# Emit the signal to notify other parts of the system about the decision
	emit_signal("action_decided", action, difficulty)
	# Log the decision for debugging purposes
	print("Agent decided action: %s, new difficulty: %f" % [action, difficulty])
