# XAPIBuilderService.gd
# Transforma datos crudos del juego en statements xAPI válidos
class_name XAPIBuilderService
extends Node

var _repository: XAPIStatementRepository

func _init() -> void:
	_repository = XAPIStatementRepository.new()

## Construye y guarda un statement xAPI
## Retorna el statement creado o Dictionary vacío si falla
func build(
	verb_key: String,
	object_type: String,
	object_id: String,
	object_name: String,
	actor_id: String,
	result: Dictionary = {},
	context: Dictionary = {}
) -> Dictionary:
	
	# Validar verbo
	if not Verbs.is_valid(verb_key):
		push_error("XAPIBuilder: Verbo inválido '%s'" % verb_key)
		return {}
	
	var verb_data := Verbs.get(verb_key)
	
	# Generar IDs únicos
	var statement_id := _generate_uuid()
	var timestamp := Time.get_datetime_string_from_system()
	
	# Construir statement
	var statement: Dictionary = {
		"id": statement_id,
		"verb_id": verb_data.get("id", ""),
		"verb_display": Verbs.get_display(verb_key),
		"object_type": object_type,
		"object_id": object_id,
		"object_name": object_name,
		"actor_id": actor_id,
		"result_score_raw": result.get("score_raw"),
		"result_score_scaled": result.get("score_scaled"),
		"result_success": result.get("success"),
		"result_completion": result.get("completion", true),
		"result_duration": result.get("duration", ""),
		"context_extensions": context,
		"timestamp": timestamp,
		"created_at": timestamp,
		"batch_id": ""  # Se asigna cuando se agrega a un batch
	}
	
	# Guardar en SQLite
	if not _repository.save(statement):
		push_error("XAPIBuilder: Error al guardar statement %s" % statement_id)
		return {}
	
	print("DEBUG [XAPIBuilder]: Statement creado: %s (%s)" % [statement_id, verb_key])
	return statement

## Método helper para eventos comunes

func on_level_started(level_id: String, level_name: String, actor_id: String) -> Dictionary:
	return build(
		Verbs.ATTEMPTED,
		"level",
		level_id,
		level_name,
		actor_id
	)

func on_level_completed(
	level_id: String,
	level_name: String,
	actor_id: String,
	score_raw: float,
	score_scaled: float,
	success: bool,
	duration: String
) -> Dictionary:
	var result := {
		"score_raw": score_raw,
		"score_scaled": score_scaled,
		"success": success,
		"completion": true,
		"duration": duration
	}
	return build(
		Verbs.COMPLETED,
		"level",
		level_id,
		level_name,
		actor_id,
		result
	)

func on_assessment_answered(
	assessment_id: String,
	assessment_name: String,
	actor_id: String,
	correct: bool,
	response_time: String = ""
) -> Dictionary:
	var result := {
		"success": correct,
		"completion": true,
		"duration": response_time
	}
	return build(
		Verbs.ANSWERED,
		"assessment",
		assessment_id,
		assessment_name,
		actor_id,
		result
	)

func on_game_started(game_id: String, game_name: String, actor_id: String) -> Dictionary:
	return build(
		Verbs.INITIALIZED,
		"game",
		game_id,
		game_name,
		actor_id
	)

func on_game_ended(game_id: String, game_name: String, actor_id: String) -> Dictionary:
	return build(
		Verbs.TERMINATED,
		"game",
		game_id,
		game_name,
		actor_id
	)

## Obtiene statements pendientes de sincronizar
func get_pending_statements(limit: int = 50) -> Array[Dictionary]:
	return _repository.get_unbatched(limit)

## Genera un UUID v4 simple
func _generate_uuid() -> String:
	var uuid := ""
	var hex_chars := "0123456789abcdef"
	
	for i in range(32):
		var random_index := randi() % 16
		uuid += hex_chars[random_index]
		if i == 7 or i == 11 or i == 15 or i == 19:
			uuid += "-"
	
	return uuid