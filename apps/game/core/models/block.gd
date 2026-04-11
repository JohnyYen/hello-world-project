# Block.gd
class_name Block


var block_id: int  # Clave primaria (PK)
var block_type_id: int  # Clave foránea (FK) a Block_types
var description: String
var name: String

# Relación con BlockType (muchos a uno)
var block_type: String  # Tipo de bloque asociado

# TODO: Eliminar esta relación incorrecta
# Relación con Segment_Blocks (uno a muchos)
var segment_blocks: Array = []  # Lista de relaciones con segmentos


func _init(id:int, b_block_type_id:int, b_description: String, b_name: String, b_block_type : String = "START") -> void:
	self.block_id = id;
	self.block_type_id = b_block_type_id;
	self.description = b_description;
	self.name = b_name
	self.block_type = b_block_type
	pass
	
