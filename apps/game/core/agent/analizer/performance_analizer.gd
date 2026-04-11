## Resource class that analyzes and normalizes performance metrics
## Provides functionality to track scores over time and calculate moving averages
## to smooth out performance data for adaptive agent decisions
extends BaseAnalizer
class_name PerformanceAnalyzer

## The current average score based on historical data
var avg_score := 0.7

## The maximum number of past scores to keep in history for calculations
var history_size := 5

## Array to store historical scores for calculating moving averages
var scores := []

## Alpha value for exponential smoothing (0.0 to 1.0)
## Lower values mean more smoothing, higher values mean more responsiveness
var smooth_alpha := 0.3

## Normalizes raw performance data and updates historical tracking
## @param raw: Dictionary containing raw performance metrics with keys:
##             - "score": float between 0.0 and 1.0 representing the raw score
##             - "errors": integer number of errors encountered
##             - "time": float representing the time taken (optional)
## @return: Dictionary containing normalized performance metrics with:
##          - "score": the original normalized score
##          - "errors": the original error count
##          - "avg_score": the calculated average score with smoothing
##          - "time": the original time value (if provided)
func normalize(raw: Dictionary) -> Dictionary:
    print("DEBUG: PerformanceAnalyzer.normalize called with raw data: ", raw)
    # Get and clamp the score between 0.0 and 1.0 to ensure valid range
    var score = clamp(raw.get("score", 0.0), 0.0, 1.0)
    # Get the number of errors, defaulting to 0 if not provided
    var errors = int(raw.get("errors", 0))
    
    print("DEBUG: Normalized raw score: ", score, ", errors: ", errors)
    
    # Add the current score to the historical scores array
    scores.append(score)
    # Maintain the history size limit by removing the oldest score if needed
    if scores.size() > history_size:
        var removed_score = scores.pop_front()
        print("DEBUG: Removed oldest score from history: ", removed_score)
        
    print("DEBUG: Scores history after update: ", scores)
    
    # Calculate exponentially weighted moving average
    # This gives more weight to recent scores while considering historical values
    # Using smooth_alpha = 0.3 means 30% weight to the new score, 70% to the historical average
    var old_avg_score = avg_score

    # avg_score = (smooth_alpha * score) + ((1 - smooth_alpha) * avg_score)

    avg_score = _calc_moving_average()  # Alternative: use simple moving average

    print("DEBUG: Updated average score from ", old_avg_score, " to ", avg_score, 
          " (new score: ", score, ", alpha: ", smooth_alpha, ")")
    
    # Return the normalized performance data including the smoothed average
    var result = {
        "score": score,
        "errors": errors,
        "avg_score": avg_score,
        "time": raw.get("time", 0.0)
    }
    print("DEBUG: Normalized result: ", result)
    return result

## Calculates a simple arithmetic moving average of stored scores
## This is an alternative to the exponential smoothing used in normalize()
## @return: Float representing the average of all scores in the history
func _calc_moving_average() -> float:
    print("DEBUG: PerformanceAnalyzer._calc_moving_average called with scores: ", scores)
    # If there are no scores in history, return the last known average
    if scores.size() == 0:
        print("DEBUG: No scores in history, returning avg_score: ", avg_score)
        return avg_score
    
    # Calculate sum of all scores in history
    var s = 0.0
    for v in scores:
        s += v
    
    var avg = s / scores.size()
    print("DEBUG: Calculated moving average: ", avg)
    # Return the arithmetic mean
    return avg


## Updates the history size parameter
## @param new_size: The new size for the scores history
func set_history_size(new_size: int) -> void:
    history_size = new_size
    # Trim the scores array if it's larger than the new history size
    while scores.size() > history_size:
        scores.pop_front()

## Updates the smoothing alpha parameter
## @param new_alpha: The new alpha value for exponential smoothing (0.0 to 1.0)
func set_smooth_alpha(new_alpha: float) -> void:
    smooth_alpha = clamp(new_alpha, 0.0, 1.0)

