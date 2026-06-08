class_name GameState
extends Node

var current_dialogue_path: String = ""
var next_scene_path: String = ""
var flags = {}
var dialogue_queue: Array = []
var player_data = {}

func _init() -> void:
	DialogueManager.dialogue_ended.connect(Callable(self, "on_dialogue_finished"))

func _ready():
	DialogueManager.dialogue_ended.connect(Callable(self, "on_dialogue_finished"))

# -------------- Serialización ----------------
func to_dict() -> Dictionary:
	return {
		"current_dialogue_path": current_dialogue_path,
		"next_scene_path": next_scene_path,
		"flags": flags,
		"dialogue_queue": dialogue_queue,
		"player_data": player_data
	}
	
func from_dict(data : Dictionary) -> void:
	current_dialogue_path = data.get("current_dialogue_path", "")
	next_scene_path = data.get("next_scene_path", "")
	flags = data.get("flags", {})
	dialogue_queue = data.get("dialogue_queue", [])
	player_data = data.get("player_data", {"name": "Leo", "gender": "male"})


# ============================================================
#               CONTROL PRINCIPAL DE FLUJO
# ============================================================

func start_dialogue(dialogue_path: String, next_scene: String = "", is_overlay : bool = false) -> void:
	# Registrar el diálogo actual y la escena siguiente
	current_dialogue_path = dialogue_path
	next_scene_path = next_scene
	print("DEBUG [Game State]: Iniciando diálogo %s" % current_dialogue_path)
	print("DEBUG [Game State]: Siguiente escena asignada %s" % next_scene_path)
	#DialogueManager.show_dialogue_balloon(load(current_dialogue_path))
	# Cambiar SIEMPRE a la escena de Visual Novel
	LoadingScreen.change_scene("res://scenes/pages/dialogue/projector_screen.tscn")

func show_current_balloon():
	if current_dialogue_path != "":
		DialogueManager.show_dialogue_balloon(load(current_dialogue_path))

func on_dialogue_finished() -> void:
	print("DEBUG [Game State]: Finalizó diálogo. next_scene_path = %s" % next_scene_path)

	_SaveController.save_game()

	# 1. Capturamos la escena que debe cargarse
	var scene_to_load = next_scene_path

	# 2. Reseteamos next_scene_path de inmediato
	next_scene_path = ""

	# 3. ¿Hay un diálogo en cola? SOLO hacemos esto si no hay escena destino inmediata
	if dialogue_queue.size() > 0 and scene_to_load == "":
		var next = dialogue_queue.pop_front()

		current_dialogue_path = next["path"]
		next_scene_path = next.get("next_scene", "")

		print("DEBUG [Game State]: Atendiendo diálogo en cola: %s" % current_dialogue_path)
		print("DEBUG [Game State]: Nueva escena asignada en cola: %s" % next_scene_path)
		DialogueManager.show_dialogue_balloon(load(current_dialogue_path))
		return

	# 4. Si hay escena destino → cargarla
	if scene_to_load != "":
		print("DEBUG [Game State]: Cambiando escena ahora: %s" % scene_to_load)
		LoadingScreen.change_scene(scene_to_load)
		return

	# 5. Si no hay más nada → fin del flujo (volvería al mapa u otra pantalla)
	print("DEBUG [Game State]: No hay escena ni diálogos pendientes. Flujo detenido.")
