## AttemptData.gd
## Data Transfer Object (DTO) para pasar datos de un intento de nivel
## entre capas: XAPIService -> GameController -> LevelController -> AdaptiveAgent
## 
## Encapsula: score, errors, time, hints_used, efficiency_rating,
## objectives_completed, blocks_count, error_details, custom_events
## con type hints explícitos y validación.

class_name AttemptData

## Score normalizado del intento (0.0 a 1.0)
var score: float

## Número de errores cometidos en el intento
var errors: int

## Tiempo de ejecución en segundos
var time: float

## ID del nivel/segmento (para contexto)
var level_id: int = 0

## ID del actor/jugador (para contexto)
var actor_id: String = ""

## Timestamp del intento (ISO format)
var timestamp: String = ""

## Cantidad de ayudas/pistas usadas
var hints_used: int = 0

## Rating de eficiencia (0.0 a 100.0)
var efficiency_rating: float = 0.0

## Objetivos completados en el intento
var objectives_completed: int = 0

## Cantidad de bloques usados
var blocks_count: int = 0

## Diccionario con detalles de errores por intento
var error_details: Dictionary = {}

## Eventos personalizados del juego
var custom_events: Array[Dictionary] = []

## Constructor con todos los parámetros
func _init(
	p_score: float = 0.0,
	p_errors: int = 0,
	p_time: float = 0.0,
	p_hints_used: int = 0,
	p_efficiency_rating: float = 0.0,
	p_objectives_completed: int = 0,
	p_blocks_count: int = 0,
	p_error_details: Dictionary = {},
	p_custom_events: Array[Dictionary] = []
) -> void:
	score = clamp(p_score, 0.0, 1.0)
	errors = max(0, p_errors)
	time = max(0.0, p_time)
	hints_used = max(0, p_hints_used)
	efficiency_rating = clamp(p_efficiency_rating, 0.0, 100.0)
	objectives_completed = max(0, p_objectives_completed)
	blocks_count = max(0, p_blocks_count)
	error_details = p_error_details
	custom_events = p_custom_events
	timestamp = Time.get_datetime_string_from_system()
	print("[AttemptData] Creado: score=%.2f, errors=%d, time=%.2f, hints=%d, efficiency=%.1f, objectives=%d, blocks=%d" % [
		score, errors, time, hints_used, efficiency_rating, objectives_completed, blocks_count
	])

## Crea un AttemptData a partir de un Dictionary (conversión desde XAPIService/GameController)
static func from_dictionary(data: Dictionary) -> AttemptData:
	print("[AttemptData] Creando desde dictionary: %s" % data)
	# Convertir untyped Array a Array[Dictionary] (GDScript 2.0 requiere typing explícito)
	var raw_events: Array = data.get("custom_events", [])
	var typed_events: Array[Dictionary] = []
	for event in raw_events:
		if event is Dictionary:
			typed_events.append(event)
	
	var attempt := AttemptData.new(
		data.get("score", 0.0),
		data.get("errors", 0),
		data.get("time", 0.0),
		data.get("hints_used", 0),
		data.get("efficiency_rating", 0.0),
		data.get("objectives_completed", 0),
		data.get("blocks_count", 0),
		data.get("error_details", {}),
		typed_events
	)
	attempt.level_id = data.get("level_id", 0)
	attempt.actor_id = data.get("actor_id", "")
	attempt.timestamp = data.get("timestamp", Time.get_datetime_string_from_system())
	return attempt

## Convierte el AttemptData a Dictionary (para serialización si es necesario)
func to_dictionary() -> Dictionary:
	return {
		"score": score,
		"errors": errors,
		"time": time,
		"level_id": level_id,
		"actor_id": actor_id,
		"timestamp": timestamp,
		"hints_used": hints_used,
		"efficiency_rating": efficiency_rating,
		"objectives_completed": objectives_completed,
		"blocks_count": blocks_count,
		"error_details": error_details,
		"custom_events": custom_events
	}

## String representation para debugging
func _to_string() -> String:
	return "AttemptData(score=%.2f, errors=%d, time=%.2fs, hints_used=%d, efficiency=%.2f, objectives=%d, blocks=%d, level_id=%d, actor_id=%s)" % [
		score, errors, time, hints_used, efficiency_rating, objectives_completed, blocks_count, level_id, actor_id
	]
