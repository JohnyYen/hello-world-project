## Represents the player's solution in a problem-solving scenario.
## This is a generic data container that works with ANY interaction mechanism.
class_name SolutionData

## Raw solution data (type-agnostic)
var _data: Dictionary = {}

## Metadata about the solution
var metadata: Dictionary = {}

## Timestamp when the solution was created
var timestamp: float = 0.0

## Number of attempts made
var attempt_count: int = 1


## Store a value in the solution data
func set_data(key: String, value) -> void:
	_data[key] = value


## Retrieve a value from the solution data
func get_data(key: String, default = null):
	if _data.has(key):
		return _data[key]
	return default


## Check if a key exists in the solution data
func has(key: String) -> bool:
	return _data.has(key)


## Get all solution data as a dictionary
func to_dict() -> Dictionary:
	return {
		"data": _data.duplicate(true),
		"metadata": metadata.duplicate(true),
		"timestamp": timestamp,
		"attempt_count": attempt_count
	}


## Load solution data from a dictionary
func from_dict(dict: Dictionary) -> void:
	if dict.has("data"):
		_data = dict["data"].duplicate(true)
	if dict.has("metadata"):
		metadata = dict["metadata"].duplicate(true)
	if dict.has("timestamp"):
		timestamp = dict["timestamp"]
	if dict.has("attempt_count"):
		attempt_count = dict["attempt_count"]


## Get a string representation of the solution
func _to_string() -> String:
	return "SolutionData<keys=%s, attempt=%d>" % [_data.keys(), attempt_count]
