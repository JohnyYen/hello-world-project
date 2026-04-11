extends Control

enum Step {
	INTRO,
	SHOW_GAMEPLAY,
	SHOW_CODE,
	SHOW_RUN_BUTTON,
	FORCE_RUN,
	COMPLETE
}

var step = Step.INTRO

@onready var template = $"."
@onready var viewport = template.get_node("MarginContainer/HBoxContainer/GameArea/SubViewportContainer/SubViewport")
@onready var code_space = template.get_node("MarginContainer/HBoxContainer/CodeArea/CodeSpace")
@onready var hud = template.get_node("MarginContainer/HBoxContainer/Hud")

func _ready():
	_block_all_inputs()
	_start_tutorial()


func _block_all_inputs():
	var blocker = Control.new()
	blocker.name = "InputBlocker"
	blocker.anchor_left = 0
	blocker.anchor_top = 0
	blocker.anchor_right = 1
	blocker.anchor_bottom = 1
	blocker.mouse_filter = Control.MOUSE_FILTER_STOP   # Bloquea CLICS
	blocker.focus_mode = Control.FOCUS_ALL             # Captura teclado

	# Bloquea teclado:
	blocker.set_process_unhandled_input(true)
	blocker.unhandled_input.connect(func(event):
		# Cancelamos TODO el input
		get_viewport().set_input_as_handled()
	)

	add_child(blocker)
	blocker.move_to_front()



func _start_tutorial():
	step = Step.INTRO
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Gameplay_Intro.dialogue"), "start")
	DialogueManager.dialogue_ended.connect(_on_dialogue_finished)


func _on_dialogue_finished():
	match step:
		Step.INTRO:
			step = Step.SHOW_GAMEPLAY
			_show_gameplay_tutorial()
		Step.SHOW_GAMEPLAY:
			step = Step.SHOW_CODE
			_show_code_tutorial()
		Step.SHOW_CODE:
			step = Step.SHOW_RUN_BUTTON
			_show_run_button_tutorial()
		Step.SHOW_RUN_BUTTON:
			step = Step.FORCE_RUN
			_wait_player_to_press_run()
		Step.FORCE_RUN:
			step = Step.COMPLETE
			_finish_tutorial()

func _highlight_node(node):
	pass

func _show_gameplay_tutorial():
	_highlight_node(viewport)
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Gameplay_Gamezone.dialogue"))


func _show_code_tutorial():
	_highlight_node(code_space)
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Gameplay_Codezone.dialogue"))


func _show_run_button_tutorial():
	var run_btn = hud.get_node("RunButton")
	_highlight_node(run_btn)
	DialogueManager.show_dialogue_balloon(load("res://dialogue/Tutorial/Tutorial_Gameplay_Run_Code.dialogue"))


func _wait_player_to_press_run():
	var run_btn = hud.get_node("RunButton")
	run_btn.disabled = false
	run_btn.pressed.connect(_on_run_pressed)
	#DialogueManager.show_dialogue_balloon(load())


func _on_run_pressed():
	#DialogueManager.show_dialogue_balloon("tutorial_gameplay_completed")
	DialogueManager.dialogue_finished.connect(_on_dialogue_finished_complete)


func _on_dialogue_finished_complete():
	_finish_tutorial()	


func _finish_tutorial():
	#_remove_highlights()
	#_unblock_all_inputs()
	_GameState.flags["has_completed_gameplay_tutorial"] = true
	_SaveController.save_game()

	get_tree().change_scene_to_file("res://scenes/pages/maps/global_map.tscn")
