class_name BaseLevelModifier


var segment_id : int 
var raw_data := {}
var level_segment := {}
var original_config := {}
var adaptation_state := {}
var merged_config := {}
var modified_config := {}

var repo : LevelRepository

func _init() -> void:
	repo = LevelRepository.new()
	print("[BaseLevelModifier] Inicializado con LevelRepository")


# ----------------------------------------------------
# Helper: resuelve placeholders {variable} en templates
# ----------------------------------------------------
static func resolve_template(template: String, ctx: Dictionary) -> String:
	var result: String = template
	for key in ctx:
		result = result.replace("{%s}" % key, str(ctx[key]))
	result = result.replace("{", "").replace("}", "")
	return result


func set_level_segment(segment: Dictionary):
	level_segment = segment
	original_config = segment.get("configuration", {}).duplicate(true)
	adaptation_state = segment.get("adaptation_state", {})
	merged_config = _merge_config(original_config, adaptation_state)
	modified_config = merged_config.duplicate(true)
	print("[BASE_MODIFIER] Segmento asignado - segment_id=%d, has_adaptation=%s, config_keys=%s" % [
		segment.get("id", 0),
		"true" if not adaptation_state.is_empty() else "false",
		original_config.keys()
	])

func get_config(level_id : int, segment_id : int) -> Dictionary:
	var repo = LevelRepository.new()
	var config = repo.get_segment_json(level_id, segment_id)
	print("[BaseLevelModifier] Config obtenida para level=%d, segment=%d: %s" % [level_id, segment_id, config])
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
	print("[BaseLevelModifier] modify_level llamado con state='%s', difficulty=%.2f - MÉTODO BASE, debe ser sobreescrito" % [state, difficulty])
	push_error("METHOD_NOT_IMPLEMENTED")
	return {}


func apply_modifications():
	print("[ADAPT_TRACE] === apply_modifications INICIO ===")
	var cfg = modified_config
	var students = cfg.get("initial_state", {}).get("student_queue", [])
	var exec_rules = cfg.get("execution_rules", {})
	print("[ADAPT_TRACE] segment_id=%d, students=%d, max_blocks=%d, time_limit=%d, hints=%d" % [
		segment_id, students.size(),
		exec_rules.get("max_blocks", 0),
		exec_rules.get("time_limit", 0),
		cfg.get("feedback_messages", {}).get("hints", []).size()
	])
	var level_id = level_segment.get("level_id", 1)
	var result := repo.update_adaptation_state(level_id, segment_id, modified_config)
	if result:
		print("[ADAPT_TRACE] update_adaptation_state EXITOSO para level=%d, segment=%d" % [level_id, segment_id])
	else:
		push_error("[ADAPT_TRACE] update_adaptation_state FALLÓ para level=%d, segment=%d" % [level_id, segment_id])


func reset_to_seed():
	print("[BaseLevelModifier] Restableciendo configuración a seed")
	var level_id = level_segment.get("level_id", 1)
	repo.reset_adaptation_state(level_id, segment_id)
	print("[BaseLevelModifier] Seed restablecido exitosamente")


# ----------------------------------------------------
# Helper: ajuste random entre min y max
# ----------------------------------------------------
func _rand_adjust(min_value: int, max_value: int) -> int:
	return randi_range(min_value, max_value)


static func _merge_config(seed: Dictionary, diff: Dictionary) -> Dictionary:
	var merged = seed.duplicate(true)
	for key in diff:
		var val = diff[key]
		if typeof(val) in [TYPE_DICTIONARY, TYPE_ARRAY]:
			merged[key] = val.duplicate(true)
		else:
			merged[key] = val
	return merged
