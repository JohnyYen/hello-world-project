## AttemptHistoryPersistence.gd
## Componente de persistencia del historial de intentos usando JSON.
## Guarda en res://data/attempt_history.json con metadata + array de AttemptData.
## Si el JSON está corrupto, reinicia desde cero.

class_name AttemptHistoryPersistence

## Versión del esquema JSON para migraciones futuras
const SCHEMA_VERSION := "1"

## Path del archivo de historial (centralizado en env.gd)
const HISTORY_FILE_PATH := Env.ATTEMPT_HISTORY_PATH

## Metadata key en el JSON
const METADATA_KEY := "metadata"
const ATTEMPTS_KEY := "attempts"

## Carga el historial completo desde el archivo JSON.
## Si el archivo no existe o está corrupto, retorna array vacío.
## @return Array[AttemptData] con el historial cargado
static func load_history() -> Array[AttemptData]:
	var attempts: Array[AttemptData] = []
	
	if not FileAccess.file_exists(HISTORY_FILE_PATH):
		print("[AttemptHistoryPersistence] No existe archivo de historial, retornando vacío")
		return attempts
	
	var file := FileAccess.open(HISTORY_FILE_PATH, FileAccess.READ)
	if file == null:
		push_warning("AttemptHistoryPersistence: No se pudo abrir el archivo para lectura")
		return attempts
	
	var json_text := file.get_as_text()
	file.close()
	
	if json_text.is_empty():
		print("[AttemptHistoryPersistence] Archivo vacío, retornando array vacío")
		return attempts
	
	var json := JSON.new()
	var parse_result := json.parse(json_text)
	
	if parse_result != OK:
		push_warning("AttemptHistoryPersistence: JSON corrupto, reiniciando desde cero")
		_clear_corrupted_file()
		return attempts
	
	var data = json.data
	if not data is Dictionary:
		push_warning("AttemptHistoryPersistence: Estructura inválida, reiniciando")
		_clear_corrupted_file()
		return attempts
	
	if not data.has(ATTEMPTS_KEY):
		return attempts
	
	var attempts_array = data[ATTEMPTS_KEY]
	if not attempts_array is Array:
		return attempts
	
	for attempt_dict in attempts_array:
		if attempt_dict is Dictionary:
			var attempt := AttemptData.from_dictionary(attempt_dict)
			attempts.append(attempt)
	
	print("[AttemptHistoryPersistence] Cargados %d intentos del historial" % attempts.size())
	return attempts

## Guarda el historial completo en el archivo JSON.
## @param attempts: Array[AttemptData] a guardar
## @return true si se guardó exitosamente, false si hubo error
static func save_history(attempts: Array[AttemptData]) -> bool:
	var attempts_dict_array: Array = []
	for attempt in attempts:
		attempts_dict_array.append(attempt.to_dictionary())
	
	var metadata := {
		"version": SCHEMA_VERSION,
		"last_update": Time.get_datetime_string_from_system(true),
		"total_attempts": attempts_dict_array.size(),
		"schema_version": SCHEMA_VERSION
	}
	
	var data := {
		"metadata": metadata,
		"attempts": attempts_dict_array
	}
	
	var json_text := JSON.stringify(data, "  ")
	return _write_to_file(json_text)

## Agrega un nuevo intento al historial sin recargar todo.
## Más eficiente que save_history para agregar un solo intento.
## @param attempt: AttemptData a agregar
## @return true si se guardó exitosamente
static func append_attempt(attempt: AttemptData) -> bool:
	var current_history := load_history()
	current_history.append(attempt)
	return save_history(current_history)

## Resetea completamente el historial.
## @return true si se reseteó exitosamente
static func clear_history() -> bool:
	var empty_data := {
		"metadata": {
			"version": SCHEMA_VERSION,
			"last_update": Time.get_datetime_string_from_system(true),
			"total_attempts": 0,
			"schema_version": SCHEMA_VERSION
		},
		"attempts": []
	}
	var json_text := JSON.stringify(empty_data, "  ")
	return _write_to_file(json_text)

## Obtiene el path completo del archivo de historial.
## @return String con el path
static func get_file_path() -> String:
	return HISTORY_FILE_PATH

## Verifica si existe el archivo de historial.
## @return true si existe
static func has_history_file() -> bool:
	return FileAccess.file_exists(HISTORY_FILE_PATH)

## Obtiene metadata del historial sin cargar todos los intentos.
## @return Dictionary con metadata, o Dictionary vacío si no existe
static func get_metadata() -> Dictionary:
	if not FileAccess.file_exists(HISTORY_FILE_PATH):
		return {}
	
	var file := FileAccess.open(HISTORY_FILE_PATH, FileAccess.READ)
	if file == null:
		return {}
	
	var json_text := file.get_as_text()
	file.close()
	
	var json := JSON.new()
	if json.parse(json_text) != OK:
		return {}
	
	var data = json.data
	if not data is Dictionary or not data.has(METADATA_KEY):
		return {}
	
	return data[METADATA_KEY]

## Escribe el texto JSON al archivo, creando directorios necesarios.
## @param json_text: Texto JSON a escribir
## @return true si se escribió exitosamente
static func _write_to_file(json_text: String) -> bool:
	# Asegurar que el directorio existe
	var dir_path := HISTORY_FILE_PATH.get_base_dir()
	if not DirAccess.dir_exists_absolute(dir_path):
		var make_dir_result := DirAccess.make_dir_recursive_absolute(dir_path)
		if make_dir_result != OK:
			push_error("AttemptHistoryPersistence: No se pudo crear directorio %s" % dir_path)
			return false
	
	var file := FileAccess.open(HISTORY_FILE_PATH, FileAccess.WRITE)
	if file == null:
		push_error("AttemptHistoryPersistence: No se pudo abrir el archivo para escritura")
		return false
	
	file.store_string(json_text)
	file.close()
	
	return true

## Limpia el archivo corrupto (lo sobrescribe con estructura vacía).
static func _clear_corrupted_file() -> void:
	clear_history()
