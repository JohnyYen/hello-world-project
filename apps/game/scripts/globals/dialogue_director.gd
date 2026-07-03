class_name DialogueDirector
extends Node

var hint_fade_delay := 4

@onready var balloon = get_parent()
@onready var dialogue_label: DialogueLabel = %DialogueLabel
@onready var responses_menu: DialogueResponsesMenu = %ResponsesMenu
@onready var skip_hint := $"../SkipHint"
@onready var audio_music :=  $"../AudioMusic"
@onready var audio_sfx := $"../AudioSFX"

func _ready() -> void:
	_update_ui_hint_label()

	if skip_hint and hint_fade_delay > 0:
		await get_tree().create_timer(hint_fade_delay).timeout
		var tween := create_tween()
		tween.tween_property(skip_hint, "modulate:a", 0.0, 1.0)

func _update_ui_hint_label():
	if not skip_hint:
		push_warning("SkipHint node not found!")
		return

	var os_name := OS.get_name()
	var is_mobile := os_name in ["Android", "iOS"]

	if is_mobile:
		skip_hint.text = "Tocá para continuar  ·  Deslizá para saltar"
	else:
		skip_hint.text = "[ESC] Saltar  |  [Z] Siguiente  |  [A] Texto rápido"
	

func _get_key_name(key: String) -> String:
	var events := InputMap.action_get_events(key)
	
	if events.is_empty():
		return "?"
	
	var event := events[0]
	if event is InputEventKey:
		return "[%s]" % event.as_text_keycode().replace("(Unset)", "?")
	elif event is InputEventMouseButton:
		match event.button_index:
			MOUSE_BUTTON_LEFT:
				return "[LMB]"
			MOUSE_BUTTON_RIGHT:
				return "[RMB]"
			_:
				return "[?]"
	return "[?]"


func _input(event: InputEvent) -> void:
	# A: Saltar animación de escritura (mostrar texto instantáneo)
	if event.is_action_pressed("dialogue_skip_typing"):
		print("Estoy saltando el dialogo")
		if dialogue_label.is_typing:
			dialogue_label.skip_typing()
		get_viewport().set_input_as_handled()
		return
	
	# Z o Click derecho: Avanzar a la siguiente línea
	if event.is_action_pressed("dialogue_next_line"):
		print("Siguiente Linea del dialogo")
		if responses_menu.visible and responses_menu.get_child_count() > 0:
			return

		if dialogue_label.is_typing:
			dialogue_label.skip_typing()
		else:
			if balloon.dialogue_line and balloon.dialogue_line.next_id:
				balloon.next(balloon.dialogue_line.next_id)
		get_viewport().set_input_as_handled()
		return
	
	# ESC: Saltarse TODO el diálogo e ir a la siguiente escena
	if event.is_action_pressed("dialogue_skip_scene"):
		print("Saltarse todo el dialogo")
		_skip_to_next_scene()
		get_viewport().set_input_as_handled()
		
func _skip_to_next_scene() -> void:
	if audio_music.is_playing():
		audio_music.stop()
	if audio_sfx.is_playing():
		audio_sfx.stop()

	if balloon:
		balloon.queue_free()

	_GameState.dialogue_flow.force_finish()
