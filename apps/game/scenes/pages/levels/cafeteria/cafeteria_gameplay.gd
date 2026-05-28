extends TemplateLevel

signal level_setup_complete(context: CafeteriaProblemContext)

var controller : LevelOneController

@export_file("*.tscn") var back_scene: String

@onready var tween: Tween = Tween.new()
@export var code_space: CodeSpace
@onready var queue_positions : Node2D = $MarginContainer/HBoxContainer/GameArea/SubViewportContainer/SubViewport/World/CustomerContainer/QueuePositions

@onready var customer_container = $MarginContainer/HBoxContainer/GameArea/SubViewportContainer/SubViewport/World/CustomerContainer
@onready var instruction_panel = $MarginContainer/Hud/PanelContainer
@onready var instruction_label = $MarginContainer/Hud/PanelContainer/CenterContainer/Instructions
@export var hud : HUD

@export var drink_machine : Node2D
@export var bread_station : Node2D
@export var cash_register : Node2D

@export var student_scenes: Array = [
	preload("res://scenes/characters/level_one/student_1.tscn"),
	preload("res://scenes/characters/level_one/student_2.tscn"),
	preload("res://scenes/characters/level_one/student_3.tscn"),
	preload("res://scenes/characters/level_one/student_4.tscn")
]

# Mantener referencia a estudiantes instanciados para poder limpiarlos
var spawned_students: Array = []
var _attempt_count: int = 0

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
	
	var actor_id: String = _GameState.player_data.get("name", "player")
	_GameController.begin_segment(self.segment_id, actor_id)
	
	controller.modifier.segment_id = self.segment_id
	controller.modifier.original_config = controller.level_configuration.json_data
	
	level_setup_complete.emit(context)
	
	controller.level_completed.connect(Callable(_GameController.agent, "analyze_and_decide"))
	controller.level_completed.connect(Callable(_GameController.feedback_controller, "process_feedback"))
	
	_GameController.agent.action_decided.connect(Callable(controller.modifier, "apply_modifications"))
	self.code_space.evaluate_signal.connect(_on_execute_solution)
	self.show_instructions(controller.level_configuration.json_data['description'])
	
	hud.reset_level.connect(Callable(self, "_on_reset_level"))
	hud.back_pressed.connect(Callable(self, "_on_back_level"))

	_GameController.feedback_controller.hud_node = hud
	
func _on_back_level():
	var scene_path := self.back_scene
	if scene_path.begins_with("uid://"):
		scene_path = ResourceUID.get_id_path(ResourceUID.text_to_id(scene_path))

	self.hud.hide_hud()
	self.code_space.hide_code_space()
	LoadingScreen.change_scene(scene_path)
	#get_tree().change_scene_to_file(back_scene)

func _on_reset_level():
	_GameController.add_tracking_event("level_reset", {"attempt_count": _attempt_count})
	_GameController.reset_level_tracking()
	_attempt_count = 0
	self.hud.hide_hud()
	self.code_space.hide_code_space()
	
	LoadingScreen.change_scene("res://scenes/pages/select level/select_level_one.tscn")
	#get_tree().call_deferred("change_scene_to_file", scene_path)
	
func _on_execute_solution(blocks : Array[BaseBlock]):
	print("DEBUG [Cafeteria Gameplay]: Execute solution with: ", blocks)
	
	_attempt_count += 1
	_GameController.begin_attempt()
	
	var block_names: Array[String] = []
	for block in blocks:
		block_names.append(block.name)
	
	_GameController.add_tracking_event("solution_evaluated", {"blocks_count": blocks.size(), "attempt": _attempt_count})
	
	var start_time := Time.get_ticks_msec()
	var final_context : CafeteriaProblemContext = _GameController.execute_solution(blocks, self.controller.context)
	var elapsed := (Time.get_ticks_msec() - start_time) / 1000.0
	
	if final_context:
		if final_context.is_solution_correct():
			_GameController.add_tracking_event("level_completed", {"success": true, "time": elapsed, "attempt": _attempt_count})
			_GameController.complete_level({
				"blocks": block_names,
				"time": elapsed,
				"success": true,
				"attempt_number": _attempt_count
			})
			
			FeedbackBalloon.show_feedback("Ganaste")
			
			await get_tree().create_timer(1).timeout
			if _GameState.flags.get("has_complete_one_level", false):
				DialogueManager.show_dialogue_balloon( load("res://dialogue/C01/C01_E05_Primera_Vez_Cafeteria.dialogue"), "start")
			var scene_path := self.back_scene
			if scene_path.begins_with("uid://"):
				scene_path = ResourceUID.get_id_path(ResourceUID.text_to_id(scene_path))
				
			self.hud.hide_hud()
			self.code_space.hide_code_space()
			LoadingScreen.change_scene(scene_path)
		else:
			# Failure path: send analytics to adaptive agent via complete_level
			# The agent receives the attempt data and adapts the level config for retry
			_GameController.complete_level({
				"blocks": block_names,
				"time": elapsed,
				"success": false,
				"attempt_number": _attempt_count
			})
			FeedbackBalloon.show_feedback("Perdiste el Juego")
	else:
		# Failure path: send analytics to adaptive agent via complete_level
		_GameController.complete_level({
			"blocks": block_names,
			"time": elapsed,
			"success": false,
			"attempt_number": _attempt_count
		})
		FeedbackBalloon.show_feedback("Solucion no valida")
	

func show_instructions(text: String) -> void:
	_GameController.add_tracking_event("instruction_shown", {"text_length": text.length()})
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
	_GameController.add_tracking_event("instruction_displayed", {})
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
	_GameController.add_tracking_event("instruction_dismissed", {})
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
	
	_set_environment_data(config)
	# 5) UI: texto, paneles, hints
	_apply_ui_from_config(config)
	
	# 6) Reglas de ejecución: límite de bloques, tiempo, etc.
	_apply_rules_from_config(config.rules)
	
	print("DEBUG [Cafeteria Gameplay]: Nivel configurado.")
	
func _set_environment_data(config : LevelOneConfiguration) -> void:
	var environment_data = config.get_environment()
	if environment_data != {}:
		drink_machine.visible = environment_data.get("drink_machine", true)
		bread_station.visible = environment_data.get("bread_station", true)
		cash_register.visible = environment_data.get("cash_register", true)

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
