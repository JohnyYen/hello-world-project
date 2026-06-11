## ProjectorScreen: Responsabilidad única es renderizar diálogos
## Escucha a DialogueFlow para saber cuándo mostrar diálogos
extends CanvasLayer

var _current_balloon: Node = null

func _ready() -> void:
	print("HOLAAA desde el screen")
	_GameState.dialogue_flow.dialogue_show_requested.connect(Callable(self, "_on_dialogue_show_requested"))
	
	var current_dialogue = _GameState.dialogue_flow.get_current_dialogue()
	if current_dialogue != "":
		print("ProjectorScreen: Diálogo pendiente detectado, mostrando...")
		_on_dialogue_show_requested(current_dialogue)

## Se ejecuta cuando DialogueFlow solicita mostrar un diálogo
func _on_dialogue_show_requested(dialogue_path: String) -> void:
	print("ProjectorScreen: Mostrando diálogo '%s'" % dialogue_path)
	
	# Destruir globo anterior si existe
	if _current_balloon:
		_current_balloon.queue_free()
		#await _current_balloon.tree_exited
	
	# Mostrar nuevo globo
	var packed_dialogue = load(dialogue_path)
	if packed_dialogue == null:
		push_error("ProjectorScreen: No se pudo cargar diálogo '%s'" % dialogue_path)
		return
	
	_current_balloon = DialogueManager.show_dialogue_balloon(packed_dialogue)

func _exit_tree() -> void:
	if _current_balloon:
		_current_balloon.queue_free()
