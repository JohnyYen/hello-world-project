extends CanvasLayer
class_name BottomBackZone

@export var back_scene_path: String = "" 
@export var zone_height: int = 120            # Altura de la franja inferior
@export var fade_speed: float = 6.0           # Velocidad del fade in/out
@export var text_to_show: String = "Volver atrás"

@onready var zone = ColorRect.new()
@onready var label = Label.new()

var target_alpha := 0.0
var current_alpha := 0.0

func _ready():
	# --- Crear la zona inferior visual ---
	zone.color = Color(1, 1, 1, 0)            # invisible al inicio
	zone.size = Vector2(get_viewport().size.x, zone_height)
	zone.position = Vector2(0, get_viewport().size.y - zone_height)
	add_child(zone)

	# --- Texto centrado ---
	label.text = text_to_show
	label.modulate.a = 0                      # iniciar invisible
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.position = Vector2(0, get_viewport().size.y - zone_height / 2 - 16)
	label.size = Vector2(get_viewport().size.x, 32)
	label.add_theme_color_override("font_color", Color(1,1,1,0.85))
	add_child(label)

	# Asegurar que siempre se dibuje encima
	layer = 100


func _process(delta):
	var mouse_pos = get_viewport().get_mouse_position()
	var bottom_limit = get_viewport().size.y - zone_height

	# Detectar si está dentro de la franja inferior
	if mouse_pos.y >= bottom_limit:
		target_alpha = 0.45
	else:
		target_alpha = 0.0

	# Animar transición suave
	current_alpha = lerp(current_alpha, target_alpha, delta * fade_speed)

	zone.color.a = current_alpha
	label.modulate.a = current_alpha


func _unhandled_input(event):
	# Click dentro de la zona → volver atrás
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var mouse_pos = get_viewport().get_mouse_position()
		if mouse_pos.y >= get_viewport().size.y - zone_height:
			if back_scene_path != "":
				get_tree().change_scene_to_file(back_scene_path)
