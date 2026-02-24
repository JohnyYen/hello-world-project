## Base class for inference engines used by the Adaptive Agent
## This class defines the interface that all inference engines must implement
## and provides a foundation for extending to different inference approaches
## such as rule-based, machine learning-based, or hybrid systems.
class_name BaseInference

## Determines the appropriate action based on the provided performance data
## This method should be overridden by subclasses to implement specific
## inference logic (e.g., rule-based, machine learning-based, etc.)
## @param performance_data: Dictionary containing normalized performance metrics with keys:
##                         - "score": the normalized performance score (0.0-1.0)
##                         - "errors": the number of errors made
##                         - "avg_score": the average performance score
##                         - "time": the time taken (if applicable)
## @return: String representing the action to take ("increase", "decrease", or "keep")
func decide_action(performance_data: Dictionary) -> String:
    print("DEBUG: BaseInference.decide_action called with data: ", performance_data)
    # Issue a warning indicating that this method should be implemented by subclasses
    push_warning("Base inference: implementar en subclase")
    # Return a default "keep" action as a fallback
    return "keep"