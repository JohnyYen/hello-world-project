class_name LoadingScreen
extends ColorRect

signal transition_finished

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var loading_label: Label = $MarginContainer/VBoxContainer/HBoxContainer/Label

var _next_scene: String = ""
var _dot_count: int = 0
var _dot_timer: float = 0.0

func _ready() -> void:
	color = Color(0, 0, 0, 0)
	z_index = 100
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	visible = false

func _process(delta: float) -> void:
	if not visible:
		return
	
	_dot_timer += delta
	if _dot_timer >= 0.4:
		_dot_timer = 0.0
		_dot_count = (_dot_count + 1) % 4
		loading_label.text = "Cargando" + ".".repeat(_dot_count)

## Entry point estático
static func change_scene(scene_path: String) -> void:
	var scene_tree := Engine.get_main_loop() as SceneTree
	if not scene_tree:
		push_error("LoadingScreen: No hay SceneTree")
		return

	var packed := load("res://scenes/components/ui/loading_screen.tscn") as PackedScene
	if not packed:
		push_error("LoadingScreen: No pudo cargar loading_screen.tscn")
		scene_tree.change_scene_to_file(scene_path)
		return

	var loading := packed.instantiate() as LoadingScreen
	if not loading:
		push_error("LoadingScreen: No pudo instanciar")
		scene_tree.change_scene_to_file(scene_path)
		return

	loading._next_scene = scene_path
	scene_tree.root.add_child(loading)
	loading._start()

func _start() -> void:
	visible = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	
	# Fade in: animación del editor o fallback por código
	if animation_player and animation_player.has_animation("fade_in"):
		animation_player.play("fade_in")
		await animation_player.animation_finished
	else:
		# Fallback manual
		var tween := create_tween()
		tween.tween_property(self, "color", Color(0, 0, 0, 1), 0.3)
		await tween.finished
	
	await _load_scene()

func _load_scene() -> void:
	print("LOADING: Iniciando carga hacia: ", _next_scene)
	var scene_tree := get_tree()
	
	# 1. Cargar la escena primero para verificar que existe
	var packed := load(_next_scene) as PackedScene
	if not packed:
		push_error("LOADING: load() devolvió null para: " + _next_scene)
		_finish()
		return
	
	print("LOADING: Escena cargada correctamente")
	
	# 2. Intentar el cambio y CAPTURAR el error
	var err := scene_tree.change_scene_to_packed(packed)
	print("LOADING: change_scene_to_packed retornó: ", err, " (OK=", OK, ")")
	
	if err != OK:
		push_error("LOADING: Falló el cambio de escena. Error code: " + str(err))
		_finish()
		return
	
	# 3. Esperar frames en la NUEVA escena
	await scene_tree.process_frame
	await scene_tree.process_frame
	print("LOADING: Frames procesados, nueva escena activa")
	_SaveController.save_game()
	_finish()

func _finish() -> void:
	# Fade out: animación del editor o fallback
	if animation_player and animation_player.has_animation("fade_out"):
		animation_player.play("fade_out")
		await animation_player.animation_finished
	else:
		var tween := create_tween()
		tween.tween_property(self, "color", Color(0, 0, 0, 0), 0.3)
		await tween.finished
	
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	visible = false
	queue_free()
