extends TemplateLevel
class_name CafeteriaLevel

signal level_setup_complete(context: CafeteriaProblemContext)

var controller : LevelOneController
var start_time : float
var _last_block_names: Array[String] = []

@export_file("*.tscn") var back_scene: String

@onready var tween: Tween = Tween.new()
@export var code_space: CodeSpace
@onready var queue_positions : Node2D = $MarginContainer/HBoxContainer/GameArea/SubViewportContainer/SubViewport/World/CustomerContainer/QueuePositions

@onready var customer_container = $MarginContainer/HBoxContainer/GameArea/SubViewportContainer/SubViewport/World/CustomerContainer
@onready var instruction_panel = $MarginContainer/Hud/PanelContainer2
@onready var instruction_label = $MarginContainer/Hud/PanelContainer2/CenterContainer/Instructions
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

# Callable para manejar action_decided (necesitamos mantener referencia para disconnect)
var _on_action_decided_callable: Callable

func _ready() -> void:
	self.controller = _GameController.create_level_controller(LevelEnum.Level.Level_One) as LevelOneController

	# NOTA: La adaptación ahora PERSISTE entre sesiones.
	# Si necesitás resetear para testing, llamá _reset_segment_1_adaptation() desde consola.

	# Connect the signal from the level controller to the code_space component
	controller.connect("send_blocks_code_zone", Callable(code_space, "receive_allowed_blocks"))
	
	modify_level_by_config(controller.get_level_configuration(self.segment_id))
	print("[ADAPT_TRACE] Config inicial cargada - segment=%d, students=%d, max_blocks=%d, desc='%s'" % [
		self.segment_id,
		controller.level_configuration.initial_state.get("student_queue", []).size(),
		controller.level_configuration.rules.get("max_blocks", 0),
		controller.level_configuration.description.left(50)
	])
	var context := controller.get_problem_context()
	
	code_space.level_config = controller.level_configuration
	
	var actor_id: String = str(_GameConfig.user.get("id", ""))
	if actor_id.is_empty():
		push_error("No authenticated user; cannot start level tracking")
		LoadingScreen.change_scene("res://scenes/pages/menu.tscn")
		return
	
	# Emit level_loaded signal for signal-based architecture (Phase 3.1)
	EventBus.level_loaded.emit(self.segment_id, self.level_number, actor_id)
	print("[CafeteriaGameplay | _ready]: level_loaded signal emit - segment_id=%d, level_number=%d, actor=%s" % [self.segment_id, self.level_number, actor_id])
	
	controller.modifier.segment_id = self.segment_id
	# Usar json_data (seed + adaptaciones) como base para el modifier
	# así las próximas modificaciones arrancan del estado adaptado actual
	controller.modifier.original_config = controller.level_configuration.json_data.duplicate(true)
	# Garantizar que attend_next_student exista si hay estudiantes en la cola
	controller.modifier.ensure_attend_action_exists(controller.level_configuration.json_data)
	
	level_setup_complete.emit(context)
	
	controller.level_completed.connect(Callable(_GameController.agent, "analyze_and_decide"))
	controller.level_completed.connect(Callable(_GameController.feedback_controller, "process_feedback"))
	
	# Conectar al action_decided con un callable que modifica y persiste la config
	# NOTA: NO se puede hacer como dos conexiones separadas porque el LevelOneController
	# se recrea en cada carga, generando conexiones huérfanas (ver Issue 2d)
	_on_action_decided_callable = func(action: String, difficulty: float):
		print("[ADAPT_TRACE] action_decided RECIBIDO - action='%s', difficulty=%.2f" % [action, difficulty])
		var modified := controller.modifier.modify_level(action, difficulty)
		print("[ADAPT_TRACE] modify_level completado - config modificada tiene %d keys" % modified.size())
		controller.modifier.apply_modifications()
		# CRITICAL: Actualizar contexto y UI con la config adaptada
		# El contexto debe recibir los nuevos expected_outputs
		controller.get_level_configuration(self.segment_id)
		controller.reset_context()
		controller.modifier.original_config = controller.level_configuration.json_data.duplicate(true)
		controller.modifier.ensure_attend_action_exists(controller.level_configuration.json_data)
		modify_level_by_config(controller.level_configuration)
		print("[ADAPT_TRACE] Contexto actualizado tras adaptación - students=%d, blocks=%d, title='%s'" % [
			controller.level_configuration.initial_state.get("student_queue", []).size(),
			controller.level_configuration.rules.get("max_blocks", 0),
			controller.level_configuration.title
		])
	EventBus.action_decided.connect(_on_action_decided_callable)
	EventBus.execution_finished.connect(_on_execution_finished)
	self.code_space.evaluate_signal.connect(_on_execute_solution)
	var initial_desc = controller.level_configuration.description
	self.show_instructions(initial_desc if not initial_desc.is_empty() else "Completa el nivel")
	
	hud.reset_level.connect(Callable(self, "_on_reset_level"))
	hud.back_pressed.connect(Callable(self, "_on_back_level"))

	_GameController.feedback_controller.hud_node = hud
	
func _exit_tree() -> void:
	# Desconectar action_decided del EventBus para evitar conexiones huérfanas
	if _on_action_decided_callable and EventBus.action_decided.is_connected(_on_action_decided_callable):
		EventBus.action_decided.disconnect(_on_action_decided_callable)
		print("[ADAPT_TRACE] action_decided desconectado de EventBus en _exit_tree")

func _on_back_level():
	var scene_path := self.back_scene
	if scene_path.begins_with("uid://"):
		scene_path = ResourceUID.get_id_path(ResourceUID.text_to_id(scene_path))

	self.hud.hide_hud()
	self.code_space.hide_code_space()
	LoadingScreen.change_scene(scene_path)
	#get_tree().change_scene_to_file(back_scene)

func _on_reset_level():
	print("[CafeteriaGameplay | _on_reset_level]: Reiniciando nivel - intentos acumulados=%d" % _attempt_count)

	# 1. Incrementar contador de reintentos en el HUD
	hud.add_attempts()

	# 2. Registrar evento de tracking
	_GameController.add_tracking_event("level_reset", {"attempt_count": _attempt_count})
	_GameController.reset_level_tracking()
	_attempt_count = 0

	# 3. Limpiar bloques colocados por el usuario en el zone de ejecución
	code_space.clear_blocks_in_zone()

	# 4. Recargar configuración desde DB (seed + adaptation_state persistido)
	controller.get_level_configuration(self.segment_id)

	# 5. Resetear backup del modifier con la config actual (seed + adaptaciones)
	#    Usamos json_data en vez de seed_data para preservar adaptaciones acumulativas
	controller.modifier.original_config = controller.level_configuration.json_data.duplicate(true)
	# Garantizar que attend_next_student exista si hay estudiantes en la cola
	controller.modifier.ensure_attend_action_exists(controller.level_configuration.json_data)

	# 6. Resetear contexto del controlador (nueva instancia de CafeteriaProblemContext)
	controller.reset_context()

	# 7. Actualizar referencia en code_space para que use la config fresca
	code_space.level_config = controller.level_configuration

	# 8. Re-aplicar configuración del nivel (limpia estudiantes, re-puebla cola, re-envía bloques)
	modify_level_by_config(controller.level_configuration)

	# 9. Resetear timer y mostrar HUD de vuelta
	hud.show_hud()

	# 10. Mostrar instrucciones del nivel
	var initial_desc := controller.level_configuration.description as String
	show_instructions(initial_desc if not initial_desc.is_empty() else "Completa el nivel")

	print("[CafeteriaGameplay | _on_reset_level]: Nivel reiniciado exitosamente")

func _on_execution_finished(final_context: CafeteriaProblemContext):
	var elapsed := (Time.get_ticks_msec() - start_time) / 1000.0
	if final_context:
		if final_context.is_solution_correct():
			print("[CafeteriaGameplay | _on_execute_solution]: SOLUCIÓN CORRECTA - completando nivel con éxito")
			_GameController.add_tracking_event("level_completed", {"success": true, "time": elapsed, "attempt": _attempt_count})
			_GameController.complete_level({
				"blocks": _last_block_names,
				"time": elapsed,
				"success": true,
				"attempt_number": _attempt_count
			})

			# Persistir progreso del nivel
			_LevelProgressManager.complete_level(self.segment_id)

			#FeedbackBalloon.show_feedback("Ganaste")
			
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
			print("[CafeteriaGameplay | _on_execute_solution]: SOLUCIÓN INCORRECTA - enviando analytics al agente adaptativo para reintento")
			# Failure path: send analytics to adaptive agent via complete_level
			# The agent receives the attempt data and adapts the level config for retry
			_GameController.complete_level({
				"blocks": _last_block_names,
				"time": elapsed,
				"success": false,
				"attempt_number": _attempt_count
			})
			hud.lose_controller.show_lose_screen()
			#FeedbackBalloon.show_feedback("Perdiste el Juego")
	else:
		print("[CafeteriaGameplay | _on_execute_solution]: CONTEXTO INVÁLIDO (null) - enviando analytics al agente adaptativo")
		# Failure path: send analytics to adaptive agent via complete_level
		_GameController.complete_level({
			"blocks": _last_block_names,
			"time": elapsed,
			"success": false,
			"attempt_number": _attempt_count
		})
		FeedbackBalloon.show_feedback("Solucion no valida")
	

func _on_execute_solution(blocks : Array[BaseBlock]):
	print("[CafeteriaGameplay | _on_execute_solution]: Ejecutando solución con %d bloques (intento #%d)" % [blocks.size(), _attempt_count + 1])
	
	_attempt_count += 1
	_GameController.begin_attempt()
	
	_last_block_names.clear()
	for block in blocks:
		_last_block_names.append(block.name)
		print("[CafeteriaGameplay | _on_execute_solution]:   Bloque: %s" % block.name)
	
	_GameController.add_tracking_event("solution_evaluated", {"blocks_count": blocks.size(), "attempt": _attempt_count})
	
	start_time = Time.get_ticks_msec()
	var final_context : CafeteriaProblemContext = await _GameController.execute_solution(blocks, self.controller.context)
	

func show_instructions(text: String) -> void:
	print("[CafeteriaGameplay | show_instructions]: Mostrando instrucciones (text_length=%d)" % text.length())
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
	print("[CafeteriaGameplay | _on_instruction_displayed]: Instrucciones mostradas al jugador")
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
	print("[CafeteriaGameplay | _on_instruction_hidden]: Instrucciones ocultas, interacciones desbloqueadas")
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
	
	
	print(config.json_data)
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
	if not allowed_blocks.is_empty():
		# Re-send blocks filtered by config's available_blocks
		var config_blocks := controller.get_avaible_blocks()
		controller.send_blocks_to_code_zone(config_blocks)
	
	_set_environment_data(config)
	# 5) UI: texto, paneles, hints
	_apply_ui_from_config(config)
	
	# 6) Reglas de ejecución: límite de bloques, tiempo, etc.
	_apply_rules_from_config(config.rules)
	
	
	
func _set_environment_data(config : LevelOneConfiguration) -> void:
	var environment_data = config.get_environment()
	if environment_data != {}:
		#push_error("Holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
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
	if queue.is_empty():
		return
	
	for i in range(queue.size()):
	
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
		
		data["node"] = inst
		data["id"] = data.get("nombre", "student_%d" % i)
		
		spawned_students.append(inst)
		
func _apply_ui_from_config(config : LevelOneConfiguration) -> void:
	# Mostrar titulo adaptado en el ProblemLabel
	var title_text = config.title if not config.title.is_empty() else config.get_display_text()
	var hud_label = $MarginContainer/HBoxContainer/Sidebar/HUD/ProblemLabel if is_instance_valid($MarginContainer/HBoxContainer/Sidebar/HUD/ProblemLabel) else null
	if hud_label:
		hud_label.text = title_text

	# Mostrar descripcion adaptada en las instrucciones
	var desc_text = config.description if not config.description.is_empty() else ""
	if not desc_text.is_empty():
		instruction_label.text = desc_text

	# Hints, messages, etc.
	var hints = config.feedback_messages.get("hints", []) if typeof(config.feedback_messages) == TYPE_DICTIONARY else []
	if hints.size() > 0:
		# mostrar primer hint en algun lugar
		var hint_label = $MarginContainer/HBoxContainer/Sidebar/HUD/HintLabel if is_instance_valid($MarginContainer/HBoxContainer/Sidebar/HUD/HintLabel) else null
		if hint_label:
			hint_label.text = hints[0]
			
func _apply_rules_from_config(rules: Dictionary) -> void:
	if typeof(rules) != TYPE_DICTIONARY:
		return
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


# -------------------------------------------------------------------------
# DEBUG: Reset adaptation_state para Segmento 1 (usa esto para testing)
# Llama esto desde la consola o desde _ready() si tenés que probar desde cero
# -------------------------------------------------------------------------
func _reset_segment_1_adaptation() -> void:
	# Solo disponible en debug builds
	if not OS.has_feature("debug"):
		return
	
	var repo := preload("res://scripts/database/repositories/level_repository.gd").new()
	var level_id := 1
	var segment_id := 1
	repo.reset_adaptation_state(level_id, segment_id)
	print("[DEBUG] reset_adaptation_state para Segmento 1 - adaptación borrada")
	
	# Recargar configuración limpia
	controller.get_level_configuration(self.segment_id)
	controller.reset_context()
	controller.modifier.original_config = controller.level_configuration.json_data.duplicate(true)
	modify_level_by_config(controller.level_configuration)
	print("[DEBUG] Segmento 1 recargado desde seed (sin adaptaciones)")
