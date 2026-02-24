extends Node
class_name HotspotPulse

@export var hotspot_node_path: NodePath                     # Nodo objetivo (Button, Control, etc.)
@export var min_alpha: float = 0.0                          # Transparencia mínima
@export var max_alpha: float = 0.35                         # Transparencia máxima
@export var pulse_duration: float = 1.2                     # Tiempo de cada fase del pulso
@export var delay_before_start: float = 0.3                 # Retraso inicial del efecto

var hotspot_node: Control
var tween: Tween

func _ready():
	hotspot_node = get_node(hotspot_node_path) as Control
	if hotspot_node == null:
		push_warning("HotspotPulse: No se encontró el nodo asignado.")
		return

	# Forzar hotspot invisible inicialmente
	hotspot_node.modulate.a = min_alpha

	# Conectar eventos del mouse
	if hotspot_node.has_signal("mouse_entered"):
		print("Entra aqui")
		hotspot_node.mouse_entered.connect(_on_mouse_entered)
	if hotspot_node.has_signal("mouse_exited"):
		hotspot_node.mouse_exited.connect(_on_mouse_exited)

	# Iniciar parpadeo constante
	start_pulse()


# ------------------------------------------------------------
# 🔥 PULSO SUAVE
# ------------------------------------------------------------
func start_pulse():
	tween = get_tree().create_tween().set_loops()

	tween.tween_interval(delay_before_start)

	# Fade in
	tween.tween_property(
		hotspot_node,
		"modulate:a",
		max_alpha,
		pulse_duration
	).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

	# Fade out
	tween.tween_property(
		hotspot_node,
		"modulate:a",
		min_alpha,
		pulse_duration
	).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)


# ------------------------------------------------------------
# 🔥 CAMBIO DE CURSOR AL PASAR EL MOUSE
# ------------------------------------------------------------
func _on_mouse_entered():
	# Cambiar cursor a uno que indique interacción
	Input.set_default_cursor_shape(Input.CURSOR_POINTING_HAND)

func _on_mouse_exited():
	# Regresar al cursor normal
	Input.set_default_cursor_shape(Input.CURSOR_ARROW)
