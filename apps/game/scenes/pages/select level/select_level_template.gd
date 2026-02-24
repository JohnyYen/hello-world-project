extends Control


@onready var level_title := $LabelContainer/Title
@onready var background = $Background
@onready var buttons_panel = $LevelContainer
@onready var back_button = $BackContainer/Back
@onready var confirmation_panel = $ConfirmationPanel
@onready var level_panel = $LevelPanel

@export_file("*.tscn") var previous_scene
@export_file("*.tscn") var gameplay_scene : String

func _ready() -> void:
	_set_select_level()
	back_button.pressed.connect(_on_back_pressed)
	var i : int = 0
	for btn in buttons_panel.get_children():
		btn.get_child(0).pressed.connect(_on_play_level.bind(i))
		i += 1 

func _on_play_level(segment_id : int):
	var packed : PackedScene = load(gameplay_scene)

	if packed.instantiate() is TemplateLevel:
		if segment_id == 0:
			DialogueManager.show_dialogue_balloon(load("res://dialogue/C01/C01_E04_Primera_Clase.dialogue"), "start")
		elif segment_id > 0 and segment_id <= 5:
			var level_instance : TemplateLevel = packed.instantiate()
			level_instance.segment_id = segment_id
			get_tree().root.add_child(level_instance)
			get_tree().current_scene.queue_free()
	else:
		print("De pinga")

func _set_select_level():
	pass


func _on_back_pressed() -> void:
	confirmation_panel.visible = 1
	back_button.visible = 0
	



func _on_yes_pressed() -> void:
	get_tree().change_scene_to_file(previous_scene)
	


func _on_no_pressed() -> void:
	confirmation_panel.visible = 0
	back_button.visible = 1
