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

## Array to store full attempt data (AttemptData objects) for enriched analytics
## This allows analysis of trends beyond just scores
var attempts_history: Array[AttemptData] = []

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
	print("[PerformanceAnalyzer | normalize]: Datos recibidos - score=%s, errors=%s" % [raw.get("score", "MISSING"), raw.get("errors", "MISSING")])
	# Get and clamp the score between 0.0 and 1.0 to ensure valid range
	var score = clamp(raw.get("score", 0.0), 0.0, 1.0)
	# Get the number of errors, defaulting to 0 if not provided
	var errors = int(raw.get("errors", 0))

	print("[PerformanceAnalyzer | normalize]: Score normalizado: %.2f, Errores: %d" % [score, errors])

	# Add the current score to the historical scores array
	scores.append(score)
	# Maintain the history size limit by removing the oldest score if needed
	if scores.size() > history_size:
		scores.pop_front()

	# Calculate exponentially weighted moving average
	# This gives more weight to recent scores while considering historical values
	# Using smooth_alpha = 0.3 means 30% weight to the new score, 70% to the historical average
	avg_score = _calc_moving_average()  # Alternative: use simple moving average

	# Return the normalized performance data including the smoothed average
	var result = {
		"score": score,
		"errors": errors,
		"avg_score": avg_score,
		"time": raw.get("time", 0.0)
	}
	return result

## Calculates a simple arithmetic moving average of stored scores
## This is an alternative to the exponential smoothing used in normalize()
## @return: Float representing the average of all scores in the history
func _calc_moving_average() -> float:
	# If there are no scores in history, return the last known average
	if scores.size() == 0:
		return avg_score

	# Calculate sum of all scores in history
	var s = 0.0
	for v in scores:
		s += v

	var avg = s / scores.size()
	# Return the arithmetic mean
	return avg


## Updates the history size parameter
## @param new_size: The new size for the scores history
func set_history_size(new_size: int) -> void:
	history_size = new_size
	while scores.size() > history_size:
		scores.pop_front()

## Updates the smoothing alpha parameter
## @param new_alpha: The new alpha value for exponential smoothing (0.0 to 1.0)
func set_smooth_alpha(new_alpha: float) -> void:
	smooth_alpha = clamp(new_alpha, 0.0, 1.0)

## === Historial de intentos enriquecido ===

## Registra un intento con datos completos (score, errors, time)
## @param attempt: AttemptData objeto con score, errors, time
func record_attempt(attempt: AttemptData) -> void:
	if attempt == null:
		push_warning("PerformanceAnalyzer.record_attempt: AttemptData es null")
		return

	attempts_history.append(attempt)
	print("[PerformanceAnalyzer | record_attempt]: Intento #%d registrado - score=%.2f, errors=%d, time=%.2fs" % [
		attempts_history.size(), attempt.score, attempt.errors, attempt.time
	])

	# Mantener límite de historial
	if attempts_history.size() > history_size:
		attempts_history.pop_front()

## Obtiene el historial completo de intentos
## @return Array de AttemptData objects
func get_attempts_history() -> Array[AttemptData]:
	return attempts_history.duplicate()

## Obtiene el número total de intentos registrados
## @return Cantidad de intentos en el historial
func get_attempt_count() -> int:
	return attempts_history.size()

## Calcula la tendencia de desempeño
## Retorna un valor entre -1.0 (empeorando) y 1.0 (mejorando)
## @return float: tendencia (-1.0 a 1.0)
func calculate_trend() -> float:
	if attempts_history.size() < 2:
		return 0.0

	# Comparar últimos 2 intentos
	var recent_attempts = attempts_history.slice(-2)
	var prev_score = recent_attempts[0].score
	var curr_score = recent_attempts[1].score

	var trend = curr_score - prev_score
	print("[PerformanceAnalyzer | calculate_trend]: Tendencia calculada - prev=%.2f, curr=%.2f, trend=%.2f" % [
		prev_score, curr_score, trend
	])

	return trend

## Obtiene el promedio de errores en el historial
## @return float: promedio de errores
func get_average_errors() -> float:
	if attempts_history.size() == 0:
		return 0.0

	var total_errors := 0
	for attempt in attempts_history:
		total_errors += attempt.errors

	var avg = float(total_errors) / attempts_history.size()
	return avg

## Obtiene el promedio de tiempo en el historial
## @return float: promedio de tiempo en segundos
func get_average_time() -> float:
	if attempts_history.size() == 0:
		return 0.0

	var total_time := 0.0
	for attempt in attempts_history:
		total_time += attempt.time

	var avg = total_time / attempts_history.size()
	return avg

## Reseta completamente el historial de intentos
func reset_attempts_history() -> void:
	attempts_history.clear()
	print("[PerformanceAnalyzer | reset_attempts_history]: Historial de intentos reseteado")