class_name TitleScreen
extends Node

@export var menu_bg      : Control
@export var logo         : Control
@export var menu_buttons : Control
@export var black_bg     : Control
@export var press_label  : Label

var waiting_for_input := true
var blink_tween : Tween

var logo_original_position : Vector2  # ← guarda la posición del editor

# Llamado por menu.gd desde su _ready()
func setup() -> void:
	await _setup_initial_state()
	_start_blink()

func _setup_initial_state() -> void:
	menu_bg.modulate.a       = 0.0
	menu_buttons.modulate.a  = 0.0
	menu_buttons.visible     = false
	logo.pivot_offset        = logo.size / 2
	
	await get_tree().process_frame
	# Guardar posición original ANTES de mover
	logo_original_position = logo.position

	# Centrar logo en pantalla
	var screen_size = get_viewport().size
	logo.position = Vector2(
		(screen_size.x - logo.size.x) / 2.0 - 40,
		(screen_size.y - logo.size.y) / 2.0
	)

	# Press label justo debajo del logo, centrado
	press_label.position = Vector2(
		(screen_size.x - press_label.size.x) / 2.0,
		logo.position.y + logo.size.y + 20.0
	)

func _start_blink() -> void:
	blink_tween = create_tween().set_loops()
	blink_tween.tween_property(press_label, "modulate:a", 0.0, 0.9)\
		.set_trans(Tween.TRANS_SINE)
	blink_tween.tween_property(press_label, "modulate:a", 1.0, 0.9)\
		.set_trans(Tween.TRANS_SINE)

func _input(event: InputEvent) -> void:
	if not waiting_for_input:
		return
	var clicked     = event is InputEventMouseButton   and event.pressed
	var key_pressed = event is InputEventKey            and event.pressed
	var pad_pressed = event is InputEventJoypadButton   and event.pressed

	if clicked or key_pressed or pad_pressed:
		_reveal_menu()

func _reveal_menu() -> void:
	waiting_for_input = false
	blink_tween.kill()

	var tween = create_tween()
	tween.tween_property(press_label,  "modulate:a",  0.0,                      0.25)
	
	# Anima de vuelta a la posición original del editor
	tween.tween_property(logo, "position", logo_original_position,         0.65)\
		.set_trans(Tween.TRANS_QUART).set_ease(Tween.EASE_OUT)
		
	tween.tween_property(menu_bg,      "modulate:a",  1.0,                      0.60)\
		.set_trans(Tween.TRANS_CUBIC)
		
	tween.tween_method(
		func(v: float): black_bg.material.set_shader_parameter("progress", v),
		0.0, 1.0, 0.8
	).set_trans(Tween.TRANS_CUBIC)

	tween.tween_callback(func(): black_bg.visible = false)
		
	tween.tween_callback(_show_buttons_staggered)

func _show_buttons_staggered() -> void:
	menu_buttons.visible = true
	menu_buttons.modulate.a = 1.0  # ← esto faltaba
	for i in menu_buttons.get_child_count():
		var btn : Control = menu_buttons.get_child(i)
		btn.modulate.a = 0.0
		var t = create_tween()
		t.tween_interval(i * 0.12)
		t.tween_property(btn, "modulate:a", 1.0, 0.35)\
			.set_trans(Tween.TRANS_CUBIC)
