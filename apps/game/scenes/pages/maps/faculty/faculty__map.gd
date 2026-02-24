extends Control

func _ready() -> void:
	if not _GameState.flags.get("has_first_time_faculty", false):
		_welcome_in_faculty()
		

func _welcome_in_faculty():
	_GameState.start_dialogue("res://dialogue/C01/C01_E03_Llegada_Facultad.dialogue", "res://scenes/pages/maps/faculty/faculty_ map.tscn")
