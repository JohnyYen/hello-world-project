class_name HoverTransparencyEffect
extends Node

## Efecto genérico de hover que cambia la transparencia al pasar el mouse.
## Agrega este script como hijo de cualquier Control o Node2D.
## Para Node2D: asegúrate de que tenga un Area2D con CollisionShape para detectar el mouse.

@export_group("Transparencia")
## Opacidad normal (sin hover). 0 = invisible, 1 = opaco.
@export_range(0.0, 1.0, 0.01) var normal_alpha: float = 1.0
## Opacidad al hacer hover. 0 = invisible, 1 = opaco.
@export_range(0.0, 1.0, 0.01) var hover_alpha: float = 0.6

@export_group("Transiciones")
## Duración del fade en segundos.
@export_range(0.0, 2.0, 0.01) var fade_duration: float = 0.15
## Curva de interpolación para la transición.
@export var transition_type: Tween.TransitionType = Tween.TRANS_LINEAR
## Tipo de easing para la transición.
@export var ease_type: Tween.EaseType = Tween.EASE_IN_OUT

@export_group("Configuración Avanzada")
## Si es true, el efecto funciona en modo "toggle" (click para activar/desactivar hover).
@export var toggle_mode: bool = false
## Si es true, aplica el efecto también a los hijos del nodo objetivo.
@export var affect_children: bool = false

var _is_hovered: bool = false
var _is_toggled: bool = false
var _current_tween: Tween
var _target_node: Node


func _ready() -> void:
	print("=== HOVER TRANSPARENCY DEBUG ===")
	print("[READY] Script iniciado en: ", self.name)
	print("[READY] Ruta: ", get_path())
	
	_target_node = get_parent()
	print("[READY] Nodo padre: ", _target_node.name)
	print("[READY] Tipo de nodo padre: ", _target_node.get_class())
	
	# Validación mejorada: verificar que el nodo tenga la propiedad modulate
	if not _has_modulate(_target_node):
		push_error("[READY] ERROR: El nodo padre '%s' no tiene propiedad 'modulate'. " % _target_node.name + 
			"Este script solo funciona con nodos que hereden de CanvasItem.")
		print("[READY] ERROR: Nodo padre no es CanvasItem. Script detenido.")
		return
	
	print("[READY] OK: Nodo padre tiene modulate")
	print("[READY] Modulate actual: ", _target_node.modulate)
	print("[READY] Alpha actual: ", _target_node.modulate.a)
	
	# Configurar detección de mouse según el tipo de nodo
	_setup_mouse_detection()
	
	# Aplicar alpha inicial
	print("[READY] Aplicando alpha inicial: ", normal_alpha)
	_apply_alpha(normal_alpha)
	print("[READY] Alpha después de aplicar: ", _target_node.modulate.a)
	print("=== FIN DEBUG READY ===")


func _has_modulate(node: Node) -> bool:
	var result = node is CanvasItem
	print("[HAS_MODULATE] Nodo: ", node.name, " | Es CanvasItem: ", result)
	return result


func _setup_mouse_detection() -> void:
	print("[SETUP] Configurando detección de mouse...")
	
	# Para nodos Control (UI): usan señales nativas mouse_entered/mouse_exited
	if _target_node is Control:
		print("[SETUP] Nodo padre es Control")
		var control_node := _target_node as Control
		var previous_filter = control_node.mouse_filter
		print("[SETUP] Mouse filter anterior: ", previous_filter)
		
		# Asegurar que el control reciba input de mouse
		control_node.mouse_filter = Control.MOUSE_FILTER_STOP
		print("[SETUP] Mouse filter cambiado a: STOP")
		
		# Conectar señales
		if not control_node.mouse_entered.is_connected(_on_mouse_entered):
			control_node.mouse_entered.connect(_on_mouse_entered)
			print("[SETUP] Señal mouse_entered CONECTADA")
		else:
			print("[SETUP] Señal mouse_entered YA estaba conectada")
			
		if not control_node.mouse_exited.is_connected(_on_mouse_exited):
			control_node.mouse_exited.connect(_on_mouse_exited)
			print("[SETUP] Señal mouse_exited CONECTADA")
		else:
			print("[SETUP] Señal mouse_exited YA estaba conectada")
			
		if not control_node.gui_input.is_connected(_on_gui_input):
			control_node.gui_input.connect(_on_gui_input)
			print("[SETUP] Señal gui_input CONECTADA")
		else:
			print("[SETUP] Señal gui_input YA estaba conectada")
		
		print("[SETUP] Control configurado correctamente - '", _target_node.name, "'")
	
	# Para nodos Node2D: requieren un Area2D hijo para detección
	elif _target_node is Node2D:
		print("[SETUP] Nodo padre es Node2D")
		var area := _find_area2d()
		if area:
			print("[SETUP] Area2D encontrado: ", area.name)
			if not area.mouse_entered.is_connected(_on_mouse_entered):
				area.mouse_entered.connect(_on_mouse_entered)
				print("[SETUP] Señal mouse_entered CONECTADA a Area2D")
			if not area.mouse_exited.is_connected(_on_mouse_exited):
				area.mouse_exited.connect(_on_mouse_exited)
				print("[SETUP] Señal mouse_exited CONECTADA a Area2D")
			if not area.input_event.is_connected(_on_input_event):
				area.input_event.connect(_on_input_event)
				print("[SETUP] Señal input_event CONECTADA a Area2D")
			print("[SETUP] Node2D configurado correctamente - '", _target_node.name, "'")
		else:
			push_error("[SETUP] ERROR: Node2D '%s' requiere un Area2D hijo para detección de mouse." % _target_node.name)
			print("[SETUP] ERROR: No se encontró Area2D hijo")
	else:
		push_error("[SETUP] ERROR: El nodo padre '%s' no es Control ni Node2D." % _target_node.name)
		print("[SETUP] ERROR: Tipo de nodo no soportado")


func _find_area2d() -> Area2D:
	print("[FIND_AREA2D] Buscando Area2D en hijos de: ", _target_node.name)
	for child in _target_node.get_children():
		print("[FIND_AREA2D] Revisando hijo: ", child.name, " | Tipo: ", child.get_class())
		if child is Area2D:
			print("[FIND_AREA2D] Area2D ENCONTRADO: ", child.name)
			return child
	print("[FIND_AREA2D] Area2D NO encontrado")
	return null


func _on_mouse_entered() -> void:
	print("[MOUSE_ENTERED] ========================================")
	print("[MOUSE_ENTERED] Nodo: ", _target_node.name)
	print("[MOUSE_ENTERED] _is_hovered antes: ", _is_hovered)
	_is_hovered = true
	print("[MOUSE_ENTERED] _is_hovered después: ", _is_hovered)
	print("[MOUSE_ENTERED] toggle_mode: ", toggle_mode)
	if not toggle_mode:
		print("[MOUSE_ENTERED] Llamando _fade_to(hover_alpha): ", hover_alpha)
		_fade_to(hover_alpha)
	else:
		print("[MOUSE_ENTERED] Modo toggle activo, ignorando fade")


func _on_mouse_exited() -> void:
	print("[MOUSE_EXITED] ========================================")
	print("[MOUSE_EXITED] Nodo: ", _target_node.name)
	print("[MOUSE_EXITED] _is_hovered antes: ", _is_hovered)
	_is_hovered = false
	print("[MOUSE_EXITED] _is_hovered después: ", _is_hovered)
	print("[MOUSE_EXITED] toggle_mode: ", toggle_mode)
	if not toggle_mode:
		print("[MOUSE_EXITED] Llamando _fade_to(normal_alpha): ", normal_alpha)
		_fade_to(normal_alpha)
	else:
		print("[MOUSE_EXITED] Modo toggle activo, ignorando fade")


func _on_gui_input(event: InputEvent) -> void:
	print("[GUI_INPUT] Evento recibido en: ", _target_node.name)
	print("[GUI_INPUT] Tipo de evento: ", event.get_class())
	if toggle_mode and event is InputEventMouseButton:
		var mouse_event := event as InputEventMouseButton
		print("[GUI_INPUT] Es mouse button. Botón: ", mouse_event.button_index, " | Presionado: ", mouse_event.pressed)
		if mouse_event.button_index == MOUSE_BUTTON_LEFT and mouse_event.pressed:
			_is_toggled = not _is_toggled
			print("[GUI_INPUT] Toggle cambiado a: ", _is_toggled)
			_fade_to(hover_alpha if _is_toggled else normal_alpha)
	else:
		print("[GUI_INPUT] No es toggle o no es mouse button")


func _on_input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
	print("[INPUT_EVENT] Evento recibido en Area2D de: ", _target_node.name)
	print("[INPUT_EVENT] Tipo de evento: ", event.get_class())
	if toggle_mode and event is InputEventMouseButton:
		var mouse_event := event as InputEventMouseButton
		print("[INPUT_EVENT] Es mouse button. Botón: ", mouse_event.button_index, " | Presionado: ", mouse_event.pressed)
		if mouse_event.button_index == MOUSE_BUTTON_LEFT and mouse_event.pressed:
			_is_toggled = not _is_toggled
			print("[INPUT_EVENT] Toggle cambiado a: ", _is_toggled)
			_fade_to(hover_alpha if _is_toggled else normal_alpha)


func _fade_to(target_alpha: float) -> void:
	print("[FADE_TO] ========================================")
	print("[FADE_TO] Target alpha: ", target_alpha)
	print("[FADE_TO] fade_duration: ", fade_duration)
	print("[FADE_TO] transition_type: ", transition_type)
	print("[FADE_TO] ease_type: ", ease_type)
	
	# Cancelar tween anterior si existe
	if _current_tween and _current_tween.is_valid():
		print("[FADE_TO] Matando tween anterior")
		_current_tween.kill()
	else:
		print("[FADE_TO] No hay tween anterior que matar")
	
	_current_tween = create_tween()
	print("[FADE_TO] Nuevo tween creado")
	_current_tween.set_trans(transition_type)
	_current_tween.set_ease(ease_type)
	print("[FADE_TO] Tween configurado con trans y ease")
	
	var target_nodes: Array[Node] = [_target_node]
	print("[FADE_TO] Nodos objetivo inicial: ", target_nodes.size())
	
	if affect_children:
		var children = _target_node.get_children()
		print("[FADE_TO] Affect_children activo. Hijos encontrados: ", children.size())
		target_nodes.append_array(children)
		print("[FADE_TO] Total nodos objetivo: ", target_nodes.size())
	else:
		print("[FADE_TO] Affect_children desactivado")
	
	var nodes_processed := 0
	for node in target_nodes:
		print("[FADE_TO] Procesando nodo: ", node.name, " | Tipo: ", node.get_class())
		if _has_modulate(node):
			var final_color = node.modulate
			print("[FADE_TO] Modulate actual: ", final_color)
			final_color.a = target_alpha
			print("[FADE_TO] Modulate final: ", final_color)
			_current_tween.parallel().tween_property(node, "modulate", final_color, fade_duration)
			print("[FADE_TO] Tween property agregado para: ", node.name)
			nodes_processed += 1
		else:
			print("[FADE_TO] Nodo ignorado (no tiene modulate): ", node.name)
	
	print("[FADE_TO] Nodos procesados: ", nodes_processed)
	print("[FADE_TO] ========================================")


func _apply_alpha(alpha: float) -> void:
	print("[APPLY_ALPHA] Aplicando alpha: ", alpha)
	var target_nodes: Array[Node] = [_target_node]
	print("[APPLY_ALPHA] Nodos objetivo inicial: ", target_nodes.size())
	
	if affect_children:
		var children = _target_node.get_children()
		target_nodes.append_array(children)
		print("[APPLY_ALPHA] Total con hijos: ", target_nodes.size())
	
	for node in target_nodes:
		print("[APPLY_ALPHA] Procesando: ", node.name)
		if _has_modulate(node):
			var old_alpha = node.modulate.a
			node.modulate.a = alpha
			print("[APPLY_ALPHA] Alpha cambiado de ", old_alpha, " a ", alpha, " en: ", node.name)
		else:
			print("[APPLY_ALPHA] Ignorado (no tiene modulate): ", node.name)


func set_hovered(hovered: bool) -> void:
	"""Método público para forzar el estado de hover desde código."""
	print("[SET_HOVERED] Forzando hover a: ", hovered)
	_is_hovered = hovered
	if not toggle_mode:
		_fade_to(hover_alpha if hovered else normal_alpha)
	else:
		print("[SET_HOVERED] Modo toggle activo, no se aplica fade")


func is_hovered() -> bool:
	return _is_hovered
