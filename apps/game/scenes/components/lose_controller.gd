extends Node
class_name LoseController

@export var lose_panel: PanelContainer
@export var hud: HUD

func _ready() -> void:
	lose_panel.visible = false

func show_lose_screen():
	# Congelar el juego
	get_tree().paused = true
	lose_panel.visible = true

func hide_lose_screen():
	lose_panel.visible = false
	get_tree().paused = false

# --- Botones del panel de derrota ---

func _on_btn_retry_pressed() -> void:
	hide_lose_screen()
	hud.emit_signal("reset_level")  # Reinicia el nivel (el add_attempts ya está en _on_reset_level)

func _on_btn_exit_to_menu_pressed() -> void:
	hide_lose_screen()
	LoadingScreen.change_scene("res://scenes/pages/select level/select_level_one.tscn")
