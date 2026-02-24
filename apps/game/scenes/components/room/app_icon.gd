extends TextureButton

# --- Propiedades exportadas para el editor ---
@export var app_name: String = ""       # Nombre del Panel de la app en ApplicationsContainer
@export var highlight_node: NodePath    # Nodo opcional de highlight (ColorRect)

# Referencias internas
var is_highlighted: bool = false
@onready var highlight = highlight_node if highlight_node != null else null
@onready var applications_container = get_tree().current_scene.get_node("Applications")

func _ready():
	self.pressed.connect(_on_icon_pressed)
	self.mouse_entered.connect(_on_mouse_entered)
	self.mouse_exited.connect(_on_mouse_exited)

	# Oculta highlight al inicio
	if highlight:
		highlight.visible = false


func _on_icon_pressed():
	if not applications_container:
		push_warning("ApplicationsContainer no encontrado")
		return

	var app_panel = applications_container.get_node_or_null(app_name)
	if app_panel:
		# Alterna visibilidad
		app_panel.visible = not app_panel.visible
		# Opcional: traer al frente
		if app_panel.visible:
			app_panel.raise_()
	else:
		push_warning("AppPanel '%s' no encontrado en ApplicationsContainer" % app_name)


func _on_mouse_entered():
	if highlight:
		highlight.visible = true
		_start_pulse(highlight)


func _on_mouse_exited():
	if highlight:
		highlight.visible = false
		_stop_pulse(highlight)


# --- Funciones de pulso para tutorial / highlight ---
var tweens := {}

func _start_pulse(node: Node):
	if not node or tweens.has(node):
		return
	var tw = create_tween()
	tw.set_loops()
	tw.tween_property(node, "modulate:a", 0.3, 0.6).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(node, "modulate:a", 0.6, 0.6).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tweens[node] = tw

func _stop_pulse(node: Node):
	if not node:
		return
	if tweens.has(node):
		tweens[node].kill()
		tweens.erase(node)
	node.modulate.a = 0.0
