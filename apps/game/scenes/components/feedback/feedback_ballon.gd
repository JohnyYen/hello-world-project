# Component that displays feedback messages to the player in a balloon-style UI element
# Can be used statically via FeedbackBalloon.show_feedback() without needing to be in the scene
class_name FeedbackBalloon
extends Control

const SCENE_PATH = "res://scenes/components/ui/feedback_balloon.tscn"
var _is_static_instance := false
## Enum property for the feedback type, affecting visual styling
@export_enum("positive", "negative", "neutral", "info") var feedback_type := "neutral"

## Time in seconds to display the feedback before auto-hiding
@export var display_time: float = 2.5

## Reference to the panel container UI element
@onready var panel = $PanelContainer/MarginContainer/VBoxContainer/HBoxContainer
## Reference to the label UI element for displaying the message
@onready var label = $PanelContainer/MarginContainer/VBoxContainer/HBoxContainer/Label
## Reference to the icon UI element
@onready var icon = $PanelContainer/MarginContainer/VBoxContainer/HBoxContainer/Icon
## Reference to the animation player for showing/hiding animations
@onready var animation_player = $AnimationPlayer
## Reference to the audio player for sound effects
@onready var audio_player = $AudioStreamPlayer

## Color mapping for different feedback types
var colors = {
	"positive": Color(0.2, 0.8, 0.2, 0.9),
	"negative": Color(0.9, 0.2, 0.2, 0.9),
	"neutral":  Color(0.7, 0.7, 0.7, 0.9),
	"info":     Color(0.2, 0.6, 1.0, 0.9)
}

## Icon mapping for different feedback types
var icons = {
	"positive": preload("res://icon.svg"),
	"negative": preload("res://icon.svg"),
	"neutral":  preload("res://icon.svg"),
	"info":     preload("res://icon.svg")
}

# ─── API estática ─────────────────────────────────────────────────────────────

## Instancia y muestra el balloon desde cualquier parte del código.
## Ejemplo: FeedbackBalloon.show_feedback("¡Correcto!", "positive")
static func show_feedback(
	message: String,
	type: String = "neutral",
	duration: float = 2.5
) -> void:
	var scene_tree := Engine.get_main_loop() as SceneTree
	if not scene_tree:
		push_error("[FeedbackBalloon] No se pudo obtener el SceneTree.")
		return

	var packed: PackedScene = load(SCENE_PATH)
	if not packed:
		push_error("[FeedbackBalloon] No se encontró la escena en: " + SCENE_PATH)
		return
	
	
	var balloon: FeedbackBalloon = packed.instantiate()
	balloon._is_static_instance = true
	balloon.display_time = duration
	balloon.z_index = 100

	# Añadir al root para que sea independiente de la escena activa
	scene_tree.root.add_child(balloon)

	# Configurar después de add_child para que los @onready estén listos
	balloon._setup(message, type)

# ─── Inicialización ───────────────────────────────────────────────────────────

func _ready() -> void:
	print("[FeedbackBalloon] Listo.")
	# Conectar al feedback_controller para uso no estático (balloon en escena)
	if _GameController and _GameController.feedback_controller and !_is_static_instance:
		_GameController.feedback_controller.feedback_generated.connect(_on_feedback_generated)

## Configuración interna llamada tras add_child
func _setup(message: String, type: String) -> void:
	feedback_type = type

	if label == null:
		push_error("[FeedbackBalloon] Label no encontrado.")
		return

	label.text = message
	panel.modulate = colors.get(type, colors["neutral"])
	panel.modulate.a = 0.0

	_animate_and_dismiss()

# ─── Uso por señal (balloon colocado en escena manualmente) ──────────────────

func _on_feedback_generated(feedback_data: Dictionary) -> void:
	print("[FeedbackBalloon] Feedback recibido:", feedback_data)
	_setup(
		feedback_data.get("message", ""),
		feedback_data.get("type", "neutral")
	)

# ─── Animación ────────────────────────────────────────────────────────────────

func _animate_and_dismiss() -> void:
	if audio_player and audio_player.stream:
		audio_player.play()

	var tween_in := create_tween()
	tween_in.tween_property(panel, "modulate:a", 1.0, 0.25)
	await tween_in.finished

	await get_tree().create_timer(display_time).timeout

	var tween_out := create_tween()
	tween_out.tween_property(panel, "modulate:a", 0.0, 0.25)
	await tween_out.finished

	queue_free()
