## AttemptData.gd
## Data Transfer Object (DTO) para pasar datos de un intento de nivel
## entre capas: XAPIService -> GameController -> LevelController -> AdaptiveAgent
## 
## Encapsula: score, errors, time con type hints explícitos
## para tener autocompletado y validación de tipos en todas las capas.

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

## Constructor con parámetros requeridos
func _init(p_score: float = 0.0, p_errors: int = 0, p_time: float = 0.0) -> void:
	score = clamp(p_score, 0.0, 1.0)
	errors = max(0, p_errors)
	time = max(0.0, p_time)
	timestamp = Time.get_datetime_string_from_system()

## Crea un AttemptData a partir de un Dictionary (conversión desde XAPIService/GameController)
static func from_dictionary(data: Dictionary) -> AttemptData:
	var attempt := AttemptData.new(
		data.get("score", 0.0),
		data.get("errors", 0),
		data.get("time", 0.0)
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
		"timestamp": timestamp
	}

## String representation para debugging
func _to_string() -> String:
	return "AttemptData(score=%.2f, errors=%d, time=%.2fs, level_id=%d, actor_id=%s)" % [
		score, errors, time, level_id, actor_id
	]
