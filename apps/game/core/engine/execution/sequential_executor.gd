## Sequential execution strategy.
## Executes solution steps one at a time in order.
## This wraps the current ExecutionEngine behavior for backward compatibility.
class_name SequentialExecutor

## Sequential executor extends Executor (abstract)
## Note: We cannot use 'extends' with Executor here because Godot's
## class_name system has limitations with abstract inheritance.
## Instead, we match the Executor interface contract.


## Execute the solution steps in sequential order.
## @param solution: Player's solution containing ordered steps
## @param context: Problem context to execute against
## @return: ExecutionContext with results
func execute(solution: SolutionData, context: BaseProblemContext) -> ExecutionContext:
	var exec_ctx := ExecutionContext.new()
	exec_ctx.completed = false

	# Extract blocks from solution data
	var blocks: Array = []
	if solution.has("blocks"):
		blocks = solution.get_data("blocks")

	# If no blocks, can't execute
	if blocks.size() == 0:
		exec_ctx.add_error("No blocks to execute")
		return exec_ctx

	# Validate first and last block (bookends)
	var first_block = blocks[0]
	var last_block = blocks[blocks.size() - 1]
	var is_valid := true

	if not first_block is StartBlock:
		print("Error: El primer bloque debe ser un StartBlock. Se encontró: ", first_block)
		is_valid = false

	if not last_block is EndBlock:
		print("Error: El último bloque debe ser un EndBlock. Se encontró: ", last_block)
		is_valid = false

	if not is_valid:
		exec_ctx.add_error("Invalid program structure: must start with StartBlock and end with EndBlock")
		return exec_ctx

	# Execute each block sequentially
	for block in blocks:
		print("DEBUG [SequentialExecutor]: Ejecutando el bloque ", block)
		if block.has_method("execute"):
			block.execute(context)
			print("DEBUG [SequentialExecutor]: Context Outputs: ", context.outputs)
			exec_ctx.add_step(str(block), true)
		else:
			var error_msg = "Error: El bloque '" + block.name + "' no tiene método 'execute'"
			print(error_msg)
			exec_ctx.add_error(error_msg)
			exec_ctx.add_step(str(block), false)

		context.advance_pc()

	exec_ctx.completed = true
	return exec_ctx


## Check if the solution has minimum requirements for execution.
func can_execute(solution: SolutionData) -> bool:
	if not solution.has("blocks"):
		return false
	var blocks: Array = solution.get_data("blocks")
	return blocks.size() > 0
