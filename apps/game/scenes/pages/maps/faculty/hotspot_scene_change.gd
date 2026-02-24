extends Node
class_name HotspotSceneChange

@export var hotspot_node_path: NodePath
@export_file("*.tscn") var scene_to_load: String
@export var fade_duration: float = 0.4      # opcional si usas fade o transiciones

var hotspot_node: Control


func _ready():
	hotspot_node = get_node(hotspot_node_path) as Control
	if hotspot_node == null:
		push_warning("HotspotSceneChange: No se encontró el nodo asignado.")
		return

	# Conectar a la señal de clic
	if hotspot_node.has_signal("pressed"):
		hotspot_node.pressed.connect(_on_pressed)
	elif hotspot_node.has_signal("gui_input"):
		hotspot_node.gui_input.connect(_on_gui_input)
	else:
		push_warning("HotspotSceneChange: El nodo no tiene señales de clic disponibles.")


# ------------------------------------------------------------
# 🔥 MANEJO DEL CLIC
# ------------------------------------------------------------

func _on_pressed():
	_change_scene()


# Fallback por si el nodo no es Button sino un Control normal
func _on_gui_input(event: InputEvent):
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_change_scene()


# ------------------------------------------------------------
# 🔥 CAMBIO DE ESCENA
# ------------------------------------------------------------
func _change_scene():
	print("\n[HotspotSceneChange] Ejecutando _change_scene()...")
	
	if scene_to_load.is_empty():
		push_warning("HotspotSceneChange: No se asignó ninguna escena para cargar.")
		print("[HotspotSceneChange][ERROR] No se asignó ninguna escena para cargar. Cancelando cambio de escena.")
		return
	
	print("[HotspotSceneChange] Escena asignada:", scene_to_load)
	print("[HotspotSceneChange] Iniciando fade-in. Duración:", fade_duration)
	
	_Util.fade_in(fade_duration)
	
	print("[HotspotSceneChange] Fade-in finalizado. Procediendo a cargar escena...")
	
	get_tree().change_scene_to_file(scene_to_load)
	
	print("[HotspotSceneChange] Escena cargada con éxito:", scene_to_load)
