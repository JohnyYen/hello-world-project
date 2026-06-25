class_name LevelOneConfiguration
extends LevelConfiguration

## ===============================================
## PROPIEDADES ESPECÍFICAS DEL NIVEL 1
## ===============================================
var title: String = ""
var description: String = ""

# Guarda el JSON original para que otros métodos puedan accederlo


## ===============================================
## CARGA DE DATOS DESDE LA BD
## ===============================================
func load_data() -> LevelOneConfiguration:
	var level_id = 1

	var repo := LevelRepository.new()
	var seed_dict = repo.get_segment_json(level_id, self.segment_id)

	if typeof(seed_dict) != TYPE_DICTIONARY:
		push_error("Invalid JSON data for segment " + str(self.segment_id))
		return self

	# Store clean seed for the modifier
	seed_data = seed_dict.duplicate(true)
	print("[ADAPT_TRACE] load_data semilla: %d keys, title=%s" % [seed_dict.size(), seed_dict.get("title", "?")])

	# Read adaptation_state (diff) and merge with seed
	var adaptation_state := repo.get_adaptation_state(level_id, self.segment_id)
	if adaptation_state.is_empty():
		print("[ADAPT_TRACE] load_data adaptation_state VACÍO - sin datos de adaptación previa")
	else:
		print("[ADAPT_TRACE] load_data adaptation_state: %d keys - %s" % [
			adaptation_state.size(), str(adaptation_state.keys())
		])
	var merged_dict := _merge_config(seed_dict, adaptation_state)
	print("[ADAPT_TRACE] load_data merged_dict: %d keys" % merged_dict.size())

	json_data = merged_dict

	# Lógica general definida en la clase base
	load_from_dict(merged_dict)

	# Propiedades específicas del Nivel 1
	title = merged_dict.get("title", "")
	description = merged_dict.get("description", "")
	ui_config = merged_dict.get("ui_config", {})

	return self


static func _merge_config(seed: Dictionary, diff: Dictionary) -> Dictionary:
	var merged = seed.duplicate(true)
	for key in diff:
		var val = diff[key]
		if typeof(val) in [TYPE_DICTIONARY, TYPE_ARRAY]:
			merged[key] = val.duplicate(true)
		else:
			merged[key] = val
	return merged


## ===============================================
## GETTERS ESPECÍFICOS DEL NIVEL 1
## ===============================================

### Obtener la cola de estudiantes
func get_student_queue() -> Array:
	if json_data.has("initial_state") and typeof(json_data["initial_state"]) == TYPE_DICTIONARY:
		print(json_data["initial_state"].student_queue)
		return json_data["initial_state"].student_queue
	return []


### Obtener los bloques permitidos al jugador
func get_allowed_blocks() -> Array:
	#print(json_data)
	if json_data.has("available_blocks") and typeof(json_data["available_blocks"]) == TYPE_ARRAY:
		return json_data["available_blocks"]
	return []


### Obtener el texto o diálogo que se muestra al jugador
func get_display_text() -> String:
	return str(json_data.get("display_text", ""))


### Obtener el resultado esperado para resolver el segmento
func get_expected_result() -> Dictionary:
	if json_data.has("expected_outputs") and typeof(json_data["expected_outputs"]) == TYPE_DICTIONARY:
		return json_data["expected_outputs"]
	return {}


### Obtener cantidad de clientes en la cola
func get_customer_count() -> int:
	var queue = get_student_queue()
	return queue.size()

### Obtener la configuración del HUD / interfaz
func get_ui_config() -> Dictionary:
	return ui_config

func get_environment():
	print(json_data)
	if json_data.has("environment_data") and typeof(json_data["environment_data"]) == TYPE_DICTIONARY:
		return json_data.get("environment_data", {})
	return {}

## ===============================================
## MÉTODO AUXILIAR PARA NAVEGAR VALORES ANIDADOS
## ===============================================
func get_value(path: Array, default_value = null):
	# Ejemplo:
	# get_value(["expected_result", "message"], "OK")
	var current = json_data
	
	for key in path:
		if typeof(current) != TYPE_DICTIONARY or not current.has(key):
			return default_value
		current = current[key]

	return current
