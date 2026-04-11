## Represents the result of executing a player's solution.
## Contains step-by-step execution data and final state.
class_name ExecutionContext

## Whether the execution completed without errors
var completed: bool = false

## Steps executed during the run: [{name, result, data}]
var steps: Array = []

## Final state after execution
var final_state: Dictionary = {}

## Any errors that occurred during execution
var errors: Array = []

## Execution time in seconds
var execution_time: float = 0.0

## Score of the execution (0.0 to 1.0)
var score: float = 0.0


## Add an execution step
func add_step(name: String, result, data = null) -> void:
	steps.append({
		"name": name,
		"result": result,
		"data": data
	})


## Get the result of a specific step by name
func get_step_result(name: String):
	for step in steps:
		if step["name"] == name:
			return step.get("result")
	return null


## Set a value in the final state
func set(key: String, value) -> void:
	final_state[key] = value


## Get a value from the final state
func get_state(key: String, default = null):
	if final_state.has(key):
		return final_state[key]
	return default


## Add an error to the execution result
func add_error(error_msg: String) -> void:
	errors.append(error_msg)


## Check if any errors occurred
func has_errors() -> bool:
	return errors.size() > 0


## Convert to dictionary for serialization
func to_dict() -> Dictionary:
	return {
		"completed": completed,
		"steps": steps.duplicate(true),
		"final_state": final_state.duplicate(true),
		"errors": errors.duplicate(true),
		"execution_time": execution_time,
		"score": score
	}


func _to_string() -> String:
	return "ExecutionContext<completed=%s, steps=%d, errors=%d>" % [completed, steps.size(), errors.size()]
