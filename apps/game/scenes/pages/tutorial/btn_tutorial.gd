extends Button

@onready var highlight = $Highlight
var pulse_tween = null

var forced_highlight = false

func _ready():
	self.mouse_entered.connect(_on_mouse_entered)
	self.mouse_exited.connect(_on_mouse_exited)

	# Estado inicial
	highlight.visible = false
	highlight.scale = Vector2(1, 1)
	highlight.color = Color(1, 1, 1, 0.15)

func enable_tutorial_highlight():
	forced_highlight = true
	highlight.visible = true
	start_pulse()

func disable_tutorial_highlight():
	forced_highlight = false
	highlight.visible = false
	stop_pulse()

func _on_mouse_entered():
	if forced_highlight:
		return
	start_pulse()

func _on_mouse_exited():
	if forced_highlight:
		return
	stop_pulse()

func start_pulse():
	if pulse_tween:
		pulse_tween.kill()

	pulse_tween = create_tween()
	pulse_tween.set_loops()

	# 1️⃣ Efecto de expansión
	pulse_tween.tween_property(
		highlight, "scale",
		Vector2(1.05, 1.05), 0.4
	).set_trans(Tween.TRANS_SINE)

	pulse_tween.tween_property(
		highlight, "scale",
		Vector2(1.0, 1.0), 0.4
	).set_trans(Tween.TRANS_SINE)

	# 2️⃣ Efecto de brillo suave (no toca alfa)
	pulse_tween.parallel().tween_property(
		highlight, "color",
		Color(1, 1, 1, 0.22), 0.4
	)

	pulse_tween.tween_property(
		highlight, "color",
		Color(1, 1, 1, 0.15), 0.4
	)

func stop_pulse():
	if pulse_tween:
		pulse_tween.kill()

	# Restaurar estado limpio
	highlight.scale = Vector2(1, 1)
	highlight.color = Color(1, 1, 1, 0.15)
