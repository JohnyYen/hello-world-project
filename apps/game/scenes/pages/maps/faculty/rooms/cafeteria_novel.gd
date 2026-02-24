extends Control

func _ready() -> void:
	if not _GameState.flags.get("has_first_time_cafeteria", false):
		_welcome_to_cafeteria()
		
func _welcome_to_cafeteria():
	_GameState.start_dialogue("res://dialogue/C01/C01_E05_Primera_Vez_Cafeteria.dialogue", "res://scenes/pages/maps/faculty/rooms/cafeteria.tscn")
