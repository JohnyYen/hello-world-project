# game_session.gd
# Data class representing the cached game session state
class_name GameSession

var game_id: String = ""
var instance_id: String = ""
var student_id: String = ""
var created_at: String = ""
var updated_at: String = ""


func _init(p_game_id: String = "", p_instance_id: String = "", p_student_id: String = "") -> void:
	game_id = p_game_id
	instance_id = p_instance_id
	student_id = p_student_id
	created_at = Time.get_datetime_string_from_system(true)
	updated_at = created_at


## Returns true if this session has the minimum required data
func is_valid() -> bool:
	return game_id != "" and instance_id != ""


## Serializes to a Dictionary for debugging/logging
func to_dict() -> Dictionary:
	return {
		"game_id": game_id,
		"instance_id": instance_id,
		"student_id": student_id,
		"created_at": created_at,
		"updated_at": updated_at,
	}
