extends Panel

@onready var scroll = $Scroll
@onready var grid = $Scroll/Grid
@onready var viewer = $Viewer
@onready var viewer_image = $Viewer/TextureRect
@onready var viewer_close = $Viewer/Close
@onready var effects_layer = $OptionalEffects   # opcional si lo tienes

var images : Array = []


func _ready():
	print("[Gallery] Escena lista, inicializando...")

	viewer.visible = false
	viewer_close.pressed.connect(func(): 
		print("[Gallery] Viewer cerrado via botón")
		viewer.visible = false
	)

	_load_test_images()
	_render_gallery()


# ---------------------------------------------------------
# IMÁGENES DE PRUEBA
# ---------------------------------------------------------
func _load_test_images():
	print("[Gallery] Cargando imágenes de prueba...")

	images = [
		load("res://icon.svg"),
		load("res://assets/shared/backgrounds/pc_background.jpg"),
		load("res://assets/shared/backgrounds/pc_background.jpg")
	]

	print("[Gallery] Total imágenes cargadas: ", images.size())


# ---------------------------------------------------------
# RENDERIZAR GALERÍA
# ---------------------------------------------------------
func _render_gallery():
	print("[Gallery] Renderizando galería...")

	# Limpiar grid sin recrearlo
	for c in grid.get_children():
		c.queue_free()

	print("[Gallery] Grid limpiado.")

	for img in images:
		print("[Gallery] Añadiendo thumbnail:", img.resource_path)

		var preview : TextureButton = TextureButton.new()
		
		# 🔥 Mantener aspecto de la imagen pero obligarla a caber en un cuadro fijo
		preview.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_COVERED
		preview.ignore_texture_size = true
		# 🔥 Tamaño fijo para todos los thumbnails (el más recomendado)
		preview.size = Vector2(400, 400)
		preview.custom_minimum_size = Vector2(300, 300)
		preview.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		preview.size_flags_vertical = Control.SIZE_SHRINK_CENTER

		preview.texture_normal = img

		preview.pressed.connect(func():
			print("[Gallery] Click en thumbnail:", img.resource_path)
			_open_viewer_with_animation(preview, img)
		)

		grid.add_child(preview)

	print("[Gallery] Galería completada. Total thumbnails:", grid.get_child_count())



# ---------------------------------------------------------
# ANIMACIÓN DE APERTURA
# ---------------------------------------------------------
func _open_viewer_with_animation(preview: TextureButton, texture: Texture2D):
	print("[Gallery] Iniciando animación de apertura del viewer...")

	# 1. Obtener rect global del thumbnail
	var preview_rect = preview.get_global_rect()
	print("[Gallery] Rect inicial thumbnail:", preview_rect)

	# 2. Crear nodo temporal para animación
	var temp = TextureRect.new()
	temp.texture = texture
	temp.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	temp.global_position = preview_rect.position
	temp.size = preview_rect.size
	temp.z_index = 9999

	print("[Gallery] Nodo temporal creado para animación.")

	# Lo agregamos a un CanvasLayer para no romper layouts
	var layer = effects_layer if effects_layer else self
	layer.add_child(temp)
	print("[Gallery] Nodo temporal añadido al layer:", layer.name)

	# 3. Determinar destino (posición del viewer)
	viewer_image.texture = texture
	viewer.visible = true
	viewer.modulate.a = 0
	await get_tree().process_frame

	var target_rect = viewer_image.get_global_rect()
	print("[Gallery] Rect final del viewer:", target_rect)

	# 4. Animar con Tween
	print("[Gallery] Animando transición...")
	var tween = create_tween()
	tween.set_trans(Tween.TRANS_CUBIC)
	tween.set_ease(Tween.EASE_OUT)

	tween.tween_property(temp, "global_position", target_rect.position, 0.4)
	tween.tween_property(temp, "size", target_rect.size, 0.4)
	tween.tween_property(viewer, "modulate:a", 1.0, 0.25).set_delay(0.25)

	await tween.finished

	print("[Gallery] Animación completada.")

	# 5. Limpiar
	temp.queue_free()
	print("[Gallery] Nodo temporal eliminado.")


# ---------------------------------------------------------
# CERRAR VIEWER
# ---------------------------------------------------------
func _on_close_pressed():
	print("[Gallery] Cierre del viewer mediante función _on_close_pressed")
	viewer.visible = false


func _on_back_pressed() -> void:
	print("[Gallery] Saliendo de la aplicación de galería.")
	self.visible = false
