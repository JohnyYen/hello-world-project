class_name ExecutionEngine

# Función principal de ejecución, ahora genérica para BaseProblemContext
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
