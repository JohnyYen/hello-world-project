extends Control

@export var level_number: int = 1
@export var is_unlocked: bool = true
@export var is_completed: bool = false
@export var stars: int = 0
@export var icon_texture: Texture2D
@export var locked_texture: Texture2D
@export var completed_texture: Texture2D
@export var hover_scale: float = 1.1

@onready var btn : TextureButton = $BackgroundBtn
@onready var label : Label = $BackgroundBtn/LevelNumber
@onready var icon_lock: TextureRect = $IconLock
@onready var icon_start: TextureRect = $IconStar
@onready var animation_player : AnimationPlayer = $AnimationPlayer

func _ready():
	update_visuals()
	btn.pressed.connect(_on_button_pressed)

func _on_button_pressed():
	pass
	
func update_visuals():
	if is_unlocked:
		btn.texture_normal = icon_texture
		icon_lock.visible = false
	else:
		btn.texture_normal = locked_texture
		icon_lock.visible = true
		# Actualizar estrellas o icono completado
		icon_start.visible = is_completed
		
	label.text = str(level_number)
	
