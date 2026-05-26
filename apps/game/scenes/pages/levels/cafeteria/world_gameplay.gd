extends Node2D

@export var player_node: CharacterBody2D
@export var drink_machine: Node2D
@export var bread_storage: Node2D

func _ready():
	var setup = owner
	setup.level_setup_complete.connect(_on_context_ready)

func _on_context_ready(context: CafeteriaProblemContext):
	context.attend_student.connect(Callable(self, "_on_attend_student"))
	context.prepare_bread.connect(Callable(self, "_on_prepare_bread"))
	context.get_bread.connect(Callable(self, "_on_get_bread"))
	context.serve_bread.connect(Callable(self, "_on_serve_bread"))
	context.no_students_left.connect(Callable(self, "_on_no_students_left"))
	context.player_move_to.connect(Callable(self, "_on_player_move_to"))
	context.money_added.connect(Callable(self, "_on_money_added"))
	
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
	#var player_node: CharacterBody2D = $World/PlayerZone/CharacterBody2D
	if player_node == null:
		push_error("Jugador no encontrado en PlayerZone!")
		return

	# 2️⃣ Localizar la zona de pan (despensa)
	#var bread_storage: Node2D = $World/Stations/DrinkMachine # Ajusta a la despensa correcta
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
		if anim_sprite.sprite_frames.has_animation("get_bread"):
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
