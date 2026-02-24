# Level.gd
class_name Level

var level_id: int       # Clave primaria (PK)
var real_problem: String
var title: String
var goal: String
var segments: Array     # Lista de segmentos asociados al nivel

# Constructor
func _init(
	p_level_id: int,
	p_real_problem: String,
	p_title: String,
	p_goal: String,
	p_segments: Array = []
) -> void:
	level_id = p_level_id
	real_problem = p_real_problem
	title = p_title
	goal = p_goal
	segments = p_segments
