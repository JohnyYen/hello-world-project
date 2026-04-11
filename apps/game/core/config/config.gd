extends Node
class_name Config

var config;
# Función para cargar el archivo JSON
func load_config() -> Dictionary:
	var file = FileAccess.open("res://config.json", FileAccess.READ)
	if file:
		var text = file.get_as_text()
		file.close()
		var config = JSON.parse_string(text)
		if config:
			return config
		else:
			print("Error: No se pudo parsear el archivo JSON.")
	else:
		print("Error: No se encontró el archivo config.json.")
	return {}

# Función para buscar una variable en el JSON
func get_config_value(path: String):
	var keys = path.split("/")  # Divide la ruta en partes
	var current = config

	# Recorre el JSON según la ruta proporcionada
	for key in keys:
		if current.has(key):
			current = current[key]
		else:
			print("Error: No se encontró la clave '", key, "' en la ruta '", path, "'")
			return null

	return current

# Ejemplo de uso
func _ready():
	var config = load_config()