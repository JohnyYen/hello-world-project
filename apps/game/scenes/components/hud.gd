extends CanvasLayer
class_name HUD

signal back_pressed
signal menu_pressed
signal reset_level
signal add_item_inventory(item: String)


@onready var timer_label = $MarginContainer2/VBoxContainer/TopBar/TimerLabel
@onready var inventory_container = $MarginContainer/VBoxContainer/InventoryPanel/InventoryList
@onready var menu_panel : PanelContainer = $MenuPanel
@onready var timer : Timer = $MarginContainer2/VBoxContainer/TopBar/Timer

@export var inventory: InventoryHUD
@export var topbar: TopHUDController

var seconds_passed := 0
var timer_running := false
var is_countdown = false
var countdown_from := 60.0 



func _ready():
	timer.wait_time = 1.0
	timer.one_shot = false
	timer.timeout.connect(_on_timer_timeout)
	start_timer()
	
func start_timer():
	timer_running = true
	if is_countdown:
		seconds_passed = countdown_from
	timer.start()

func stop_timer():
	timer_running = false
	timer.stop()

func reset_timer():
	seconds_passed = 0
	_update_timer_label()

func _update_timer_label():
	var mins = int(seconds_passed) / 60
	var secs = int(seconds_passed) % 60
	var time = "%02d:%02d" % [mins, secs]
	timer_label.text = time

func on_back_pressed():
	emit_signal("back_pressed")


func _on_btn_menu_pressed() -> void:
	self.menu_panel.visible = true
	#get_tree().paused = true


func _on_btn_back_pressed() -> void:
	emit_signal("back_pressed")


func _on_btn_resume_pressed() -> void:
	self.menu_panel.visible = false
	#get_tree().paused = false


func _on_btn_reset_level_pressed() -> void:
	emit_signal("reset_level")
	



func _on_btn_exit_to_main_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/pages/menu.tscn")


func _on_timer_timeout():
	if not timer_running:
		return

	if is_countdown:
		seconds_passed -= 1.0
		if seconds_passed <= 0.0:
			seconds_passed = 0.0
			timer.stop()
			timer_running = false
			# Aquí puedes emitir una señal de "tiempo agotado"
	else:
		seconds_passed += 1.0
	
	_update_timer_label()

func hide_hud():
	stop_timer()
	reset_timer()
	clear_inventory()
	visible = false

func show_hud():
	visible = true
	reset_timer()
	start_timer()

# --- Inventario (delega a InventoryManager) ---
func add_inventory_item(item_name: String, qty: int = 1):
	inventory.add_inventory_item(item_name, qty)

func remove_inventory_item(item_name: String):
	inventory.remove_inventory_item(item_name)

func clear_inventory():
	inventory.clear_inventory()

func set_inventory(items: Array):
	inventory.set_inventory(items)
	
func add_attempts():
	self.topbar.add_attempts()

func add_coin(coin: int):
	self.topbar.add_coin(coin)

func set_active_coin_label(active: bool):
	self.topbar.set_active_coin(active)
