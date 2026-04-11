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

func modify_level(state: String, difficulty : float):
	push_error("METHOD_NOT_IMPLEMENTED")


func apply_modifications():
	_update_segment_configurations(level_segment, modified_config)


func _update_segment_configurations(segment: Dictionary, new_config: Dictionary):
	segment["configuration"] = new_config


# ----------------------------------------------------
# Helper: ajuste random entre min y max
# ----------------------------------------------------
func _rand_adjust(min_value: int, max_value: int) -> int:
	return randi_range(min_value, max_value)
