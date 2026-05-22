extends Control
@onready var dormitory_btn = $"Dormitory Btn"
@onready var faculty_btn = $"Faculty Btn"
@onready var park_btn = $"Park Btn"

func _ready() -> void:
	dormitory_btn.mouse_entered.connect(_on_TextureButton_mouse_entered.bind(dormitory_btn))
	faculty_btn.mouse_entered.connect(_on_TextureButton_mouse_entered.bind(faculty_btn))
	park_btn.mouse_entered.connect(_on_TextureButton_mouse_entered.bind(park_btn))
	
	dormitory_btn.mouse_exited.connect(_on_TextureButton_mouse_exited.bind(dormitory_btn))
	faculty_btn.mouse_exited.connect(_on_TextureButton_mouse_exited.bind(faculty_btn))
	park_btn.mouse_exited.connect(_on_TextureButton_mouse_exited.bind(park_btn))
	
	dormitory_btn.pressed.connect(_on_mouse_click.bind("res://scenes/pages/maps/dormitory/dormitory_map.tscn"))
	faculty_btn.pressed.connect(_on_mouse_click.bind("res://scenes/pages/maps/faculty/faculty_map.tscn"))
	park_btn.pressed.connect(_on_mouse_click.bind(""))
	
	if not _GameState.flags.get("has_complete_tutorial", false):
		_start_tutorial()

func _start_tutorial():
	pass
func _on_mouse_click(path: String = ""):
	# path = ruta de la escena a la que quieres ir, por ejemplo: "res://scenes/dormitory.tscn"

	# Opción 1: cambio directo usando path como String
	get_tree().change_scene_to_file(path)
	#if error != OK:
		#push_error("No se pudo cargar la escena: %s" % path)

	# Opción 2: cargar primero como recurso (útil si quieres pre-cargar la escena)
	# var escena = load(path)
	# get_tree().change_scene_to(escena)


func _on_TextureButton_mouse_entered(btn : TextureButton):
	btn.z_index = 100
	var t = create_tween()
	t.tween_property(btn, "modulate", Color(1.2, 1.2, 1.2, 1), 0.2)
	#$TextureButton.modulate = Color(1, 1, 0.7) # amarillo suave
	#var tween = create_tween()
	#tween.tween_property(boton, "scale", Vector2(1.1, 1.1), 0.2).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)

func _on_TextureButton_mouse_exited(btn):
	btn.z_index = 0
	var t = create_tween()
	t.tween_property(btn, "modulate", Color(1, 1, 1, 1), 0.2)
	#var tween = create_tween()
	#tween.tween_property(button, "scale", Vector2(1, 1), 0.2).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
