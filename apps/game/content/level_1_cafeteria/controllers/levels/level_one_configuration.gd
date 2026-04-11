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
	var json_dict = _load_segment_data()

	if typeof(json_dict) != TYPE_DICTIONARY:
		push_error("Invalid JSON data for segment " + str(self.segment_id))
		return self

	json_data = json_dict

	# Lógica general definida en la clase base
	load_from_dict(json_dict)

	# Propiedades específicas del Nivel 1
	title = json_dict.get("title", "")
	description = json_dict.get("description", "")
	ui_config = json_dict.get("ui_config", {})

	return self


## Load segment data from JSON config file (preferred) with DB fallback.
func _load_segment_data() -> Dictionary:
	# Try JSON file first
	var json_config := LevelJSONConfig.new()
	var segment := json_config.load_segment("cafeteria_level", self.segment_id)

	if not segment.is_empty():
		print("DEBUG [LevelOneConfiguration]: Loaded segment from JSON file, segment_id=", self.segment_id)
		return segment

	# Fallback to database
	print("DEBUG [LevelOneConfiguration]: JSON not found, falling back to DB, segment_id=", self.segment_id)
	var level_id = 1
	var repo := LevelRepository.new()
	return repo.get_segment_json(level_id, self.segment_id)


## ===============================================
## GETTERS ESPECÍFICOS DEL NIVEL 1
## ===============================================

### Obtener la cola de estudiantes
func get_student_queue() -> Array:
	if json_data.has("initial_state") and typeof(json_data["initial_state"]) == TYPE_DICTIONARY:
		return json_data["initial_state"].get("student_queue", [])
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
func get_expected_result() -> Array:
	if json_data.has("expected_outputs") and typeof(json_data["expected_outputs"]) == TYPE_ARRAY:
		return json_data["expected_outputs"]
	return []


### Obtener cantidad de clientes en la cola
func get_customer_count() -> int:
	var queue = get_student_queue()
	return queue.size()

### Obtener la configuración del HUD / interfaz
func get_ui_config() -> Dictionary:
	return ui_config


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
