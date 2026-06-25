## The AdaptiveAgent class monitors student performance and adjusts
## difficulty levels in the educational game accordingly.
## It uses a performance analyzer to process raw data and an inference
## engine to decide on appropriate actions for difficulty modification.
class_name AdaptiveAgent

## Número mínimo de intentos requeridos antes de comenzar a adaptar la dificultad
const MIN_HISTORY_FOR_DECISION := 5

## Ventana de intentos recientes para el cálculo de corto plazo
const SHORT_TERM_WINDOW := 5

## Peso para el promedio de corto plazo en el blend
const SHORT_TERM_WEIGHT := 0.8

## Peso para el promedio de largo plazo en el blend
const LONG_TERM_WEIGHT := 0.2

## Deltas proporcionales para cada acción
const DELTA_DECREASE_MAJOR := -0.2
const DELTA_DECREASE_MINOR := -0.1
const DELTA_KEEP := 0.0
const DELTA_INCREASE_MINOR := 0.1
const DELTA_INCREASE_MAJOR := 0.2

## The inference engine used to determine what action to take based on performance data
var inference_engine: BaseInference

## The performance analyzer that normalizes raw performance data
var analyzer: PerformanceAnalyzer

## The trend calculator for analyzing performance trends
var trend_calculator: TrendCalculator

## Current difficulty level, ranging from min_difficulty to max_difficulty
var difficulty := 1.0

## Minimum allowed difficulty level
var min_difficulty := 0.5

## Maximum allowed difficulty level  
var max_difficulty := 2.0

## Initializes the adaptive agent with required components
func _init() -> void:
	inference_engine = RuleBasedInference.new()
	analyzer = PerformanceAnalyzer.new()
	trend_calculator = TrendCalculator.new()
	
	# Cargar historial persistido de sesiones anteriores
	var history_loaded := analyzer.load_history_from_persistence()
	if history_loaded:
		print("[AdaptiveAgent] Historial cargado: %d intentos previos" % analyzer.get_attempt_count())
	else:
		print("[AdaptiveAgent] Sin historial previo - comenzando desde cero")

## Calcula un score blend entre corto y largo plazo.
## El corto plazo usa los últimos SHORT_TERM_WINDOW intentos de la sesión actual.
## El largo plazo carga el historial completo desde persistencia.
## @param attempts_history: Array[AttemptData] historial de la sesión actual
## @return Dictionary con {blended_score, short_term_avg, long_term_avg, long_term_count}
func _blend_short_and_long_term(attempts_history: Array[AttemptData]) -> Dictionary:
	var window_size := mini(attempts_history.size(), SHORT_TERM_WINDOW)
	print("[ADAPT_TRACE] blend: window_size=%d (de %d intentos disponibles)" % [window_size, attempts_history.size()])
	var short_term_sum := 0.0
	for i in range(attempts_history.size() - window_size, attempts_history.size()):
		print("[ADAPT_TRACE] blend: short_term incluye intento[%d] score=%.2f" % [i, attempts_history[i].score])
		short_term_sum += attempts_history[i].score
	var short_term_avg := short_term_sum / window_size if window_size > 0 else 0.0
	print("[ADAPT_TRACE] blend: short_term_avg=%.4f (sum=%.2f / count=%d)" % [short_term_avg, short_term_sum, window_size])

	var long_term_history := AttemptHistoryPersistence.load_history()
	var long_term_sum := 0.0
	for a in long_term_history:
		long_term_sum += a.score
	var long_term_avg := long_term_sum / long_term_history.size() if long_term_history.size() > 0 else 0.0
	print("[ADAPT_TRACE] blend: long_term_avg=%.4f (basado en %d intentos persistidos)" % [long_term_avg, long_term_history.size()])

	var blended_score: float
	if long_term_history.size() > 0:
		blended_score = short_term_avg * SHORT_TERM_WEIGHT + long_term_avg * LONG_TERM_WEIGHT
		print("[ADAPT_TRACE] blend: blended=%.2f*%.1f + %.2f*%.1f = %.4f" % [
			short_term_avg, SHORT_TERM_WEIGHT, long_term_avg, LONG_TERM_WEIGHT, blended_score
		])
	else:
		blended_score = short_term_avg
		print("[ADAPT_TRACE] blend: sin long_term, usando solo short_term=%.4f" % blended_score)

	return {
		"blended_score": blended_score,
		"short_term_avg": short_term_avg,
		"long_term_avg": long_term_avg,
		"long_term_count": long_term_history.size()
	}

## Analyzes raw performance data and decides on an action to adjust difficulty
## Incorpora blended score de corto y largo plazo para decisión más robusta.
## @param raw_data: Dictionary containing raw performance metrics with keys:
##                  - "score": float between 0.0 and 1.0 representing performance
##                  - "errors": integer number of errors made
##                  - "time": float representing time taken (optional)
func analyze_and_decide(raw_data : Dictionary) -> void:
	print("[ADAPT_TRACE] === analyze_and_decide INICIO ===")
	var attempt := AttemptData.from_dictionary(raw_data)
	analyzer.record_attempt(attempt)
	print("[ADAPT_TRACE] Intento registrado - score=%.2f, errors=%d" % [attempt.score, attempt.errors])

	var blended_data := _blend_short_and_long_term(analyzer.get_attempts_history())
	var total_count := analyzer.get_attempt_count()
	print("[ADAPT_TRACE] Conteo: total=%d (mínimo requerido=%d), blended_score=%.4f" % [
		total_count, MIN_HISTORY_FOR_DECISION, blended_data.get("blended_score", 0.0)
	])

	if total_count < MIN_HISTORY_FOR_DECISION:
		print("[ADAPT_TRACE] Insuficientes intentos (%d/%d) - SIN ADAPTACIÓN" % 
			[total_count, MIN_HISTORY_FOR_DECISION])
		return

	print("[ADAPT_TRACE] Umbral superado - calculando decisión...")
	var processed_data = analyzer.normalize(raw_data)
	var attempts_history = analyzer.get_attempts_history()
	var trend = trend_calculator.calculate(attempts_history, TrendCalculator.TrendMode.WEIGHTED)
	print("[ADAPT_TRACE] Trend calculado: %.4f" % trend)

	processed_data["trend"] = trend
	processed_data["blended_score"] = blended_data["blended_score"]
	processed_data["score"] = blended_data["blended_score"]

	var action = inference_engine.decide_action(processed_data)
	print("[ADAPT_TRACE] Acción decidida por inference_engine: '%s'" % action)
	_apply_action(action)

## Applies the specified action to adjust the difficulty level
## Soporta 5 acciones graduadas con deltas proporcionales.
## @param action: String representing the action to take ("decrease_major", "decrease_minor", "keep", "increase_minor", "increase_major")
func _apply_action(action: String) -> void:
	var old_difficulty = difficulty
	var delta_value := 0.0

	match action:
		"decrease_major":
			delta_value = DELTA_DECREASE_MAJOR
		"decrease_minor":
			delta_value = DELTA_DECREASE_MINOR
		"increase_minor":
			delta_value = DELTA_INCREASE_MINOR
		"increase_major":
			delta_value = DELTA_INCREASE_MAJOR
		"keep":
			delta_value = DELTA_KEEP
		_:
			push_warning("Unknown action: %s" % action)

	difficulty = clamp(difficulty + delta_value, min_difficulty, max_difficulty)

	print("[ADAPT_TRACE] Emitiendo action_decided en EventBus('%s', %.2f)" % [
		action, difficulty
	])
	EventBus.action_decided.emit(action, difficulty)
	print("[ADAPT_TRACE] Signal action_decided emitida en EventBus")
	print("[AdaptiveAgent] Acción %s aplicada - Dificultad %.2f → %.2f" % [action, old_difficulty, difficulty])
