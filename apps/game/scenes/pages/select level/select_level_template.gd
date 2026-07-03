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

	# Cargar progreso y refrescar todos los botones
	_LevelProgressManager.load_progress()
	refresh_all_levels()

	back_button.pressed.connect(_on_back_pressed)
	var i : int = 0
	for btn in buttons_panel.get_children():
		if btn.has_method("refresh_state"):
			btn.segment_id = i
		btn.get_child(0).pressed.connect(_on_play_level.bind(i))
		i += 1


## Refresca el estado visual de todos los botones de nivel.
func refresh_all_levels() -> void:
	for level_button in buttons_panel.get_children():
		if level_button.has_method("refresh_state"):
			level_button.refresh_state()


func _on_play_level(segment_id : int) -> void:
	# Verificar que el nivel esté desbloqueado
	if not _LevelProgressManager.is_level_unlocked(segment_id):
		print("[LevelSelect] Nivel %d bloqueado — ignorando" % segment_id)
		return

	var packed : PackedScene = load(gameplay_scene)

	if packed.instantiate() is TemplateLevel:
		if segment_id == 0:
			DialogueManager.show_dialogue_balloon(load("res://dialogue/C01/C01_E04_Primera_Clase.dialogue"), "start")
			_LevelProgressManager.complete_level(0)
		elif segment_id > 0 and segment_id <= 5:
			var level_instance : TemplateLevel = packed.instantiate()
			level_instance.segment_id = segment_id
			get_tree().root.add_child(level_instance)
			get_tree().current_scene.queue_free()
			get_tree().current_scene = level_instance
	else:
		push_error("[LevelSelect] gameplay_scene no es un TemplateLevel")

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
