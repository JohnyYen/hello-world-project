# LevelRepository.gd
class_name LevelRepository

# Conexión a la base de datos SQLite
var _db: SQLite
# Inicializar la conexión a la base de datos
func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL;
	if !_db.open_db():
		push_error("No se pudo abrir la base de datos.")

func mapper_level(db_level: Dictionary) -> Level:
	print(db_level);
	return Level.new(db_level.level_id, db_level.real_problem, db_level.title, db_level.goal);

func update_configuration_segment(level_id: int, segment_id: int, configuration: Dictionary) -> bool:
	print("DEBUG [Level One Modifier]: Datos recibidiso level_id %s, segment_id %s, configuration %s" % [level_id, segment_id, configuration])
	var raw_data = JSON.stringify(configuration)

	var query = """
		UPDATE Segments 
		SET configuration = ? 
		WHERE level_id = ? AND segment_id = ?
	"""

	var result = _db.query_with_bindings(query, [raw_data, level_id, segment_id])

	return result

func get_segment_json(level: int, segment_id: int) -> Dictionary:
	print("DEBUG [Level Repository]: Level_ID: %s and Segment_ID: %s" % [level, segment_id])
	var rows = _db.select_rows("Segments", "segment_id = %d AND level_id = %d" % [segment_id, level], ["configuration"])
	# Verificar que la query devuelve datos
	if rows.is_empty():
		push_error("No se encontró el segmento %d del nivel %d" % [segment_id, level])
		return {}
	
	var row = rows[0]
	
	# Obtener el JSON como string
	var config_string = row.get("configuration", "")
	
	if config_string == "":
		push_error("El segmento %d del nivel %d tiene configuracion vacía" % [segment_id, level])
		return {}
	
	# Parsear string a JSON
	var parsed = JSON.parse_string(config_string)
	
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("Configuración inválida en el segmento %d del nivel %d" % [segment_id, level])
		return {}
	
	return parsed


# Obtener todos los niveles
func get_all_levels() -> Array[Level]:
	var levels: Array[Level] = []
	var levels_result = _db.select_rows("Levels", "", ["*"]);
	
	print(levels_result);
	
	for level in levels_result:
		var l = mapper_level(level);
		levels.append(l)
		
	return levels

# Obtener un nivel por su ID
func get_level_by_id(level_id: int) -> Level:
	var level = _db.select_rows("Levels", "level_id = " + str(level_id), ['*']).map(mapper_level)[0];
	return level
