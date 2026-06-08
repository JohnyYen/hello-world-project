extends Control

func _ready() -> void:
	if Env.ENVIORMENT == "dev":
		_GameState.player_data = {
			"name": "Pedro"
		}
	if not _GameState.flags.get("has_first_time_cafeteria", false):
		print("Hola soy yo otra vez")
		_welcome_to_cafeteria()


func _welcome_to_cafeteria():
	_GameState.flags["has_first_time_cafeteria"] = true
	DialogueManager.show_dialogue_balloon(load("res://dialogue/C01/C01_E05_Primera_Vez_Cafeteria.dialogue"))
	#_GameState.start_dialogue("res://dialogue/C01/C01_E05_Primera_Vez_Cafeteria.dialogue", "res://scenes/pages/maps/faculty/rooms/cafeteria.tscn")
