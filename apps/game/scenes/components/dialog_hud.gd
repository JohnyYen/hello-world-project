extends CanvasLayer

@export var chapter_label: Label 
@export var menu_button:MenuButton

func _ready():
	# Capítulo invisible al inicio, se muestra al cambiar de escena
	chapter_label.modulate.a = 0

func show_chapter(text: String, duration: float = 4.0):
	chapter_label.text = text
	chapter_label.visible = true
	
	var tween = create_tween().set_ease(Tween.EASE_OUT)
	# Fade in
	tween.tween_property(chapter_label, "modulate:a", 1.0, 0.5)
	# Esperar
	tween.tween_interval(duration - 1.0)
	# Fade out
	tween.tween_property(chapter_label, "modulate:a", 0.0, 0.5)
	tween.tween_callback(func(): chapter_label.visible = false)

func _on_menu_pressed():
	# Abrir menú de pausa
	get_tree().paused = true
	# Instanciar o mostrar menú
