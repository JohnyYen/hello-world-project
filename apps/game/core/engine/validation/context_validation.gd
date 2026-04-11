## Validation strategy that delegates to the problem context.
## Calls context.is_solution_correct() to determine success.
## This preserves the current validation behavior.
class_name ContextValidation


## Validate by delegating to the problem context's is_solution_correct().
func validate(exec_ctx: ExecutionContext, problem_ctx: BaseProblemContext) -> Dictionary:
	var is_correct := problem_ctx.is_solution_correct()

	var score := 0.0
	if is_correct:
		score = 1.0
	elif exec_ctx.has_errors():
		score = 0.0
	else:
		# Partial credit based on steps completed
		if exec_ctx.steps.size() > 0:
			var successful_steps = 0
			for step in exec_ctx.steps:
				if step.get("result") == true:
					successful_steps += 1
			score = float(successful_steps) / float(exec_ctx.steps.size())

	var feedback := _generate_feedback(is_correct, exec_ctx, problem_ctx)

	return {
		"correct": is_correct,
		"score": score,
		"feedback": feedback
	}


## Generate feedback message based on validation result.
func _generate_feedback(is_correct: bool, exec_ctx: ExecutionContext, problem_ctx: BaseProblemContext) -> String:
	if is_correct:
		return "Solucion correcta! Has completado el objetivo."

	if exec_ctx.has_errors():
		return "Error durante la ejecucion: " + exec_ctx.errors[0]

	return "La solucion no resolvio el problema correctamente. Intenta de nuevo."
