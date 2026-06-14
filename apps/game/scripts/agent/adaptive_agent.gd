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
const SHORT_TERM_WEIGHT := 0.6

## Peso para el promedio de largo plazo en el blend
const LONG_TERM_WEIGHT := 0.4

## Deltas proporcionales para cada acción
const DELTA_DECREASE_MAJOR := -0.2
const DELTA_DECREASE_MINOR := -0.1
const DELTA_KEEP := 0.0
const DELTA_INCREASE_MINOR := 0.1
const DELTA_INCREASE_MAJOR := 0.2

## Emitted when the agent decides on an action to adjust difficulty
## @param action: String representing the action taken ("decrease_major", "decrease_minor", "keep", "increase_minor", or "increase_major")
## @param new_difficulty: Float representing the new difficulty level after the action
signal action_decided(action: String, new_difficulty: float)

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

## Calcula un score blend entre corto y largo plazo.
## El corto plazo usa los últimos SHORT_TERM_WINDOW intentos de la sesión actual.
## El largo plazo carga el historial completo desde persistencia.
## @param attempts_history: Array[AttemptData] historial de la sesión actual
## @return Dictionary con {blended_score, short_term_avg, long_term_avg, long_term_count}
func _blend_short_and_long_term(attempts_history: Array[AttemptData]) -> Dictionary:
	var window_size := mini(attempts_history.size(), SHORT_TERM_WINDOW)
	var short_term_sum := 0.0
	for i in range(attempts_history.size() - window_size, attempts_history.size()):
		short_term_sum += attempts_history[i].score
	var short_term_avg := short_term_sum / window_size if window_size > 0 else 0.0

	var long_term_history := AttemptHistoryPersistence.load_history()
	var long_term_sum := 0.0
	for a in long_term_history:
		long_term_sum += a.score
	var long_term_avg := long_term_sum / long_term_history.size() if long_term_history.size() > 0 else 0.0

	var blended_score: float
	if long_term_history.size() > 0:
		blended_score = short_term_avg * SHORT_TERM_WEIGHT + long_term_avg * LONG_TERM_WEIGHT
	else:
		blended_score = short_term_avg

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
	var attempt := AttemptData.from_dictionary(raw_data)
	analyzer.record_attempt(attempt)

	var blended_data := _blend_short_and_long_term(analyzer.get_attempts_history())
	var in_session_count := analyzer.get_attempt_count()
	var long_term_count := blended_data["long_term_count"] as int
	var total_count := in_session_count + long_term_count

	if total_count < MIN_HISTORY_FOR_DECISION:
		print("[AdaptiveAgent] Insuficientes intentos (%d/%d) - sin adaptación" % 
			[total_count, MIN_HISTORY_FOR_DECISION])
		return

	var processed_data = analyzer.normalize(raw_data)
	var attempts_history = analyzer.get_attempts_history()
	var trend = trend_calculator.calculate(attempts_history, TrendCalculator.TrendMode.WEIGHTED)

	processed_data["trend"] = trend
	processed_data["blended_score"] = blended_data["blended_score"]
	processed_data["score"] = blended_data["blended_score"]

	var action = inference_engine.decide_action(processed_data)
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

	emit_signal("action_decided", action, difficulty)
	print("[AdaptiveAgent] Acción %s aplicada - Dificultad %.2f → %.2f" % [action, old_difficulty, difficulty])
