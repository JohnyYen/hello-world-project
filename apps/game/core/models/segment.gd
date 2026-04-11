# Segment

class_name Segment

var segment_id: int  # Clave primaria (PK)
var level_id: int  # Clave foránea (FK) a Level
var problem: String
var goal: String
var order: int
var difficulty: String  # ENUM se representa como String en Godot
var configuration : String
# Relación con Level (muchos a uno)
var level: Level = null

# Relación con Segment_Blocks (uno a muchos)
var blocks: Array = []  # Lista de bloques asociados al segmento


func _init(
	p_segment_id: int,
	p_level_id: int,
	p_problem: String,
	p_goal: String,
	p_order: int,
	p_difficulty: String,
	p_configuration: String,
	p_level: Level = null,
	p_blocks: Array = []
):
	segment_id = p_segment_id
	level_id = p_level_id
	problem = p_problem
	goal = p_goal
	order = p_order
	difficulty = p_difficulty
	configuration = p_configuration
	level = p_level
	blocks = p_blocks
