class_name SegmentRepository

# Conexión a la base de datos SQLite
var _db: SQLite

# Inicializar la conexión a la base de datos
func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL;
	if !_db.open_db():
		push_error("No se pudo abrir la base de datos.")
		

func mapper_segment(json_data: Dictionary) -> Segment:
	return Segment.new(
	json_data["segment_id"],        
	json_data["level_id"],         
	json_data["problem"],          
	json_data["goal"],             
	json_data["position"], 
	json_data["difficulty"],
	json_data["configuration"],
	null,                          
	[]                             
);
		
func get_segment_by_id(segment_id: int) -> Segment:
	var segment = _db.select_rows("Segments", 'segment_id = ' + str(segment_id), ["*"]).map(mapper_segment)[0]
	return segment
	
func get_all_segments() -> Array[Segment]:
	return _db.select_rows("Segments", '', ['*']).map(mapper_segment);
	
func get_all_segments_by_level(level_id: int) -> Array:
	var result: Array[Segment] = []
	var rows = _db.select_rows("Segments", 'level_id = ' + str(level_id), ["*"])
	#for row in rows:
	#	result.append(mapper_segment(row))
	return rows
