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
func _ready() -> void:
	var ballon = DialogueManager.show_dialogue_balloon(load("res://dialogue/start.dialogue"))
	edit_container.visible = false
	#name_input.visible = false
	#continue_button.visible = false

func _on_character_male_pressed() -> void:
	var tween = create_tween()
	
	male_node.get_child(0).get_child(0).queue_free()
	male_node.get_child(2).queue_free()
	male_node_panel.modulate.a = 0
	
	# 1️⃣ Desvanece el personaje femenino
	tween.tween_property(female_node.get_parent(), "modulate:a", 0.0, 0.5)
	
	# 2️⃣ Cuando termina el fade del personaje, cambia el texto y muestra los inputs
	tween.finished.connect(func ():
		# Cambiar texto del label con fade-in
		label.modulate.a = 0
		label.text = "¿Cómo te llamas?"
		edit_container.modulate.a = 0
		#name_input.modulate.a = 0
		#continue_button.modulate.a = 0

		# Mostrar nodos antes de animar
		#name_input.visible = true
		#continue_button.visible = true
		edit_container.visible = true

		# 3️⃣ Crear un nuevo tween para el fade-in del texto y los controles
		var tween2 = create_tween()
		tween2.tween_property(label, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(name_input, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(continue_button, "modulate:a", 1.0, 0.5)
		tween2.parallel().tween_property(edit_container, "modulate:a", 1.0, 0.5)
	)
	player_data["gender"] = "male"
	name_input.focus_mode = Control.FocusMode.FOCUS_ALL

	
	
func _on_character_female_pressed() -> void:
	var tween = create_tween()
	
	female_node.get_child(0).get_child(0).queue_free()
	female_node.get_child(2).queue_free()
	female_node_panel.modulate.a = 0
	
	tween.tween_property(male_node.get_parent(), "modulate:a", 0.0, 0.5)
	# 2️⃣ Cuando termina el fade del personaje, cambia el texto y muestra los inputs
	tween.finished.connect(func ():
		# Cambiar texto del label con fade-in
		label.modulate.a = 0
		label.text = "¿Cómo te llamas?"
		edit_container.modulate.a = 0
		#name_input.modulate.a = 0
		#continue_button.modulate.a = 0

		# Mostrar nodos antes de animar
		#name_input.visible = true
		#continue_button.visible = true
		edit_container.visible = true

		# 3️⃣ Crear un nuevo tween para el fade-in del texto y los controles
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
		_GameState.queue_dialogues(["res://dialogue/C00/C00_E02_Bienvenida_Orqui.dialogue", "res://dialogue/C00/C00_E03_Teatro_Facultad.dialogue", "res://dialogue/C00/C00_E04_Tour_Facultad.dialogue", "res://dialogue/C00/C00_E05_Llegada_Dormitorio.dialogue", {
				"path": "res://dialogue/C00/C00_E05_Llegada_Dormitorio.dialogue", "next_scene": "res://scenes/pages/maps/dormitory/player_room.tscn"
			}])
		#_GameState.dialogue_queue = [
			#{
				#"path" : "res://dialogue/C00/C00_E02_Bienvenida_Orqui.dialogue",
			#},
			#{
				#"path": "res://dialogue/C00/C00_E03_Teatro_Facultad.dialogue",
			#},
			#{
				#"path": "res://dialogue/C00/C00_E04_Tour_Facultad.dialogue",
			#},
			#{
				#"path": "res://dialogue/C00/C00_E05_Llegada_Dormitorio.dialogue",
			#},
			#{
				#"path": "res://dialogue/C00/C00_E05_Llegada_Dormitorio.dialogue", "next_scene": "res://scenes/pages/maps/dormitory/player_room.tscn"
			#},
			##{
				##"path": "res://dialogue/C00/C00_E05_Llegada_Dormitorio.dialogue", "next_scene": "res://scenes/pages/menu.tscn"
			##}
		#]
		_GameState.start_dialogue("res://dialogue/C00/C00_E01_Entrada_Facultad.dialogue")
		#self.queue_free()
		#_GameState.start_dialogue("res://dialogue/C00/C00_E02_Bienvenida_Orqui.dialogue")
		#_GameState.start_dialogue("res://dialogue/C00/C00_E03_Teatro_Facultad.dialogue")
		#_GameState.start_dialogue("res://dialogue/C00/C00_E01_Entrada_Facultad.dialogue")
		
