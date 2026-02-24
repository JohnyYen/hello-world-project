# Transicion.gd
extends CanvasLayer

@onready var color_rect: ColorRect = $ColorRect

func fade_in():
	var tween = create_tween()
	tween.tween_property(color_rect, "color:a", 1.0, 0.5)  # Fade a negro
	await tween.finished

func fade_out():
	var tween = create_tween()
	tween.tween_property(color_rect, "color:a", 0.0, 0.5)  # Fade a transparente
	await tween.finished
