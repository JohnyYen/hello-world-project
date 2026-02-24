extends Control

@onready var pc_panel = $PC
@onready var message_label = $"Message Label"

func _ready() -> void:
	print_debug("[PlayerRoom] _ready() iniciado")
	message_label.visible = false
	pc_panel.visible = false
	print_debug("[PlayerRoom] Paneles ocultos: PC =", pc_panel.visible, " MessageLabel =", message_label.visible)
	
	# Puedes activar el fade si quieres
	# _Util.fade_in()
	
	await get_tree().process_frame
	if not _GameState.flags.get("has_completed_tutorial_in_room", false):
		print_debug("[PlayerRoom] Tutorial no completado, iniciando tutorial...")
		_star_tutorial()
	else:
		print_debug("[PlayerRoom] Tutorial ya completado, listo para interactuar")

func _star_tutorial():
	print_debug("[PlayerRoom] Cambiando escena a tutorial_room.tscn")
	var err = get_tree().change_scene_to_file("res://scenes/pages/tutorial/tutorial_room.tscn")
	print_debug("[PlayerRoom] Resultado change_scene_to_file:", err)

func _on_pc_btn_pressed() -> void:
	pc_panel.visible = true
	print_debug("[PlayerRoom] Botón PC presionado, PC panel visible =", pc_panel.visible)

func _on_bedroom_btn_pressed() -> void:
	print_debug("[PlayerRoom] Botón Bedroom presionado, guardando juego...")
	_SaveController.save_game()
	message_label.visible = true
	print_debug("[PlayerRoom] Message label visible =", message_label.visible)
