## Collects standard performance metrics: score, errors, time.
## Compatible with the existing PerformanceAnalyzer and AdaptiveAgent.
class_name PerformanceMetricsCollector


## Collect performance metrics from the execution.
## Returns: {"score": 0.0-1.0, "errors": int, "time": float}
func collect(exec_ctx: ExecutionContext, problem_ctx: BaseProblemContext = null) -> Dictionary:
	var metrics := {}

	metrics["score"] = _calculate_score(exec_ctx)
	metrics["errors"] = _count_errors(exec_ctx)
	metrics["time"] = exec_ctx.execution_time

	return metrics
