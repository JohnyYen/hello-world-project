## TrendCalculator.gd
## Calcula la tendencia de desempeño a partir del historial de intentos.
## Soporta dos modos: simple (últimos 2 intentos) y weighted (últimos N intentos con pesos).
## Diseñado para ser independiente y reutilizable en otros contextos.

class_name TrendCalculator

## Modos de cálculo de tendencia disponibles
enum TrendMode {
	SIMPLE,    # Compara último vs anterior intento
	WEIGHTED   # Pondera últimos N intentos con pesos exponenciales
}

## Número máximo de intentos a considerar en modo weighted
var max_history_length: int = 5

## Pesos para el modo weighted (exponencial decreciente)
## Índice 0 = más reciente, con mayor peso
var weighted_mode_weights: Array[float] = [0.5, 0.3, 0.15, 0.04, 0.01]

## Calcula la tendencia usando el modo especificado
## @param attempts_history: Array[AttemptData] con el historial de intentos
## @param mode: TrendMode.SIMPLE o TrendMode.WEIGHTED
## @return float: Tendencia entre -1.0 (empeorando) y 1.0 (mejorando)
func calculate(attempts_history: Array[AttemptData], mode: int = TrendMode.SIMPLE) -> float:
	if attempts_history.size() < 2:
		return 0.0
	
	match mode:
		TrendMode.SIMPLE:
			return _calculate_simple_trend(attempts_history)
		TrendMode.WEIGHTED:
			return _calculate_weighted_trend(attempts_history)
		_:
			push_warning("TrendCalculator: Modo inválido %d, usando SIMPLE" % mode)
			return _calculate_simple_trend(attempts_history)

## Calcula tendencia simple: compara último vs penúltimo intento
## @param attempts_history: Array[AttemptData]
## @return float: score_actual - score_anterior
func _calculate_simple_trend(attempts_history: Array[AttemptData]) -> float:
	if attempts_history.size() < 2:
		return 0.0
	
	var recent = attempts_history.slice(-2)
	var prev_score = recent[0].score
	var curr_score = recent[1].score
	
	var trend = curr_score - prev_score
	return trend

## Calcula tendencia ponderada: considera últimos N intentos con pesos exponenciales
## Los intentos más recientes tienen mayor peso
## @param attempts_history: Array[AttemptData]
## @return float: Tendencia ponderada normalizada
func _calculate_weighted_trend(attempts_history: Array[AttemptData]) -> float:
	if attempts_history.size() < 2:
		return 0.0
	
	# Tomar los últimos N intentos (máximo max_history_length)
	var history_to_use = attempts_history.slice(
		maxi(0, attempts_history.size() - max_history_length)
	)
	
	# Calcular promedio ponderado de scores
	var weighted_sum = 0.0
	var weight_sum = 0.0
	
	# Iterar en orden inverso (más reciente primero)
	for i in range(history_to_use.size() - 1, -1, -1):
		var weight_index = history_to_use.size() - 1 - i
		if weight_index < weighted_mode_weights.size():
			var weight = weighted_mode_weights[weight_index]
			weighted_sum += history_to_use[i].score * weight
			weight_sum += weight
	
	if weight_sum == 0.0:
		return 0.0
	
	var weighted_avg = weighted_sum / weight_sum
	
	# Calcular tendencia como diferencia entre promedio reciente y más antiguo
	# Si hay solo 2 intentos, es como SIMPLE
	if history_to_use.size() == 2:
		return history_to_use[1].score - history_to_use[0].score
	
	# Para más intentos: comparar promedio de los 2 más recientes vs los 2 más antiguos
	var recent_avg = (history_to_use[history_to_use.size() - 1].score + 
					history_to_use[history_to_use.size() - 2].score) / 2.0
	var old_avg = (history_to_use[0].score + history_to_use[1].score) / 2.0
	
	var trend = recent_avg - old_avg
	return trend

## Calcula una métrica híbrida combinando score y tendencia
## @param current_score: Score del intento actual (0.0 a 1.0)
## @param trend: Tendencia calculada (-1.0 a 1.0)
## @param score_weight: Peso para el score (0.0 a 1.0)
## @param trend_weight: Peso para la tendencia (0.0 a 1.0)
## @return float: Métrica híbrida normalizada
func calculate_hybrid_metric(current_score: float, trend: float, 
							score_weight: float = 0.7, trend_weight: float = 0.3) -> float:
	# Normalizar scores a rango 0.0-1.0
	var normalized_score = clamp(current_score, 0.0, 1.0)
	var normalized_trend = clamp((trend + 1.0) / 2.0, 0.0, 1.0)  # Mapear [-1,1] a [0,1]
	
	# Calcular métrica híbrida
	var hybrid = (normalized_score * score_weight) + (normalized_trend * trend_weight)
	
	return hybrid

## Obtiene descripción textual de la tendencia
## @param trend: Valor de tendencia
## @return String: Descripción ("Mejorando", "Estable", "Empeorando")
func get_trend_description(trend: float) -> String:
	if trend > 0.1:
		return "Mejorando"
	elif trend < -0.1:
		return "Empeorando"
	else:
		return "Estable"

## Configura los pesos para modo weighted
## @param weights: Array[float] con pesos en orden (más reciente primero)
func set_weighted_mode_weights(weights: Array[float]) -> void:
	if weights.size() > 0:
		weighted_mode_weights = weights
	else:
		push_warning("TrendCalculator: Array de pesos vacío, no se actualiza")

## Configura el máximo de intentos a considerar en modo weighted
## @param length: Cantidad máxima de intentos
func set_max_history_length(length: int) -> void:
	if length > 0:
		max_history_length = length
	else:
		push_warning("TrendCalculator: max_history_length debe ser > 0")
