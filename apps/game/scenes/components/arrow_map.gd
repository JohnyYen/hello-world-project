extends TextureButton

@export var pulse_scale: Vector2 = Vector2(1.05, 1.05) # escala máxima del pulso
@export var pulse_time: float = 0.5                     # tiempo para subir/bajar
@export_file("*.tscn") var target_scene: String = ""                   # ruta de la escena a cargar

var pulse_tween: Tween = null
var original_scale: Vector2

func _ready():
	original_scale = self.scale
	# Conectar la señal pressed al método de cambio de escena
	self.pressed.connect(_on_pressed)

	# Iniciar animación de pulso
	start_pulse()


# ----------------------
# PULSO (animación suave)
# ----------------------
func start_pulse():
	if pulse_tween:
		pulse_tween.kill()
	
	pulse_tween = create_tween()
	pulse_tween.set_loops()  # bucle infinito
	pulse_tween.tween_property(self, "scale", pulse_scale, pulse_time).set_trans(Tween.TRANS_SINE)
	pulse_tween.tween_property(self, "scale", original_scale, pulse_time).set_trans(Tween.TRANS_SINE)


func stop_pulse():
	if pulse_tween:
		pulse_tween.kill()
		pulse_tween = null
	self.scale = original_scale


# ----------------------
# CAMBIO DE ESCENA
# ----------------------
func _on_pressed():
	if target_scene == "":
		push_error("No se ha definido 'target_scene' en el TextureButton")
		return

	var next_scene = load(target_scene)
	get_tree().change_scene_to_file(next_scene.resource_path)
