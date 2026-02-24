## Base class for performance analyzers used by the Adaptive Agent
## This class defines the interface that all performance analyzers must implement
## and provides a foundation for extending to different analysis approaches
## for processing raw performance data into normalized metrics.
## This is an abstract base class intended to be extended by specific analyzers.
extends Resource
class_name BaseAnalizer

## Normalizes raw performance data into standardized metrics
## This method should be overridden by subclasses to implement specific
## normalization logic for different types of performance analysis
## @param raw: Dictionary containing raw performance metrics
## @return: Dictionary containing normalized performance metrics
func normalize(raw: Dictionary) -> Dictionary:
    print("DEBUG: BaseAnalizer.normalize called with raw data: ", raw)
    push_error("METHOD_NOT_IMPLEMENTED")
    return {};