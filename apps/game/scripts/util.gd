extends CanvasLayer
class_name Util

# Rectángulo de color que cubre toda la pantalla
@onready var fade_rect: ColorRect = ColorRect.new()

func _ready():
	print("DEBUG [Util]: Inicializando fade_rect")

	fade_rect.color = Color(0, 0, 0, 0)
	fade_rect.size = get_viewport().size
	fade_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	fade_rect.visible = false  # crucial

	add_child(fade_rect)
	move_child(fade_rect, get_child_count() - 1)

	get_viewport().size_changed.connect(_on_viewport_resized)

	print("DEBUG [Util]: fade_rect creado. Visible =", fade_rect.visible, 
		" Alpha =", fade_rect.color.a, 
		" Size =", fade_rect.size)


func _on_viewport_resized():
	fade_rect.size = get_viewport().size
	print("DEBUG [Util]: Viewport resized. Nuevo tamaño =", fade_rect.size)


# ------------------------------
# FADE OUT (oscurece la pantalla)
# ------------------------------
func fade_out(duration: float = 1.0) -> void:
	print("DEBUG [Util]: Iniciando fade OUT. Duración =", duration)

	fade_rect.visible = true
	print("DEBUG [Util]: fade_rect.visible =", fade_rect.visible)

	var tween = create_tween()
	print("DEBUG [Util]: Tween OUT creado")

	tween.tween_property(fade_rect, "color:a", 1.0, duration)

	print("DEBUG [Util]: Esperando fin de tween OUT...")
	await tween.finished
	
	print("DEBUG [Util]: Esperando un frame adicional antes de ocultar rect...")
	await get_tree().process_frame

	fade_rect.visible = false
	fade_rect.color.a = 0.0
	print("DEBUG [Util]: Fade OUT completado. Alpha actual =", fade_rect.color.a)


# ------------------------------
# FADE IN (aclara la pantalla)
# ------------------------------
func fade_in(duration: float = 1.0) -> void:
	print("DEBUG [Util]: Iniciando fade IN. Duración =", duration)

	fade_rect.visible = true
	print("DEBUG [Util]: fade_rect.visible =", fade_rect.visible)

	fade_rect.color = Color(0, 0, 0, 1.0)
	print("DEBUG [Util]: Estado inicial fade IN. Alpha =", fade_rect.color.a)

	var tween = create_tween()
	print("DEBUG [Util]: Tween IN creado")

	tween.tween_property(fade_rect, "color:a", 0.0, duration)

	print("DEBUG [Util]: Esperando fin de tween IN...")
	await tween.finished
	print("DEBUG [Util]: Tween IN terminado. Alpha =", fade_rect.color.a)

	# Frame extra por el cambio de escena
	print("DEBUG [Util]: Esperando un frame adicional antes de ocultar rect...")
	await get_tree().process_frame

	fade_rect.visible = false
	fade_rect.color.a = 0.0

	print("DEBUG [Util]: Fade IN completado. Rect oculto:",
		"Visible =", fade_rect.visible, 
		"Alpha =", fade_rect.color.a)


# ------------------------------
# FADE OUT DE MÚSICA
# ------------------------------
func fade_out_music(audio: AudioStreamPlayer2D, duration: float = 1.0):
	print("DEBUG [Util]: Fade out music START")

	if not audio.playing:
		print("DEBUG [Util]: Audio no está reproduciéndose. Abortando fade.")
		return

	var tween = create_tween()
	tween.tween_property(audio, "volume_db", -30.0, duration)
	tween.tween_callback(audio.stop)

	print("DEBUG [Util]: Fade out music tween creado. Bajando volumen.")

	await tween.finished

	print("DEBUG [Util]: Fade out music COMPLETADO. Audio detenido.")
