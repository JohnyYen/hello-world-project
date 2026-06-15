extends Control

## Botón individual de nivel en la pantalla de selección.
## Consulta su estado (unlocked/completed/stars) al _LevelProgressManager
## usando segment_id como identificador.

@export var segment_id: int = 0
@export var level_number: int = 1
@export var icon_texture: Texture2D
@export var locked_texture: Texture2D
@export var completed_texture: Texture2D
@export var hover_scale: float = 1.1

# Estado dinámico consultado al _LevelProgressManager
var is_unlocked: bool = false
var is_completed: bool = false
var stars: int = 0

@onready var btn: TextureButton = $BackgroundBtn
@onready var label: Label = $BackgroundBtn/LevelNumber
@onready var icon_lock: TextureRect = $IconLock
@onready var icon_star: TextureRect = $IconStar
@onready var animation_player: AnimationPlayer = $AnimationPlayer


func _ready() -> void:
	refresh_state()
	btn.pressed.connect(_on_button_pressed)


## Refresca el estado del botón consultando al _LevelProgressManager.
func refresh_state() -> void:
	is_unlocked = _LevelProgressManager.is_level_unlocked(segment_id)
	is_completed = _LevelProgressManager.is_level_completed(segment_id)
	stars = _LevelProgressManager.get_level_stars(segment_id)
	update_visuals()


func _on_button_pressed() -> void:
	if not is_unlocked:
		# Opcional: reproducir sonido de error o animación de sacudida
		if animation_player:
			animation_player.play("locked_shake")
		return

	# La navegación la maneja el script padre (select_level_template)
	# conectándose directamente a btn.pressed


func update_visuals() -> void:
	if not is_unlocked:
		btn.texture_normal = locked_texture if locked_texture else null
		icon_lock.visible = true
		icon_star.visible = false
		btn.disabled = true
	elif is_completed:
		btn.texture_normal = completed_texture if completed_texture else icon_texture
		icon_lock.visible = false
		icon_star.visible = true
		btn.disabled = false
	else:
		btn.texture_normal = icon_texture
		icon_lock.visible = false
		icon_star.visible = false
		btn.disabled = false

	label.text = str(level_number)
