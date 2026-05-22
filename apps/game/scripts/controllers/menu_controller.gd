extends Control

@onready var panel = $Panel
@onready var main_button = $Panel_Button
@onready var art_options = $"Panel/Art Options"
@onready var language_options = $"Panel/Lang Options"
@onready var audio = $Audio

# Called when the node enters the scene tree for the first time.
func _ready():
	panel.visible = false
	main_button.visible = true
	
	if _GameConfig.jwt == "" or _GameConfig.user == {}:
		print(_GameConfig.jwt)
		print(_GameConfig.user)
		_go_to_login()


func _go_to_login():
	
	await get_tree().process_frame
	
	await AlertComponent.show_alert(
		"No hay una sesión activa. Por favor inicia sesión para continuar.",
		"warning",
		3.0
	)
	
	print("aaadasdas")
	LoadingScreen.change_scene("res://scenes/pages/login.tscn")
	
func _on_play_pressed():
	print("[MainMenu] Play pressed")
	_Util.fade_out_music(audio, 0.4)
	
	var new_player = _GameState.player_data.get("name", "") == ""
	if not new_player:
		get_tree().change_scene_to_file("res://scenes/pages/maps/dormitory/player_room.tscn")
	else:
		get_tree().change_scene_to_file("res://scenes/pages/custom_character_page.tscn")
		#var scenes = [
			#{"path": "res://dialogue/C00/C00_E02_Bienvenida_Orqui.dialogue"},
			#{"path": "res://dialogue/C00/C00_E03_Teatro_Facultad.dialogue"},
			#{"path": "res://dialogue/C00/C00_E04_Tour_Facultad.dialogue" },
			#{"path": "res://dialogue/C00/C00_E05_Llegada_Dormitorio.dialogue", "next_scene": "res://scenes/pages/maps/dormitory/player_room.tscn"}
		#]
		#_GameState.start_dialogue("res://dialogue/C00/C00_E01_Entrada_Facultad.dialogue")
	#var target_scene := (
		#"res://scenes/pages/custom_character_page.tscn"
		#if new_player
		#else "res://scenes/pages/maps/dormitory/player_room.tscn"
	#)
	
	#_SaveController.save_game()
	#get_tree().change_scene_to_file(target_scene)



func _on_option_pressed():
	panel.visible = true
	main_button.visible = false

func _on_quit_pressed():
	get_tree().quit() 


func _on_back_pressed():
	_ready()


func _on_music_slider_value_changed(value: float):
	_GameConfig.set_volume("music", value)


func _on_sfx_slider_value_changed(value: float):
	_GameConfig.set_volume("sfx", value)



func _on_toogle_fullscreen_toggled(toggled_on: bool) -> void:
	_GameConfig.set_screen(toggled_on)


func _on_art_style_item_selected(index: int) -> void:
	_GameConfig.set_art_style(art_options.get_item_text(index))

func _on_lang_options_item_selected(index: int) -> void:
	_GameConfig.set_language(language_options.get_item_text(index))


func _on_gallery_pressed() -> void:
	pass # Replace with function body.
