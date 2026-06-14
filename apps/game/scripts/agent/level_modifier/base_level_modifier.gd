class_name BaseLevelModifier


var segment_id : int 
var raw_data := {}
var level_segment := {}
var original_config := {}
var modified_config := {}

var repo : LevelRepository

func _init() -> void:
	repo = LevelRepository.new()

func set_level_segment(segment: Dictionary):
	level_segment = segment
	original_config = segment.get("configuration", {}).duplicate(true)
	modified_config = original_config.duplicate(true)

func get_config(level_id : int, segment_id : int) -> Dictionary:
	var repo = LevelRepository.new()
	var config = repo.get_segment_json(level_id, segment_id)
	return config

## Modify level configuration based on action state and difficulty.
## @param state: String - Action to apply. One of:
##   "decrease_major" - Much easier (strong decrease)
##   "decrease_minor" - Slightly easier (light decrease)
##   "keep" - Maintain current difficulty
##   "increase_minor" - Slightly harder (light increase)
##   "increase_major" - Much harder (strong increase)
## @param difficulty: float - Current difficulty value
## @return: Dictionary - Modified level configuration
func modify_level(state: String, difficulty: float) -> Dictionary:
	push_error("METHOD_NOT_IMPLEMENTED")
	return {}


func apply_modifications():
	_update_segment_configurations(level_segment, modified_config)


func _update_segment_configurations(segment: Dictionary, new_config: Dictionary):
	segment["configuration"] = new_config


# ----------------------------------------------------
# Helper: ajuste random entre min y max
# ----------------------------------------------------
func _rand_adjust(min_value: int, max_value: int) -> int:
	return randi_range(min_value, max_value)
