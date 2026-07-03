## Responsabilidad única: Manejar el flujo y procesamiento de diálogos
## Emite señales para que otros sistemas escuchen, sin conocer sus detalles
class_name DialogueFlow
extends Node

signal dialogue_started(dialogue_path: String)
signal dialogue_show_requested(dialogue_path: String)
signal dialogue_finished()
signal queue_finished()
signal scene_transition_requested(scene_path: String)

var _current_dialogue_path: String = ""
var _next_scene_path: String = ""
var _dialogue_queue: Array = []

func _init() -> void:
	DialogueManager.dialogue_ended.connect(Callable(self, "_on_dialogue_manager_finished"))

func _ready() -> void:
	pass

# =============================================================================
#                            CONTROL DE FLUJO
# =============================================================================

## Inicia un nuevo diálogo (el primero de una secuencia)
func start_dialogue(dialogue_path: String, next_scene: String = "") -> void:
	_current_dialogue_path = dialogue_path
	_next_scene_path = next_scene
	
	print("DialogueFlow: Iniciando diálogo '%s'" % dialogue_path)
	print("DialogueFlow: Escena siguiente '%s'" % next_scene)
	
	print("ESTOY INICIANDO EL DIALOGO EN DIALOGUE FLOW")
	dialogue_started.emit(dialogue_path)
	print("Estoy solicitando que se me muestre una escena de la novela visual")
	dialogue_show_requested.emit(dialogue_path)

## Agrega diálogos a la cola para ser procesados secuencialmente
func queue_dialogue(dialogue_path: String, next_scene: String = "") -> void:
	var entry = {
		"path": dialogue_path,
		"next_scene": next_scene
	}
	_dialogue_queue.append(entry)
	print("DialogueFlow: Diálogo agregado a cola. Total en cola: %d" % _dialogue_queue.size())

## Agregar múltiples diálogos de una vez
func queue_dialogues(dialogues: Array) -> void:
	for dialogue in dialogues:
		if dialogue is String:
			queue_dialogue(dialogue)
		elif dialogue is Dictionary:
			queue_dialogue(dialogue.get("path", ""), dialogue.get("next_scene", ""))

## Obtiene el diálogo actual
func get_current_dialogue() -> String:
	return _current_dialogue_path

## Obtiene la cantidad de diálogos en cola
func get_queue_size() -> int:
	return _dialogue_queue.size()

## Limpia completamente la cola
func clear_queue() -> void:
	_dialogue_queue.clear()
	_next_scene_path = ""
	_current_dialogue_path = ""
	print("DialogueFlow: Cola limpiada")

func force_finish() -> void:
	_on_dialogue_manager_finished(null)
# =============================================================================
#                         MANEJADOR DE FINALIZACIONES
# =============================================================================

func _on_dialogue_manager_finished(resource: DialogueResource) -> void:
	print("DialogueFlow: Diálogo finalizado '%s'" % _current_dialogue_path)
	
	var scene_to_load = _next_scene_path
	_next_scene_path = ""
	
	# Prioridad 1: Si hay escena destino, cargarla
	if scene_to_load != "":
		print("DialogueFlow: Transicionando a escena '%s'" % scene_to_load)
		scene_transition_requested.emit(scene_to_load)
		_current_dialogue_path = ""
		return
	
	# Prioridad 2: Si hay diálogos en cola, mostrar el siguiente
	if _dialogue_queue.size() > 0:
		var next_entry = _dialogue_queue.pop_front()
		_current_dialogue_path = next_entry["path"]
		_next_scene_path = next_entry.get("next_scene", "")
		
		print("DialogueFlow: Procesando siguiente de cola '%s'" % _current_dialogue_path)
		dialogue_show_requested.emit(_current_dialogue_path)
		return
	
	# Prioridad 3: No hay más nada, flujo finalizado
	print("DialogueFlow: No hay más diálogos. Flujo completado")
	_current_dialogue_path = ""
	dialogue_finished.emit()
	queue_finished.emit()

# =============================================================================
#                              UTILIDADES
# =============================================================================

## Obtiene información de depuración del flujo actual
func debug_info() -> Dictionary:
	return {
		"current_dialogue": _current_dialogue_path,
		"next_scene": _next_scene_path,
		"queue_size": _dialogue_queue.size(),
		"queue": _dialogue_queue.duplicate()
	}
