# BlockRepository.gd
class_name BlockRepository

# Conexión a la base de datos SQLite
var _db: SQLite

# Inicializar la conexión a la base de datos
func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL
	if !_db.open_db():
		push_error("No se pudo abrir la base de datos.")

# Obtener todos los bloques
func get_all_blocks() -> Array[Block]:
	var query := """
		SELECT
			b.block_id,
			b.block_type_id, 
			b.description,
			bt.name
		FROM Blocks b
		INNER JOIN Block_Types bt ON b.block_type_id = bt.block_type_id;
	"""
	var blocks : Array[Block] = []
	var raw_block = _db.select_rows("Blocks", "", ["block_id", "block_type_id", "description", "name"])
	var raw_block_types = _db.select_rows("Block_Types", "", ["block_type_id", "block_type"])
	var block_list = []
	for rb in raw_block:
		print(rb)
		for rbt in raw_block_types:
			print(rbt)
			if rb.block_type_id == rbt.block_type_id:
				var block_data = {
					"block_id": rb.block_id,
					"block_type_id": rb.block_type_id,
					"description": rb.description,
					"name": rb.name,
					"block_type": rbt.block_type
				}
				block_list.append(block_data)
				break
	print(block_list)
	# var result :=_db.query(query)

	# if result:
	# 	print("DEBUG [BlockRepository]: Query executed successfully %s." % query)
	# else:
	# 	print_debug("DEBUG [BlockRepository]: Failed to execute query %s." % query)
	# 	return blocks  # Return empty array on failure
	# while _db.fetch_row():
	# 	var b = Block.new(_db.get_data("block_id"), _db.get_data("block_type_id"), _db.get_data("description"), _db.get_data("name"), _db.get_data("block_type"))
	# 	blocks.append(b)
	# var block_list = _db.query(query)
	
	for block in block_list:
		var b = Block.new(block.block_id, block.block_type_id, block.description, block.name, block.block_type)
		blocks.append(b)
		
	return blocks

# Obtener todos los tipos de bloque
func get_all_block_types() -> Array[BlockType]:
	var block_types = []
	var query = """
		SELECT * FROM block_types;
	"""
	_db.query(query)
	while _db.fetch_row():
		var block_type = BlockType.new()
		block_type.tipo_bloque_id = _db.get_data("tipo_bloque_id")
		block_type.tipo_bloque = _db.get_data("tipo_bloque")
		block_types.append(block_type)
	return block_types

# Obtener todos los bloques de un tipo específico
func get_blocks_by_block_type(block_type_id: int) -> Array[Block]:
	var blocks: Array[Block] = []
	
	var blocks_list = _db.select_rows("Blocks", "block_type_id = " + str(block_type_id), ['*'])
	print(blocks_list)
	for block in blocks_list:
		var b = Block.new(block.block_id, block.block_type_id, block.description, block.name, "START")
		blocks.append(b)
		
	return blocks
