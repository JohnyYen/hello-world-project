## Resource class that analyzes and normalizes performance metrics
## Provides functionality to track scores over time and calculate moving averages
## to smooth out performance data for adaptive agent decisions
extends BaseAnalizer
class_name PerformanceAnalyzer

## Maximum number of historical entries to retain
const MAX_HISTORY := 50

## The current average score based on historical data
var avg_score := 0.7

## The maximum number of past scores to keep in history for calculations
var history_size := MAX_HISTORY

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
##             - "hints_used": integer number of hints used (optional)
##             - "efficiency_rating": float efficiency rating 0.0-100.0 (optional)
##             - "objectives_completed": integer objectives completed (optional)
##             - "blocks_count": integer blocks used (optional)
## @return: Dictionary containing normalized performance metrics with:
##          - "score": the original normalized score
##          - "errors": the original error count
##          - "avg_score": the calculated average score with smoothing
##          - "time": the original time value (if provided)
##          - "hints_used": the original hints used (if provided)
##          - "efficiency_rating": the original efficiency rating (if provided)
##          - "objectives_completed": the original objectives completed (if provided)
##          - "blocks_count": the original blocks count (if provided)
func normalize(raw: Dictionary) -> Dictionary:
	print("[PerformanceAnalyzer | normalize]: Datos recibidos - score=%s, errors=%s" % [raw.get("score", "MISSING"), raw.get("errors", "MISSING")])
	var score = clamp(raw.get("score", 0.0), 0.0, 1.0)
	var errors = int(raw.get("errors", 0))

	print("[PerformanceAnalyzer | normalize]: Score normalizado: %.2f, Errores: %d" % [score, errors])

	scores.append(score)
	if scores.size() > history_size:
		scores.pop_front()

	avg_score = _calc_moving_average()

	var result = {
		"score": score,
		"errors": errors,
		"avg_score": avg_score,
		"time": raw.get("time", 0.0),
		"hints_used": raw.get("hints_used", 0),
		"efficiency_rating": raw.get("efficiency_rating", 0.0),
		"objectives_completed": raw.get("objectives_completed", 0),
		"blocks_count": raw.get("blocks_count", 0)
	}
	return result

## Calculates a simple arithmetic moving average of stored scores
## This is an alternative to the exponential smoothing used in normalize()
## @return: Float representing the average of all scores in the history
func _calc_moving_average() -> float:
	# If there are no scores in history, return the last known average
	if scores.size() == 0:
		print("[PerformanceAnalyzer] _calc_moving_average: sin scores, retornando avg_score=%.2f" % avg_score)
		return avg_score

	# Calculate sum of all scores in history
	var s = 0.0
	for v in scores:
		s += v

	var avg = s / scores.size()
	print("[PerformanceAnalyzer] _calc_moving_average: avg=%.4f (basado en %d scores)" % [avg, scores.size()])
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

## Registra un intento con datos completos (score, errors, time, hints_used, efficiency_rating, etc.)
## @param attempt: AttemptData objeto con score, errors, time, hints_used, efficiency_rating, objectives_completed, blocks_count
func record_attempt(attempt: AttemptData) -> void:
	if attempt == null:
		push_warning("PerformanceAnalyzer.record_attempt: AttemptData es null")
		return
	
	print("[PerformanceAnalyzer] Registrando intento #%d: score=%.2f, errors=%d, time=%.2f, hints=%d" % [
		attempts_history.size() + 1, attempt.score, attempt.errors, attempt.time, attempt.hints_used
	])
	
	attempts_history.append(attempt)

	if attempts_history.size() > MAX_HISTORY:
		attempts_history.pop_front()
	
	AttemptHistoryPersistence.append_attempt(attempt)
	print("[PerformanceAnalyzer] Intento registrado - historial actual: %d intentos" % attempts_history.size())

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

## Obtiene el promedio de score de TODO el historial
## (long-term baseline para blended decisions)
## @return float: promedio de score (0.0 a 1.0)
func get_long_term_baseline() -> float:
	if attempts_history.size() == 0:
		return 0.0

	var total_score := 0.0
	for attempt in attempts_history:
		total_score += attempt.score

	return total_score / attempts_history.size()

## Obtiene el promedio de hints_used en todo el historial
## @return float: promedio de pistas usadas
func get_average_hints_used() -> float:
	if attempts_history.size() == 0:
		return 0.0

	var total_hints := 0
	for attempt in attempts_history:
		total_hints += attempt.hints_used

	return float(total_hints) / attempts_history.size()

## Obtiene el promedio de efficiency_rating en todo el historial
## @return float: promedio de eficiencia (0.0 a 100.0)
func get_average_efficiency() -> float:
	if attempts_history.size() == 0:
		return 0.0

	var total_efficiency := 0.0
	for attempt in attempts_history:
		total_efficiency += attempt.efficiency_rating

	return total_efficiency / attempts_history.size()

## Obtiene la suma total de objectives_completed en todo el historial
## @return int: total de objetivos completados
func get_total_objectives() -> int:
	var total := 0
	for attempt in attempts_history:
		total += attempt.objectives_completed
	return total

## Reseta completamente el historial de intentos
func reset_attempts_history() -> void:
	attempts_history.clear()
	AttemptHistoryPersistence.clear_history()
	print("[PerformanceAnalyzer | reset_attempts_history]: Historial de intentos reseteado")

## Carga el historial desde el archivo JSON persistente
## @return true si se cargó exitosamente
func load_history_from_persistence() -> bool:
	var loaded_history := AttemptHistoryPersistence.load_history()
	if loaded_history.size() > 0:
		if loaded_history.size() > history_size:
			loaded_history = loaded_history.slice(-history_size)
		attempts_history = loaded_history
		print("[PerformanceAnalyzer] Historial cargado: %d intentos" % attempts_history.size())
		return true
	return false
