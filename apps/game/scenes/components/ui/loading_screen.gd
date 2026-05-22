class_name LoadingScreen
extends ColorRect

signal transition_finished

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var loading_label: Label = $MarginContainer/VBoxContainer/HBoxContainer/Label

var _next_scene: String = ""
var _dot_count: int = 0
var _dot_timer: float = 0.0

func _ready() -> void:
	# Cubre toda la pantalla y arranca invisible
	color = Color(0, 0, 0, 0)
	z_index = 100
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func _process(delta: float) -> void:
	if not visible:
		return
	# Anima los puntos "Cargando... → Cargando·· → Cargando···"
	_dot_timer += delta
	if _dot_timer >= 0.4:
		_dot_timer = 0.0
		_dot_count = (_dot_count + 1) % 4
		loading_label.text = "Cargando" + ".".repeat(_dot_count)

## Método principal — llama esto en lugar de change_scene_to_file()
## @param scene_path: Ruta a la escena destino
static func change_scene(scene_path: String) -> void:
	var scene_tree = Engine.get_main_loop() as SceneTree
	if not scene_tree:
		return

	var packed: PackedScene = load("res://scenes/components/ui/loading_screen.tscn")
	var loading: LoadingScreen = packed.instantiate()
	loading._next_scene = scene_path
	scene_tree.root.add_child(loading)
	loading._start()

func _start() -> void:
	visible = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	animation_player.play("fade_in")
	await animation_player.animation_finished
	await _load_scene()

func _load_scene() -> void:
	var scene_tree = get_tree()

	# Cambia la escena mientras la pantalla está negra
	scene_tree.change_scene_to_file(_next_scene)

	# Espera un frame a que la nueva escena esté lista
	await scene_tree.process_frame
	await scene_tree.process_frame

	animation_player.play("fade_out")
	await animation_player.animation_finished

	mouse_filter = Control.MOUSE_FILTER_IGNORE
	queue_free()
