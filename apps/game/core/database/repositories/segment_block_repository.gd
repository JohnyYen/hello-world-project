class_name SegmentBlockRepository

# Conexión a la base de datos SQLite
var _db: SQLite

## Inicializa el repositorio y abre la conexión a la base de datos.
func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL
	if !_db.open_db():
		push_error("No se pudo abrir la base de datos.")
		
## Mapea un diccionario de datos de la base de datos a un objeto SegmentBlock.
## @param data: Un diccionario que representa una fila de la tabla Segment_Blocks.
## @return: Un objeto SegmentBlock con los datos mapeados.
func _map_segment_block(data: Dictionary) -> SegmentBlock:
	var segment_block = SegmentBlock.new()
	segment_block.segment_id = data.get("segment_id", -1)
	segment_block.block_id = data.get("block_id", -1)
	segment_block.is_required = bool(data.get("is_required", false))
	return segment_block

## Obtiene todos los bloques asociados a un ID de segmento específico.
## @param segment_id: El ID del segmento del que se quieren obtener los bloques.
## @return: Un Array de diccionarios, donde cada diccionario representa un bloque.
func get_blocks_by_segment(segment_id: int) -> Array:
	#var segment_blocks: Array[SegmentBlock] = []
	var results = _db.select_rows("Segment_Blocks", "segment_id = " + str(segment_id), ["*"])
	
	return results
