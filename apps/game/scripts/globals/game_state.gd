#class_name GameState
#extends Node
#
#var current_dialogue_path: String = ""
#var next_scene_path: String = ""
#var flags = {}
#var dialogue_queue: Array = []
#var player_data = {}
#
#func _init() -> void:
	#DialogueManager.dialogue_ended.connect(Callable(self, "on_dialogue_finished"))
#
#func _ready():
	#DialogueManager.dialogue_ended.connect(Callable(self, "on_dialogue_finished"))
#
## -------------- Serialización ----------------
#func to_dict() -> Dictionary:
	#return {
		#"current_dialogue_path": current_dialogue_path,
		#"next_scene_path": next_scene_path,
		#"flags": flags,
		#"dialogue_queue": dialogue_queue,
		#"player_data": player_data
	#}
	#
#func from_dict(data : Dictionary) -> void:
	#current_dialogue_path = data.get("current_dialogue_path", "")
	#next_scene_path = data.get("next_scene_path", "")
	#flags = data.get("flags", {})
	#dialogue_queue = data.get("dialogue_queue", [])
	#player_data = data.get("player_data", {"name": "Leo", "gender": "male"})
#
#
## ============================================================
##               CONTROL PRINCIPAL DE FLUJO
## ============================================================
#
#func start_dialogue(dialogue_path: String, next_scene: String = "", is_overlay : bool = false) -> void:
	## Registrar el diálogo actual y la escena siguiente
	#current_dialogue_path = dialogue_path
	#next_scene_path = next_scene
	#print("DEBUG [Game State]: Iniciando diálogo %s" % current_dialogue_path)
	#print("DEBUG [Game State]: Siguiente escena asignada %s" % next_scene_path)
	##DialogueManager.show_dialogue_balloon(load(current_dialogue_path))
	## Cambiar SIEMPRE a la escena de Visual Novel
	#LoadingScreen.change_scene("res://scenes/pages/dialogue/projector_screen.tscn")
#
#func show_current_balloon():
	#if current_dialogue_path != "":
		#DialogueManager.show_dialogue_balloon(load(current_dialogue_path))
#
#func on_dialogue_finished() -> void:
	#print("DEBUG [Game State]: Finalizó diálogo. next_scene_path = %s" % next_scene_path)
#
	#_SaveController.save_game()
#
	## 1. Capturamos la escena que debe cargarse
	#var scene_to_load = next_scene_path
#
	## 2. Reseteamos next_scene_path de inmediato
	#next_scene_path = ""
#
	## 3. ¿Hay un diálogo en cola? SOLO hacemos esto si no hay escena destino inmediata
	#if dialogue_queue.size() > 0 and scene_to_load == "":
		#var next = dialogue_queue.pop_front()
#
		#current_dialogue_path = next["path"]
		#next_scene_path = next.get("next_scene", "")
#
		#print("DEBUG [Game State]: Atendiendo diálogo en cola: %s" % current_dialogue_path)
		#print("DEBUG [Game State]: Nueva escena asignada en cola: %s" % next_scene_path)
		#call_deferred("_load_next_dialogue_scene")
		#return
#
	## 4. Si hay escena destino → cargarla
	#if scene_to_load != "":
		#print("DEBUG [Game State]: Cambiando escena ahora: %s" % scene_to_load)
		#LoadingScreen.change_scene(scene_to_load)
		#return
#
	## 5. Si no hay más nada → fin del flujo (volvería al mapa u otra pantalla)
	#print("DEBUG [Game State]: No hay escena ni diálogos pendientes. Flujo detenido.")
#
#func _load_next_dialogue_scene() -> void:
	#LoadingScreen.change_scene("res://scenes/pages/dialogue/projector_screen.tscn")

## GameState: Responsabilidad única es mantener el estado global del juego
## Delega toda lógica de diálogos a DialogueFlow
class_name GameState
extends Node

# Estado del juego
var flags: Dictionary = {}
var player_data: Dictionary = {}

# Componentes (inyectados/instanciados)
var dialogue_flow: DialogueFlow

func _init() -> void:
	dialogue_flow = DialogueFlow.new()
	add_child(dialogue_flow)

func _ready() -> void:
	# Escuchar las señales de DialogueFlow sin conocer sus detalles internos
	dialogue_flow.dialogue_started.connect(_on_dialogue_started)
	dialogue_flow.scene_transition_requested.connect(_on_scene_transition_requested)
	dialogue_flow.queue_finished.connect(_on_dialogue_queue_finished)

# =============================================================================
#                          SERIALIZACIÓN
# =============================================================================

func to_dict() -> Dictionary:
	return {
		"flags": flags,
		"player_data": player_data
	}

func from_dict(data: Dictionary) -> void:
	flags = data.get("flags", {})
	player_data = data.get("player_data", {"name": "Leo", "gender": "male"})

# =============================================================================
#                        CONTROL DE DIÁLOGOS (DELEGADO)
# =============================================================================

## Inicia un diálogo (carga la escena de diálogo si es necesaria)
func start_dialogue(dialogue_path: String, next_scene: String = "") -> void:
	print("ASASAS")
	# Si no estamos en la escena de diálogos, cargarla
	if get_tree().current_scene.name != "ProjectorScreen":
		LoadingScreen.change_scene("res://scenes/pages/dialogue/projector_screen.tscn")
	
	print("HOLAAA X #$##")
	# Delegar a DialogueFlow
	call_deferred("_deferred_start_dialogue", dialogue_path, next_scene)

func _deferred_start_dialogue(path: String, scene: String) -> void:
	dialogue_flow.start_dialogue(path, scene)
## Agrega diálogos a la cola
func queue_dialogue(dialogue_path: String, next_scene: String = "") -> void:
	dialogue_flow.queue_dialogue(dialogue_path, next_scene)

## Agrega múltiples diálogos
func queue_dialogues(dialogues: Array) -> void:
	dialogue_flow.queue_dialogues(dialogues)

## Limpia la cola de diálogos
func clear_dialogue_queue() -> void:
	dialogue_flow.clear_queue()

# =============================================================================
#                      MANEJADORES DE SEÑALES
# =============================================================================

func _on_dialogue_started(dialogue_path: String) -> void:
	print("GameState: Diálogo iniciado '%s'" % dialogue_path)
	print("Holaaaa")
	_SaveController.save_game()

func _on_scene_transition_requested(scene_path: String) -> void:
	print("GameState: Transicionando a '%s'" % scene_path)
	_SaveController.save_game()
	LoadingScreen.change_scene(scene_path)

func _on_dialogue_queue_finished() -> void:
	print("GameState: Cola de diálogos completada")
	_SaveController.save_game()

# =============================================================================
#                            UTILIDADES
# =============================================================================

func get_dialogue_queue_size() -> int:
	return dialogue_flow.get_queue_size()

func get_current_dialogue() -> String:
	return dialogue_flow.get_current_dialogue()

func print_dialogue_debug() -> void:
	print("DialogueFlow Debug: ", dialogue_flow.debug_info())
