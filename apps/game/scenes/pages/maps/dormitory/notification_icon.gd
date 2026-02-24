extends TextureRect
class_name NotificationIcon

@export var pulse_scale: float = 1.2
@export var pulse_duration: float = 0.8

func _ready():
	# Configuración inicial
	stretch_mode = STRETCH_KEEP_ASPECT_CENTERED
	modulate = Color(1, 1, 1, 1) # visible

	# Ajusta tamaño inicial
	scale = Vector2.ONE

	# Inicia el efecto de palpitación
	_start_pulse()


func _start_pulse():
	var tween = create_tween().set_loops() # bucle infinito
	tween.tween_property(self, "scale", Vector2(pulse_scale, pulse_scale), pulse_duration / 2)\
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(self, "scale", Vector2.ONE, pulse_duration / 2)\
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
