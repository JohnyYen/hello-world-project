extends CanvasLayer
class_name VisualNovelScene

# --- Exportables / nodos ---
@onready var background = $Background
@onready var background_tint = $BackgroundTint
@onready var dialogue_box = $DialogueBox
@onready var left_char = $Characters/CharacterLeft
@onready var right_char = $Characters/CharacterRight
@onready var center_char = $Characters/CharacterCenter
@onready var music_player = $Audio

@onready var title_panel = $Panel
@onready var title = $Panel/Label
# --- Variables ---
var is_overlay: bool = false
var dialogue_runner
var dialogue_resource

signal dialogue_finished()

# --- Inicialización ---
func _ready():
	print("Inicio de los dialogos")
	# 1. Definir modo overlay o normal
	if is_overlay:
		background.visible = false
		background_tint.visible = true
	else:
		background.visible = true
		background_tint.visible = false

	# 2. Cargar el diálogo indicado por GameState
	dialogue_resource = load(_GameState.current_dialogue_path)
	# 3. Iniciar Dialogue Manager
	dialogue_runner = DialogueManager.show_dialogue_balloon(dialogue_resource, "start", [self, {"game": self}])
	
	print("DEBUG: Conectando Señales con el Dialogue Manager")
	# 4. Conectar señales de Dialogue Manager
	DialogueManager.dialogue_ended.connect(_on_end)
	
func _exit_tree():
	print("DEBUG: VisualNovelScene destruido")

func _on_line(line_data):
	# Mostrar texto en el cuadro de diálogo
	dialogue_box.show_text(line_data.text)
	
	# Mostrar el nombre del hablante
	dialogue_box.set_name(line_data.speaker)

func _on_choice(choices):
	dialogue_box.show_choices(choices)
	# Espera a que el jugador haga su selección
	# Cuando seleccione, llamar a dialogue_runner.choose(index)
	
func set_background(relative_path : String = ""):
	print("DEBUG: Mutation Background")
	var full_path = "res://assets/%s/%s" % [_GameConfig.art_style.to_lower(), relative_path]

	# Carga la textura
	var tex = load(full_path)
	if tex:
		print("DEBUG: Cambiando Background");
		background.texture = tex
	else:
		print("DEBUG: No se pudo background: %s" % full_path);
		push_error("No se pudo cargar la textura: %s" % full_path)

func set_character(side : String = "", char_name : String = ""):
	print("DEBUG: Mutation Character")
	_show_character(side, char_name)
	
func clean_character(side : String):
	match side.to_lower():
		"left", "l":
			left_char.texture = null
			left_char.visible = false

		"right", "r":
			right_char.texture = null
			right_char.visible = false

		"center", "c":
			center_char.texture = null
			center_char.visible = false

		_:
			push_warning("clean_character(): lado inválido -> %s" % side)

func set_expression(side : String = "", expression : String = ""):
	print("DEBUG: Mutation Expression")
	#_change_expression(side, expression)
	
func play_animation(animation: String = ''):
	pass 	
	
func play_music(path : String = ""):
	print("DEBUG: Mutation Music")
	_play_music(path)
	
	
func set_flag(flag : String = "", value : bool = true):
	_GameState.flags[flag] = value
	print("DEBUG [Game State]: Mutation Flag")

func _on_end(dialogue):
	print("Se termino el dialogo")
	if is_overlay:
		# Modo overlay: quitar la UI, continuar juego
		queue_free()
	else:
		# Modo normal: ir a la siguiente escena según GameState
		_GameState.on_dialogue_finished()
		
func _show_character(side: String, path: String):
	# Construye la ruta completa según el estilo de arte
	var texture_path = "res://assets/%s/%s" % [_GameConfig.art_style.to_lower(), path]

	# Carga la textura
	var tex = load(texture_path)
	if not tex:
		print("No se pudo cargar la textura: %s" % texture_path)
		push_error("No se pudo cargar la textura: %s" % texture_path)
		return

	# Asigna la textura al personaje correspondiente
	if side == "left":
		left_char.texture = tex
		left_char.visible = true
	elif side == "right":
		right_char.texture = tex
		right_char.visible = true
	elif side == "center":
		center_char.texture = tex
		center_char.visible = true
	else:
		push_error("Lado inválido: %s" % side)

func _change_expression(side: String, expression: String):
	var node = left_char if side == "left" else right_char
	node.texture = load("res://characters/%s_%s.png" % [node.name, expression])
	
func _play_music(path: String):
	var music_path = "res://assets/%s/%s" % [_GameConfig.art_style.to_lower(), path]
	var stream = load(music_path)
	
	if stream == null:
		print("❌ No se pudo cargar la música:", music_path)
		return

	# Asignar y reproducir
	var tween = create_tween()
	tween.tween_property(music_player, "volume_db", -20, 0.5)
	await tween.finished
	music_player.stream = stream
	music_player.play()
	tween = create_tween()
	tween.tween_property(music_player, "volume_db", 0, 1.0)
	print("🎵 Reproduciendo:", music_path)
	
func show_text_center(title_string: String, time: float) -> void:
	# Establece el texto y muestra el panel
	title.text = title_string
	title_panel.visible = true
	title_panel.modulate.a = 0.0

	# Crea un tween para hacer un fade-in, espera, y luego fade-out
	var tween = create_tween()
	tween.tween_property(title_panel, "modulate:a", 1.0, 0.5) # Fade in
	tween.tween_interval(time) # Mantiene el texto visible por "time" segundos
	tween.tween_property(title_panel, "modulate:a", 0.0, 0.5) # Fade out

	await tween.finished
	title_panel.visible = false

	
func show_cg(relative_path: String) -> void:
	print(relative_path)
	# Construir ruta completa
	var full_path = "res://assets/%s/%s" % [_GameConfig.art_style.to_lower(), relative_path]

	# Cargar textura
	var tex: Texture2D = load(full_path)
	if tex == null:
		push_error("No se pudo cargar el CG: %s" % full_path)
		return

	# Crear nodo de imagen a pantalla completa
	var cg_sprite := TextureRect.new()
	cg_sprite.texture = tex
	cg_sprite.z_index = 10000
	cg_sprite.stretch_mode = TextureRect.STRETCH_SCALE
	cg_sprite.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	cg_sprite.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cg_sprite.size = get_viewport().size
	cg_sprite.modulate.a = 0.0  # Arranca transparente

	add_child(cg_sprite)
	cg_sprite.move_to_front()

	# Animación profesional: Fade-in + pequeño zoom-in suave
	var tween = create_tween()
	tween.tween_property(cg_sprite, "modulate:a", 1.0, 0.6).set_trans(Tween.TRANS_SINE)
	tween.parallel().tween_property(cg_sprite, "scale", Vector2(1.05, 1.05), 1).set_trans(Tween.TRANS_SINE)

	await tween.finished
	
	# Fade-out y destrucción
	var tween2 = create_tween()
	tween2.tween_property(cg_sprite, "modulate:a", 0.0, 0.5).set_trans(Tween.TRANS_SINE)

	await tween2.finished
	cg_sprite.queue_free()


func fade_in(duration: float = 1.0):
	_Util.fade_in(duration)


func fade_out(duration: float = 1.0):
	_Util.fade_out(duration)
