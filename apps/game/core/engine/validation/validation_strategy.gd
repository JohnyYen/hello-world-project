## Abstract base class for solution validation strategies.
## Defines HOW a solution is judged as correct or incorrect.
##
## Subclasses MUST implement validate().
## Examples of concrete implementations:
##   - ContextValidation: Delegates to context.is_solution_correct() (current)
##   - ExactMatchValidation: Compare outputs to expected outputs
##   - ScoringValidation: Score-based threshold validation
##   - RubricValidation: Multi-criteria weighted validation
class_name ValidationStrategy


## Validate the execution result against the problem context.
## MUST be overridden by subclasses.
## @param exec_ctx: The execution context with results
## @param problem_ctx: The problem context with expected state
## @return: Dictionary with {correct: bool, score: float, feedback: String}
func validate(exec_ctx: ExecutionContext, problem_ctx: BaseProblemContext) -> Dictionary:
	push_error("ValidationStrategy.validate() is abstract. Subclasses MUST implement this method.")
	return {"correct": false, "score": 0.0, "feedback": "No validation strategy configured"}


## Create a validation result dictionary.
## Utility method for subclasses.
func _make_result(correct: bool, score: float, feedback: String) -> Dictionary:
	return {
		"correct": correct,
		"score": score,
		"feedback": feedback
	}
