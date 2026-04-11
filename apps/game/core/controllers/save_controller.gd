extends Node
class_name SaveController



func save_game():
	var data := _GameState.to_dict();
	var json = JSON.stringify(data, "\t")
	
	var file = FileAccess.open(Env.SAVE_FILE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(json)
		print("DEBUG [Save Controller]: Guardado realizado con exito");
	else:
		print("DEBUG [Save Controller]: Hubo un error inesperado guardando el juego")
	
func load_game():
	if not FileAccess.file_exists(Env.SAVE_FILE_PATH):
		print("DEBUG [Save Controller]: No existe archivo guardado o esta corrupto, se usara un estado inicial")
		return
	
	var file = FileAccess.open(Env.SAVE_FILE_PATH, FileAccess.READ)
	if not file:
		push_error("DEBUG [Save Controller]: No se pudo cargar la informacion del juego")
		return
	
	var content = file.get_as_text()
	var data = JSON.parse_string(content)
	
	if typeof(data) == TYPE_DICTIONARY:
		_GameState.from_dict(data)
		print("DEBUG [Save Controller]: Se cargaron correctamente los datos del juego")
	else:
		push_error("DEBUG [Save Controller]: Los datos del guardado estan corruptos")
	
