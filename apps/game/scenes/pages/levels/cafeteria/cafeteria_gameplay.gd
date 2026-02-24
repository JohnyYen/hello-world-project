extends TemplateLevel

var controller : LevelOneController

@export_file("*.tscn") var back_scene

@onready var code_space: CodeSpace = $MarginContainer/HBoxContainer/CodeArea/CodeSpace
@onready var queue_positions : Node2D = $MarginContainer/HBoxContainer/GameArea/SubViewportContainer/SubViewport/World/CustomerContainer/QueuePositions

@onready var customer_container = $MarginContainer/HBoxContainer/GameArea/SubViewportContainer/SubViewport/World/CustomerContainer
@onready var instruction_panel = $MarginContainer/Hud/PanelContainer
@onready var instruction_label = $MarginContainer/Hud/PanelContainer/CenterContainer/Instructions
@onready var hud : HUD = $MarginContainer/Hud


@export var student_scenes: Array = [
	preload("res://scenes/characters/level_one/student_1.tscn"),
	preload("res://scenes/characters/level_one/student_2.tscn"),
	preload("res://scenes/characters/level_one/student_3.tscn"),
	preload("res://scenes/characters/level_one/student_4.tscn")
]

# Mantener referencia a estudiantes instanciados para poder limpiarlos
var spawned_students: Array = []

func _ready() -> void:
	self.controller = _GameController.create_level_controller(LevelEnum.Level.Level_One) as LevelOneController

	# Connect the signal from the level controller to the code_space component
	controller.connect("send_blocks_code_zone", Callable(code_space, "receive_allowed_blocks"))
	
	modify_level_by_config(controller.get_level_configuration(self.segment_id))
	var context := controller.get_problem_context()
	
	code_space.level_config = controller.level_configuration
	
	# Request the allowed blocks for this level
	var allowed_blocks = controller.get_avaible_blocks()
	controller.send_blocks_to_code_zone(allowed_blocks)
	
	controller.modifier.segment_id = self.segment_id
	controller.modifier.original_config = controller.level_configuration.json_data

	context.attend_student.connect(Callable(self, "_on_attend_student"))
	context.prepare_bread.connect(Callable(self, "_on_prepare_bread"))
	context.get_bread.connect(Callable(self, "_on_get_bread"))
	context.serve_bread.connect(Callable(self, "_on_serve_bread"))
	context.no_students_left.connect(Callable(self, "_on_no_students_left"))
	context.player_move_to.connect(Callable(self, "_on_player_move_to"))
	context.money_added.connect(Callable(self, "_on_money_added"))
	
	controller.level_completed.connect(Callable(_GameController.agent, "analyze_and_decide"))
	controller.level_completed.connect(Callable(_GameController.feedback_controller, "process_feedback"))
	
	_GameController.agent.action_decided.connect(Callable(controller.modifier, "apply_modifications"))
	self.code_space.evaluate_signal.connect(_on_execute_solution)
	self.show_instructions(controller.level_configuration.json_data['description'])
	
	hud.reset_level.connect(Callable(self, "_on_reset_level"))
	hud.back_pressed.connect(Callable(self, "_on_back_level"))
	#controller.finish_level({})
	
	_GameController.feedback_controller.hud_node = hud
	
func _on_back_level():
	get_tree().change_scene_to_file(back_scene)

func _on_reset_level():
	print("Nivel reiniciado")
	get_tree().reload_current_scene()
	
func _on_execute_solution(blocks : Array[BaseBlock]):
	print("DEBUG [Cafeteria Gameplay]: Execute solution with: ", blocks)
	var final_context : CafeteriaProblemContext = _GameController.execute_solution(blocks, self.controller.context)
	if final_context:
		if final_context.is_solution_correct():
			controller.finish_level({})
			await get_tree().create_timer(1).timeout
			if _GameState.flags.get("has_complete_one_level", false):
				DialogueManager.show_dialogue_balloon( load("res://dialogue/C01/C01_E05_Primera_Vez_Cafeteria.dialogue"), "start")
			get_tree().change_scene_to_file(back_scene)
		else:
			_GameController.feedback_controller.show_feedback({
				"message": 'Perdiste el juego'
			})
	else:
		_GameController.feedback_controller.show_feedback({
				"message": 'Solucion no valida'
			})
	
func _on_attend_student(student: Dictionary) -> void:
	# student puede tener keys como: "id", "position", "node"
	var student_node: Node2D = student.get("node", null)
	if student_node == null:
		push_error("Student node missing for student: " + str(student))
		return

	print("DEBUG: Atendiendo al estudiante: ", student.get("id", "unknown"))

	# 1️⃣ Mover al jugador frente al estudiante
	var player_node: CharacterBody2D = $World/PlayerZone/CharacterBody2D
	var target_position: Vector2 = student_node.global_position + Vector2(-50, 0) # Ajusta offset si quieres
	player_node.global_position = target_position

	# 2️⃣ Cambiar animación a "attend" (si la tienes)
	var anim_sprite: AnimatedSprite2D = player_node.get_node("AnimatedSprite2D")
	if anim_sprite != null:
		anim_sprite.animation = "attend"
		anim_sprite.frame = 0
		anim_sprite.play()

	# 3️⃣ Marcar que el estudiante está siendo atendido
	student["being_attended"] = true

	# 4️⃣ Opcional: disparar una señal si quieres que otros sistemas reaccionen
	emit_signal("student_attended", student)

	# 5️⃣ Esperar un momento simulando el tiempo de atención (opcional, para animación)
	await get_tree().create_timer(1.0) # 1 segundo de atención

	# 6️⃣ Finalizar atención
	student["being_attended"] = false
	print("DEBUG: Estudiante atendido: ", student.get("id", "unknown"))


func _on_prepare_bread(bread_type: String) -> void:
	print("Preparando pan de tipo: ", bread_type)

func _on_get_bread() -> void:
	print("DEBUG [Cafeteria Gameplay]: Obtener pan")
	# 1️⃣ Localizar el nodo del jugador
	var player_node: CharacterBody2D = $World/PlayerZone/CharacterBody2D
	if player_node == null:
		push_error("Jugador no encontrado en PlayerZone!")
		return

	# 2️⃣ Localizar la zona de pan (despensa)
	var bread_storage: Node2D = $World/Stations/DrinkMachine # Ajusta a la despensa correcta
	if bread_storage == null:
		push_error("Zona de pan no encontrada!")
		return

	print("DEBUG: Moviendo jugador a la despensa de pan en ", bread_storage.global_position)

	# 3️⃣ Mover al jugador a la posición de la despensa
	var target_position: Vector2 = bread_storage.global_position + Vector2(0, -20) # Offset para posicionar delante
	player_node.global_position = target_position

	# 4️⃣ Cambiar animación a "get_bread" si existe
	var anim_sprite: AnimatedSprite2D = player_node.get_node("AnimatedSprite2D")
	if anim_sprite != null:
		if anim_sprite.has_animation("get_bread"):
			anim_sprite.animation = "get_bread"
			anim_sprite.frame = 0
			anim_sprite.play()
		else:
			# Si no existe la animación, usar idle o walk
			anim_sprite.animation = "idle"
			anim_sprite.frame = 0
			anim_sprite.play()

	# 5️⃣ Opcional: esperar un tiempo simulando que toma el pan
	await get_tree().create_timer(1.0) # 1 segundo

	# 6️⃣ Confirmar acción completada
	print("DEBUG: Pan obtenido del almacenamiento.")
	# Si quieres, puedes emitir señal a controller o context
	# emit_signal("bread_obtained")


func _on_serve_bread(student: Dictionary) -> void:
	print("Sirviendo pan al estudiante: ", student)

func _on_no_students_left() -> void:
	print("No hay más estudiantes en la cola.")

func _on_player_move_to(position: Vector2) -> void:
	print("El jugador se mueve a la posición: ", position)

func _on_money_added(amount: int) -> void:
	print("Se ha añadido dinero: ", amount)

# Asegúrate de importar Tween si estás en Godot 4
@onready var tween: Tween = Tween.new()

func show_instructions(text: String) -> void:
	var tween = instruction_panel.create_tween()
	# Bloquear interacciones
	#code_space.mouse_filter = Control.MOUSE_FILTER_IGNORE
	for student in spawned_students:
		if is_instance_valid(student) and student.has_method("set_process_input"):
			student.set_process_input(false)
	

	# Setear el texto
	instruction_label.text = text
	instruction_panel.visible = true
	instruction_panel.modulate.a = 0.0  # empezar transparente

	# Añadir tween si no está en la escena

	# Animación: fade in
	tween.tween_property(
		instruction_panel, "modulate:a",
		1.0, # alpha final
		0.5, # duración en segundos
	)

	# Mantener visible unos segundos y luego desbloquear
	tween.tween_callback(
		Callable(self, "_on_instruction_displayed")
	).set_delay(2.0)  # 2 segundos de lectura antes de desbloquear

func _on_instruction_displayed() -> void:
	var tween = instruction_panel.create_tween()
	# Fade out opcional
	tween.tween_property(
		instruction_panel, "modulate:a",
		0.0, 
		0.5
	)
	tween.tween_callback(
		Callable(self, "_on_instruction_hidden")
	).set_delay(0.5)  # esperar a que termine el fade out

func _on_instruction_hidden() -> void:
	instruction_panel.visible = false

	# Desbloquear interacciones
	code_space.mouse_filter = Control.MOUSE_FILTER_PASS
	for student in spawned_students:
		if is_instance_valid(student) and student.has_method("set_process_input"):
			student.set_process_input(true)

func modify_level_by_config(config : LevelOneConfiguration):
	if config == null:
		push_error("CONFIG_IS_NULL")
		return
	
	print("DEBUG [Cafeteria Gameplay]: Modificando nivel con config:", config.title)
	
	# 1) LIMPIAR lo anterior
	_clear_spawned_students()
	
	# 2) INICIALIZAR CONTEXTO (estado del juego)
	
	# 3) POBLAR la cola de estudiantes según config
	var queue := config.get_student_queue()
	_spawn_students_from_queue(queue)
	
	# 4) CONFIGURAR CodeSpace (bloques permitidos)
	var allowed_blocks := config.get_allowed_blocks()
	if allowed_blocks.is_empty():
		# fallback a los access_blocks del propio config base
		allowed_blocks = config.access_blocks
	#controller.send_blocks_to_code_zone(allowed_blocks)
	## También enviar a component local si fuera necesario
	#code_space.receive_allowed_blocks(allowed_blocks)
	
	# 5) UI: texto, paneles, hints
	_apply_ui_from_config(config)
	
	# 6) Reglas de ejecución: límite de bloques, tiempo, etc.
	_apply_rules_from_config(config.rules)
	
	print("DEBUG [Cafeteria Gameplay]: Nivel configurado.")
	
func _set_environment_data(config : LevelOneConfiguration) -> void:
	pass

func _clear_spawned_students() -> void:
	for s in spawned_students:
		if is_instance_valid(s):
			s.queue_free()
	spawned_students.clear()

# Queue es un Array de diccionarios: [{"nombre": "...", "pedido": "..."}]
func _spawn_students_from_queue(queue : Array) -> void:
	print("DEBUG [Cafeteria Gameplay]: Spawn Student in process... %s " % queue)
	
	if queue.is_empty():
		print("DEBUG [Cafeteria Gameplay]: Student Queue Empty")
		return
	
	for i in range(queue.size()):
		print("DEBUG [Cafeteria Gameplay]: Spawn Student %s" % i)
	
		var data = queue[i]
		var spawn_pos_node = queue_positions.get_child(i) if i < queue_positions.get_child_count() else null
		var scene_idx := 0
		# Puedes mapear tipo de student a scene index aquí; por ahora rotamos por student_scenes
		scene_idx = i % student_scenes.size()
		var packed = student_scenes[scene_idx]
		if packed == null:
			continue
		var inst = packed.instantiate()
		customer_container.add_child(inst)
		# Colocar en la posición del marker si existe
		if spawn_pos_node:
			var global_pos = spawn_pos_node.global_position
			# convertir a local relativo al container si hace falta
			inst.position = customer_container.to_local(global_pos)
		else:
			# fallback: posicion por defecto
			inst.position = Vector2(0, 0) + Vector2(i * 30, 0)
		
		# Configurar propiedades del estudiante (nombre, pedido) si su script lo permite
		if inst.has_method("configure"):
			inst.call("configure", data)
		else:
			# si es Node2D simple, exponer nombre/pedido como metadata
			inst.set_meta("student_data", data)
		
		spawned_students.append(inst)
		
	print("DEBUG [Cafeteria Gameplay]: Spawn Student Completed")
	
func _apply_ui_from_config(config : LevelOneConfiguration) -> void:
	# Ejemplo: mostrar texto del reto en un Label/HUD
	var display_text := config.get_display_text()
	var hud_label := $MarginContainer/HBoxContainer/Sidebar/HUD/ProblemLabel if has_node("$MarginContainer/HBoxContainer/Sidebar/HUD/ProblemLabel") else null
	print("DEBUG [Cafeteria Gameplay]: UI Config Setup")
	
	if hud_label:
		hud_label.text = display_text

	# Hints, messages, etc.
	var hints = config.feedback_messages.get("hints", []) if typeof(config.feedback_messages) == TYPE_DICTIONARY else []
	if hints.size() > 0:
		# mostrar primer hint en algun lugar
		var hint_label := $MarginContainer/HBoxContainer/Sidebar/HUD/HintLabel if has_node("$MarginContainer/HBoxContainer/Sidebar/HUD/HintLabel") else null
		if hint_label:
			hint_label.text = hints[0]
			
	print("DEBUG [Cafeteria Gameplay]: UI Config Setup Completed")
	
func _apply_rules_from_config(rules: Dictionary) -> void:
	if typeof(rules) != TYPE_DICTIONARY:
		return
	
	print("DEBUG [Cafeteria Gameplay]: Setup Rules %s" % rules)
	# ejemplo: limitar número de bloques
	var max_blocks = rules.get("max_blocks", 999)
	# enviar al controller o code_space
	if controller:
		if controller.has_method("set_max_blocks"):
			controller.call("set_max_blocks", max_blocks)
	# si hay time_limit, pasarlo al timer del nivel
	var time_limit = rules.get("time_limit", 0)
	if time_limit > 0:
		if has_node("Timer"):
			$Timer.wait_time = time_limit
			$Timer.start()
			
	print("DEBUG [Cafeteria Gameplay]: Setup Rules Completed")
