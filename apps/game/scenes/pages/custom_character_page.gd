extends CanvasLayer

@export var male_node: Control
@export var male_node_panel: PanelContainer
@export var female_node: Control
@export var female_node_panel: PanelContainer
@export var name_input : LineEdit
@export var continue_button: Button
@export var label: Label
@export var edit_container: PanelContainer

var player_data = {}
var _gender_selected := false

func _ready() -> void:
	var ballon = DialogueManager.show_dialogue_balloon(load("res://dialogue/start.dialogue"))
	edit_container.visible = false

func _on_character_male_pressed() -> void:
	if _gender_selected:
		return
	_gender_selected = true

	var tween = create_tween()

	var child_00 = male_node.get_child(0).get_child(0) if male_node.get_child_count() > 0 and male_node.get_child(0).get_child_count() > 0 else null
	var child_2 = male_node.get_child(2) if male_node.get_child_count() > 2 else null

	if child_00:
		child_00.queue_free()
	if child_2:
		child_2.queue_free()

	male_node_panel.modulate.a = 0

	tween.tween_property(female_node.get_parent(), "modulate:a", 0.0, 0.5)

	tween.finished.connect(func ():
		label.modulate.a = 0
		label.text = "¿Cómo te llamas?"
		edit_container.modulate.a = 0
		edit_container.visible = true

		var tween2 = create_tween()
		tween2.tween_property(label, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(name_input, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(continue_button, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(edit_container, "modulate:a", 1.0, 0.5)
	)

	player_data["gender"] = "male"
	name_input.focus_mode = Control.FocusMode.FOCUS_ALL


func _on_character_female_pressed() -> void:
	if _gender_selected:
		return
	_gender_selected = true

	var tween = create_tween()

	var child_00 = female_node.get_child(0).get_child(0) if female_node.get_child_count() > 0 and female_node.get_child(0).get_child_count() > 0 else null
	var child_2 = female_node.get_child(2) if female_node.get_child_count() > 2 else null

	if child_00:
		child_00.queue_free()
	if child_2:
		child_2.queue_free()

	female_node_panel.modulate.a = 0

	tween.tween_property(male_node.get_parent(), "modulate:a", 0.0, 0.5)

	tween.finished.connect(func ():
		label.modulate.a = 0
		label.text = "¿Cómo te llamas?"
		edit_container.modulate.a = 0
		edit_container.visible = true

		var tween2 = create_tween()
		tween2.tween_property(label, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(name_input, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(continue_button, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(edit_container, "modulate:a", 1.0, 0.5)
	)

	player_data["gender"] = "female"


func _on_continue_pressed() -> void:
	if name_input.text != "":
		player_data["name"] = name_input.text
		_GameState.player_data = player_data
		_GameState.queue_dialogues([
			"res://dialogue/C00/C00_E02_Bienvenida_Orqui.dialogue",
			"res://dialogue/C00/C00_E03_Teatro_Facultad.dialogue",
			"res://dialogue/C00/C00_E04_Tour_Facultad.dialogue",
			"res://dialogue/C00/C00_E05_Llegada_Dormitorio.dialogue",
			{
				"path": "res://dialogue/C00/C00_E05_Llegada_Dormitorio.dialogue",
				"next_scene": "res://scenes/pages/maps/dormitory/player_room.tscn"
			}
		])
		_GameState.start_dialogue("res://dialogue/C00/C00_E01_Entrada_Facultad.dialogue")
