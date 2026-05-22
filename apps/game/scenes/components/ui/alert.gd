class_name AlertComponent
extends Control

# Ruta a tu escena del componente
const SCENE_PATH = "res://scenes/components/ui/alert.tscn"

static func show_alert(
	text: String,
	type: String = "normal",
	duration: float = 3.0
) -> void:
	# Obtener el árbol de escena actual
	var scene_tree = Engine.get_main_loop() as SceneTree
	if not scene_tree:
		return

	# Instanciar la escena del componente
	var scene: PackedScene = load(SCENE_PATH)
	var alert: AlertComponent = scene.instantiate()

	# Configurar el componente antes de añadirlo
	alert.setup(text, type)
	
	alert.z_index = 100
	
	# Añadir al root para que sea independiente de la escena actual
	scene_tree.root.add_child(alert)
	
	# Auto-destruirse tras la duración
	await scene_tree.create_timer(duration).timeout
	alert.queue_free()


# Método de configuración interna
func setup(text: String, type: String) -> void:
	# Aquí aplicas el texto y el estilo visual
	$Panel/Label.text = text
	# Ejemplo: aplicar tema según type
	pass
