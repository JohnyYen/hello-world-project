class_name ExecutionEngine

# Internal executor instance (uses SequentialExecutor by default)
static var _executor: Executor = null


## Get or create the default executor.
static func _get_executor() -> Executor:
	if _executor == null:
		_executor = SequentialExecutor.new()
	return _executor


## Set a custom executor for the engine.
static func set_executor(executor: Executor) -> void:
	_executor = executor


## Execute solution using the new abstraction path.
## Delegates to the configured Executor (SequentialExecutor by default).
static func execute_with_executor(solution: SolutionData, context: BaseProblemContext) -> ExecutionContext:
	var executor := _get_executor()
	return executor.execute(solution, context)


# Función principal de ejecución, ahora genérica para BaseProblemContext
# MANTENIDA PARA COMPATIBILIDAD CON CÓDIGO EXISTENTE
static func execute(blocks: Array, context: BaseProblemContext) -> BaseProblemContext:
	print("Llegueeeeeee")

	# Validar primer y último bloque
	if blocks.size() == 0:
		print("Error: No hay bloques para ejecutar")
		return context

	var first_block = blocks[0]
	var last_block = blocks[blocks.size() - 1]
	var is_valid = true
	if not first_block is StartBlock:
		print("Error: El primer bloque debe ser un StartBlock. Se encontró: ", first_block)
		is_valid = false
	if not last_block is EndBlock:
		print("Error: El último bloque debe ser un EndBlock. Se encontró: ", last_block)
		is_valid = false

	if is_valid:
		# Ejecutar los bloques
		for block in blocks:
			print("DEBUG [Execution Engine]: Ejecutando el bloque ", block)
			if block.has_method("execute"):
				block.execute(context)
				print("DEBUG [Execution Engine]: Context Outputs: ", context.outputs)
			else:
				context.log("Error: El bloque '" + block.name + "' no tiene método 'execute'")
			context.advance_pc() # Avanzar el contador de programa
	else: return null

	return context
