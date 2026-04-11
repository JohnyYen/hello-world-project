## Abstract base class for solution execution strategies.
## Defines HOW a player's solution is executed against the problem context.
##
## Subclasses MUST implement execute().
## Examples of concrete implementations:
##   - SequentialExecutor: Execute steps in order (current game)
##   - GraphExecutor: Execute based on graph/flow structure
##   - ParallelExecutor: Execute multiple steps simultaneously
##   - StepByStepExecutor: Execute with manual stepping
class_name Executor

## Emitted when execution starts
signal execution_started(solution: SolutionData)

## Emitted when execution completes
signal execution_completed(context: ExecutionContext)

## Emitted when an error occurs during execution
signal execution_error(error: String)


## Execute the player's solution against the problem context.
## MUST be overridden by subclasses.
## @param solution: The player's solution data
## @param context: The problem context to execute against
## @return: ExecutionContext with execution results
func execute(solution: SolutionData, context: BaseProblemContext) -> ExecutionContext:
	push_error("Executor.execute() is abstract. Subclasses MUST implement this method.")
	return ExecutionContext.new()


## Validates that the solution has the minimum required data.
## MAY be overridden by subclasses.
func can_execute(solution: SolutionData) -> bool:
	push_warning("Executor.can_execute() not implemented by subclass.")
	return true
