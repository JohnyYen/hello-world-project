extends BaseLevelModifier
class_name LevelOneModifier

func _init() -> void:
	super()

func modify_level(state: String, difficulty : float):
	print("LevelOneModifier.modify_level called with state =", state)
	var new_config = {}
	match state:
		"decrease":
			new_config = _apply_easy_changes()
		"increase":
			new_config = _apply_hard_changes()
		"keep":
			new_config = _apply_maintain_changes()
		_:
			push_error("Invalid difficulty state")
	if not new_config.is_empty():
		var result = repo.update_configuration_segment(1, self.segment_id, new_config)
		print("DEBUG [Level One Modifier]: Result of Query: ", result)
		if result:
			print("DEBUG [Level One Modifier]: Guardando nueva configuracion")
			
	print("LevelOneModifier.modify_level finished")


# -------------------------------------------------------
#  EASY MODE  → hacer el nivel más sencillo
# -------------------------------------------------------

func _apply_easy_changes() -> Dictionary:
	var cfg = self.original_config
	
	# 1️⃣ Aumentar bloques con variación
	var inc_blocks = _rand_adjust(1, 4)
	cfg.execution_rules.max_blocks += inc_blocks
	print("EASY: Blocks +", inc_blocks)

	# 2️⃣ Reducir número de estudiantes (random si hay más de 1)
	while cfg.initial_state.student_queue.size() > _rand_adjust(1, 2):
		cfg.initial_state.student_queue.pop_back()

	# 3️⃣ Añadir inventario fijo
	cfg.initial_state.inventory = ["pan", "cafe"]

	# 4️⃣ Nueva pista aleatoria
	var possible_hints = [
		"Recuerda revisar el pedido antes de ejecutarlo.",
		"Piensa en el orden de las acciones.",
		"No necesitas usar todos los bloques."
	]

	cfg.feedback_messages.hints.append(
		possible_hints[_rand_adjust(0, possible_hints.size() - 1)]
	)

	# 5️⃣ Asegurar dispensadores con contenido
	cfg.initial_state.stations.bread_dispenser = ["pan"]
	cfg.initial_state.stations.drink_dispenser = ["cafe"]
	
	return cfg



# -------------------------------------------------------
#  HARD MODE  → hacer el nivel más desafiante
# -------------------------------------------------------

func _apply_hard_changes() -> Dictionary:
	var cfg = original_config

	# 1️⃣ Reducir bloques permitidos con variación
	var dec_blocks = _rand_adjust(1, 3)
	cfg.execution_rules.max_blocks = max(
		6, 
		cfg.execution_rules.max_blocks - dec_blocks
	)
	print("HARD: Blocks -", dec_blocks)

	# 2️⃣ Añadir un nuevo estudiante aleatorio
	var extra_students = [
		{"nombre": "Luisa", "pedido": "pan"},
		{"nombre": "Carlos", "pedido": "cafe"},
		{"nombre": "Ana", "pedido": "pan"},
	]

	cfg.initial_state.student_queue.append(
		extra_students[_rand_adjust(0, extra_students.size() - 1)]
	)

	# 3️⃣ Inventario vacío
	cfg.initial_state.inventory = []

	# 4️⃣ Quitar pistas hasta dejar entre 0 y 1
	var new_size = _rand_adjust(0, 1)
	while cfg.feedback_messages.hints.size() > new_size:
		cfg.feedback_messages.hints.pop_back()

	# 5️⃣ Desabastecer dispensadores
	if randi() % 2 == 0:
		cfg.initial_state.stations.bread_dispenser = []
	else:
		cfg.initial_state.stations.drink_dispenser = []
	
	return cfg


# -------------------------------------------------------
#  MAINTAIN MODE  → cambios sutiles
# -------------------------------------------------------

func _apply_maintain_changes() -> Dictionary:
	var cfg = original_config

	# Cambio leve (0 o 1 bloque más)
	var adjust = _rand_adjust(0, 1)
	cfg.execution_rules.max_blocks += adjust

	# Reorganizar pistas de forma aleatoria
	cfg.feedback_messages.hints.shuffle()

	# Metadata para saber que se mantuvo
	cfg.version = str(cfg.version) + ".maintained"
	
	return cfg
