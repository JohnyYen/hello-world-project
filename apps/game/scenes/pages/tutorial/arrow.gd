extends TextureRect

@export var scale_strength: float = 0.15
@export var speed: float = 2.0
@export var alpha_strength: float = 0.3

var base_scale := Vector2.ONE
var base_modulate := Color(1, 1, 1, 1)

func _ready():
	base_scale = scale
	base_modulate = modulate

func _process(delta):
	var t = sin(Time.get_ticks_msec() / 1000.0 * speed)

	# Escala pulsante
	scale = base_scale * (1.0 + t * scale_strength)

	# Opacidad pulsante
	var alpha = 1.0 - abs(t) * alpha_strength
	modulate.a = alpha
