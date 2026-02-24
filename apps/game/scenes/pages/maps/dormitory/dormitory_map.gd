extends Control

@onready var male_btn = $"Male Btn"

func _ready() -> void:
	_Util.fade_in()
	male_btn.pressed.connect(_on_pressed.bind("res://scenes/pages/maps/dormitory/player_room.tscn"))
	male_btn.mouse_entered.connect(_on_TextureButton_mouse_entered.bind(male_btn))
	male_btn.mouse_exited.connect(_on_TextureButton_mouse_exited.bind(male_btn))


	
func _on_pressed(path: String):
	get_tree().change_scene_to_file(path)


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
