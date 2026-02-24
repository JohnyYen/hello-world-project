extends CanvasLayer
class_name HUD

signal back_pressed
signal menu_pressed
signal reset_level

@onready var timer_label = $MarginContainer2/VBoxContainer/TopBar/TimerLabel
@onready var inventory_container = $MarginContainer/VBoxContainer/InventoryPanel/InventoryList
@onready var menu_panel : Panel = $MenuPanel

var seconds_passed := 0
var timer_running := false

func _ready():
	# Opcional: iniciar el temporizador automáticamente
	timer_running = false
func start_timer():
	timer_running = true

func stop_timer():
	timer_running = false

func reset_timer():
	seconds_passed = 0
	_update_timer_label()

func _process(delta):
	if timer_running:
		seconds_passed += delta
		_update_timer_label()

func _update_timer_label():
	var mins = int(seconds_passed) / 60
	var secs = int(seconds_passed) % 60
	timer_label.text = "%02d:%02d" % [mins, secs]

func add_inventory_item(item_name: String):
	var entry = Label.new()
	entry.text = "- " + item_name
	inventory_container.add_child(entry)

func clear_inventory():
	for child in inventory_container.get_children():
		child.queue_free()

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
