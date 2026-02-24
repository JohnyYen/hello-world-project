extends CanvasLayer
## A basic dialogue balloon for use with Dialogue Manager.

## The action to use for advancing the dialogue
@export var next_action: StringName = &"ui_accept"

## The action to use to skip typing the dialogue
@export var skip_action: StringName = &"ui_cancel"

## The dialogue resource
var resource: DialogueResource

## Temporary game states
var temporary_game_states: Array = []

## See if we are waiting for the player
var is_waiting_for_input: bool = false

## See if we are running a long mutation and should hide the balloon
var will_hide_balloon: bool = false

## A dictionary to store any ephemeral variables
var locals: Dictionary = {}

var _locale: String = TranslationServer.get_locale()

## The current line
var dialogue_line: DialogueLine:
	set(value):
		if value:
			dialogue_line = value
			apply_dialogue_line()
		else:
			# The dialogue has finished so close the balloon
			queue_free()
	get:
		return dialogue_line

## A cooldown timer for delaying the balloon hide when encountering a mutation.
var mutation_cooldown: Timer = Timer.new()

## The base balloon anchor
@onready var balloon: Control = %Balloon

## The label showing the name of the currently speaking character
@onready var character_label: RichTextLabel = %CharacterLabel

## The label showing the currently spoken dialogue
@onready var dialogue_label: DialogueLabel = %DialogueLabel

## The menu of responses
@onready var responses_menu: DialogueResponsesMenu = %ResponsesMenu

@onready var audio_sfx = $AudioSFX
@onready var audio_music = $AudioMusic
@onready var background: TextureRect = $Background
@onready var title: Label = $Panel/Title
@onready var title_panel : Panel = $Panel

@onready var right_char = $Characters/CharacterRight
@onready var center_char = $Characters/CharacterCenter
@onready var left_char = $Characters/CharacterLeft

func _ready() -> void:
	balloon.hide()
	Engine.get_singleton("DialogueManager").mutated.connect(_on_mutated)
	
	_DialogueUiController.changed_background.connect(_on_changed_background)
	_DialogueUiController.changed_character.connect(_on_changed_character)
	_DialogueUiController.played_music.connect(_on_play_music)
	_DialogueUiController.set_flag.connect(_on_set_flag)
	_DialogueUiController.clean_character.connect(_on_clean_character)
	_DialogueUiController.showed_cg.connect(_on_show_cg)
	_DialogueUiController.showed_title.connect(_on_show_text_center)
	
	# If the responses menu doesn't have a next action set, use this one
	if responses_menu.next_action.is_empty():
		responses_menu.next_action = next_action

	mutation_cooldown.timeout.connect(_on_mutation_cooldown_timeout)
	add_child(mutation_cooldown)

func _on_show_text_center(title_string: String = "", time: float = 1.0) -> void:
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

func _on_show_cg(relative_path: String) -> void:
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

func _on_clean_character(side: String):
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

func _on_changed_background(path : String):
	print("DEBUG: Mutation Background")
	var full_path = "res://assets/%s/%s" % [_GameConfig.art_style.to_lower(), path]

	# Carga la textura
	var tex = load(full_path)
	if tex:
		print("DEBUG: Cambiando Background");
		background.texture = tex
	else:
		print("DEBUG: No se pudo background: %s" % full_path);
		push_error("No se pudo cargar la textura: %s" % full_path)

func _on_changed_character(side: String, path: String):
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

func _on_play_animation(animation: String = ''):
	pass 	
	
func _on_play_music(path : String = ""):
	print("DEBUG: Mutation Music")
	var music_path = "res://assets/%s/%s" % [_GameConfig.art_style.to_lower(), path]
	var stream = load(music_path)
	
	if stream == null:
		print("❌ No se pudo cargar la música:", music_path)
		return

	# Asignar y reproducir
	var tween = create_tween()
	tween.tween_property(audio_music, "volume_db", -20, 0.5)
	await tween.finished
	audio_music.stream = stream
	audio_music.play()
	tween = create_tween()
	tween.tween_property(audio_music, "volume_db", 0, 1.0)
	print("🎵 Reproduciendo:", music_path)
	
	
func _on_set_flag(flag : String = "", value : bool = true):
	_GameState.flags[flag] = value
	print("DEBUG [Game State]: Mutation Flag")

func _unhandled_input(_event: InputEvent) -> void:
	# Only the balloon is allowed to handle input while it's showing
	get_viewport().set_input_as_handled()


func _notification(what: int) -> void:
	## Detect a change of locale and update the current dialogue line to show the new language
	if what == NOTIFICATION_TRANSLATION_CHANGED and _locale != TranslationServer.get_locale() and is_instance_valid(dialogue_label):
		_locale = TranslationServer.get_locale()
		var visible_ratio = dialogue_label.visible_ratio
		self.dialogue_line = await resource.get_next_dialogue_line(dialogue_line.id)
		if visible_ratio < 1:
			dialogue_label.skip_typing()


## Start some dialogue
func start(dialogue_resource: DialogueResource, title: String, extra_game_states: Array = []) -> void:
	temporary_game_states = [self] + extra_game_states
	is_waiting_for_input = false
	resource = dialogue_resource
	self.dialogue_line = await resource.get_next_dialogue_line(title, temporary_game_states)


## Apply any changes to the balloon given a new [DialogueLine].
func apply_dialogue_line() -> void:
	mutation_cooldown.stop()

	is_waiting_for_input = false
	balloon.focus_mode = Control.FOCUS_ALL
	balloon.grab_focus()

	character_label.visible = not dialogue_line.character.is_empty()
	character_label.text = tr(dialogue_line.character, "dialogue")

	dialogue_label.hide()
	dialogue_label.dialogue_line = dialogue_line

	responses_menu.hide()
	responses_menu.responses = dialogue_line.responses

	# Show our balloon
	balloon.show()
	will_hide_balloon = false

	dialogue_label.show()
	if not dialogue_line.text.is_empty():
		dialogue_label.type_out()
		await dialogue_label.finished_typing

	# Wait for input
	if dialogue_line.responses.size() > 0:
		balloon.focus_mode = Control.FOCUS_NONE
		responses_menu.show()
	elif dialogue_line.time != "":
		var time = dialogue_line.text.length() * 0.02 if dialogue_line.time == "auto" else dialogue_line.time.to_float()
		await get_tree().create_timer(time).timeout
		next(dialogue_line.next_id)
	else:
		is_waiting_for_input = true
		balloon.focus_mode = Control.FOCUS_ALL
		balloon.grab_focus()


## Go to the next line
func next(next_id: String) -> void:
	self.dialogue_line = await resource.get_next_dialogue_line(next_id, temporary_game_states)


#region Signals


func _on_mutation_cooldown_timeout() -> void:
	if will_hide_balloon:
		will_hide_balloon = false
		balloon.hide()


func _on_mutated(_mutation: Dictionary) -> void:
	is_waiting_for_input = false
	will_hide_balloon = true
	mutation_cooldown.start(0.1)


func _on_balloon_gui_input(event: InputEvent) -> void:
	# See if we need to skip typing of the dialogue
	if dialogue_label.is_typing:
		var mouse_was_clicked: bool = event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.is_pressed()
		var skip_button_was_pressed: bool = event.is_action_pressed(skip_action)
		if mouse_was_clicked or skip_button_was_pressed:
			get_viewport().set_input_as_handled()
			dialogue_label.skip_typing()
			return

	if not is_waiting_for_input: return
	if dialogue_line.responses.size() > 0: return

	# When there are no response options the balloon itself is the clickable thing
	get_viewport().set_input_as_handled()

	if event is InputEventMouseButton and event.is_pressed() and event.button_index == MOUSE_BUTTON_LEFT:
		next(dialogue_line.next_id)
	elif event.is_action_pressed(next_action) and get_viewport().gui_get_focus_owner() == balloon:
		next(dialogue_line.next_id)


func _on_responses_menu_response_selected(response: DialogueResponse) -> void:
	next(response.next_id)


#endregion
