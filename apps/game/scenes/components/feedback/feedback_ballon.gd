class_name FeedbackBalloon
extends Control

const SCENE_PATH = "res://scenes/components/feedback/feedback_ballon.tscn"
var _is_static_instance := false

@export_enum("positive", "negative", "neutral", "info") var feedback_type := "neutral"
@export var display_time: float = 2.5

@onready var panel = $PanelContainer/MarginContainer/VBoxContainer/HBoxContainer
@onready var label = $PanelContainer/MarginContainer/VBoxContainer/HBoxContainer/Label
@onready var icon = $PanelContainer/MarginContainer/VBoxContainer/HBoxContainer/TextureRect
@onready var animation_player = $AnimationPlayer
@onready var audio_player = $AudioStreamPlayer

var colors = {
	"positive": Color(0.2, 0.8, 0.2, 0.9),
	"negative": Color(0.9, 0.2, 0.2, 0.9),
	"neutral":  Color(0.7, 0.7, 0.7, 0.9),
	"info":     Color(0.2, 0.6, 1.0, 0.9)
}

var icons = {
	"positive": preload("res://icon.svg"),
	"negative": preload("res://icon.svg"),
	"neutral":  preload("res://icon.svg"),
	"info":     preload("res://icon.svg")
}

# ─── API estática ─────────────────────────────────────────────────────────────

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

	balloon._setup_static(message, type)
	scene_tree.root.add_child(balloon)

# ─── Configuración previa al árbol ───────────────────────────────────────────

func _setup_static(message: String, type: String) -> void:
	feedback_type = type
	set_meta("pending_message", message)
	set_meta("pending_type", type)

# ─── Inicialización ───────────────────────────────────────────────────────────

func _ready() -> void:
	print("[FeedbackBalloon] _ready llamado")
	print("[FeedbackBalloon] is_static=%s" % str(_is_static_instance))
	print("[FeedbackBalloon] has_meta pending_message=%s" % str(has_meta("pending_message")))
	print("[FeedbackBalloon] panel=%s" % str(panel))
	print("[FeedbackBalloon] label=%s" % str(label))
	print("[FeedbackBalloon] icon=%s" % str(icon))
	print("[FeedbackBalloon] _ready llamado - is_static=%s" % str(_is_static_instance))
	
	if _is_static_instance and has_meta("pending_message"):
		var message: String = get_meta("pending_message")
		var type: String = get_meta("pending_type")

		if label == null:
			push_error("[FeedbackBalloon] Label no encontrado en _ready.")
			return

		label.text = message
		panel.modulate = colors.get(type, colors["neutral"])
		panel.modulate.a = 0.0

		_animate_and_dismiss()

	elif not _is_static_instance:
		if _GameController and _GameController.feedback_controller:
			_GameController.feedback_controller.feedback_generated.connect(_on_feedback_generated)

# ─── Uso por señal (balloon colocado en escena manualmente) ──────────────────

func _on_feedback_generated(feedback_data: Dictionary) -> void:
	print("[FeedbackBalloon] Feedback recibido:", feedback_data)
	var message: String = feedback_data.get("message", "")
	var type: String = feedback_data.get("type", "neutral")

	label.text = message
	panel.modulate = colors.get(type, colors["neutral"])
	panel.modulate.a = 0.0

	_animate_and_dismiss()

# ─── Animación ────────────────────────────────────────────────────────────────

func _animate_and_dismiss() -> void:
	var tree := Engine.get_main_loop() as SceneTree

	if audio_player and audio_player.stream:
		audio_player.play()

	var tween_in := create_tween()
	tween_in.tween_property(panel, "modulate:a", 1.0, 0.25)
	await tween_in.finished

	await tree.create_timer(display_time).timeout

	var tween_out := create_tween()
	tween_out.tween_property(panel, "modulate:a", 0.0, 0.25)
	await tween_out.finished

	queue_free()
