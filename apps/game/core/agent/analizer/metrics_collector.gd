## Abstract base class for performance metrics collection.
## Defines WHAT data is collected about the player's performance for the adaptive agent.
##
## Subclasses MUST implement collect().
## Examples of concrete implementations:
##   - PerformanceMetricsCollector: Score, errors, time (current game)
##   - BehavioralMetricsCollector: Patterns, hesitation, retries
##   - CustomMetricsCollector: Game-specific metrics defined by config
class_name MetricsCollector


## Collect performance metrics from the execution context.
## MUST be overridden by subclasses.
## @param exec_ctx: The execution context with results
## @param problem_ctx: Optional problem context for additional metrics
## @return: Dictionary with metric keys and values
func collect(exec_ctx: ExecutionContext, problem_ctx: BaseProblemContext = null) -> Dictionary:
	push_error("MetricsCollector.collect() is abstract. Subclasses MUST implement this method.")
	return {}


## Utility: Calculate score from execution context.
## Score is 1.0 if correct with no errors, scales down based on errors and partial progress.
func _calculate_score(exec_ctx: ExecutionContext) -> float:
	if exec_ctx.completed and not exec_ctx.has_errors():
		return 1.0

	if exec_ctx.has_errors():
		# Penalize for each error
		var error_penalty = float(exec_ctx.errors.size()) * 0.1
		return max(0.0, 1.0 - error_penalty)

	# Partial credit based on steps completed successfully
	if exec_ctx.steps.size() > 0:
		var successful = 0
		for step in exec_ctx.steps:
			if step.get("result") == true:
				successful += 1
		return float(successful) / float(exec_ctx.steps.size())

	return 0.0


## Utility: Count errors from execution context.
func _count_errors(exec_ctx: ExecutionContext) -> int:
	return exec_ctx.errors.size()
