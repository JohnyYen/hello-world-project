## Abstract base class for level difficulty modifiers.
## Defines HOW difficulty adjustments are applied to level configurations.
##
## Subclasses MUST implement modify_level().
## Examples:
##   - LevelOneModifier: Cafeteria-specific adjustments (current game)
##   - ResourceModifier: More/fewer resources available
##   - TimeModifier: More/less time pressure
##   - CompositeModifier: Combine multiple modifiers
class_name BaseLevelModifier


## Emitted when a level modification is applied
signal level_modified(action: String, modified_config: Dictionary)


## The level repository
var repo: LevelRepository

## Current segment data
var level_segment: Dictionary = {}

## Original (unmodified) configuration
var original_config: Dictionary = {}

## Modified configuration
var modified_config: Dictionary = {}


func _init() -> void:
	repo = LevelRepository.new()


## Set the current segment data for modification.
func set_level_segment(segment: Dictionary) -> void:
	level_segment = segment
	original_config = segment.get("configuration", {}).duplicate(true)
	modified_config = original_config.duplicate(true)


## Get the raw config from repository for a given level and segment.
func get_config(level_id: int, segment_id: int) -> Dictionary:
	var level_repo = LevelRepository.new()
	var config = level_repo.get_segment_json(level_id, segment_id)
	return config


## Modify the level based on the decided action and difficulty.
## MUST be overridden by subclasses.
## @param action: "increase", "decrease", or "keep"
## @param difficulty: Current difficulty value (0.5-2.0)
func modify_level(action: String, difficulty: float) -> void:
	push_error("BaseLevelModifier.modify_level() is abstract. Subclasses MUST implement this method.")


## Apply the modified configuration back to the segment.
func apply_modifications() -> void:
	_update_segment_configurations(level_segment, modified_config)


## Update segment configuration with new values.
func _update_segment_configurations(segment: Dictionary, new_config: Dictionary) -> void:
	segment["configuration"] = new_config


## Helper: Random adjustment between min and max.
func _rand_adjust(min_value: int, max_value: int) -> int:
	return randi_range(min_value, max_value)


## Helper: Clamp a value between min and max.
func _clamp_value(value: float, min_val: float, max_val: float) -> float:
	return clamp(value, min_val, max_val)
