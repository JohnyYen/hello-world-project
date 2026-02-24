# Clase abstracta para los controladores de niveles
class_name LevelController

var level_configuration : LevelConfiguration
var modifier : BaseLevelModifier
var context : BaseProblemContext
var segment : Segment
var block_repository : BlockRepository

signal level_completed(data : Dictionary)
signal send_blocks_code_zone(blocks : Array[Block])

func get_problem_context() -> BaseProblemContext:
	push_error("METHOD_NOT_IMPLEMENTED")
	return null

func save_progress():
	push_error("METHOD_NOT_IMPLEMENTED");


func get_avaible_blocks() -> Array[Block]:
	push_error("METHOD_NOT_IMPLEMENTED");
	return []

func finish_level(data : Dictionary):
	emit_signal('level_completed', data)

func get_level_configuration(segment_id : int) -> LevelConfiguration:
	push_error("METHOD_NOT_IMPLEMENTED");
	return null

func send_blocks_to_code_zone(blocks: Array[Block]) -> void:
	print("DEBUG: LevelController sending ", blocks.size(), " blocks via signal")
	for i in range(blocks.size()):
		var block = blocks[i]
		if block != null:
			print("DEBUG: Sending block #", i, " name: ", block.name, ", ID: ", block.block_id)
		else:
			print("DEBUG: Found a null block at index ", i)
	emit_signal("send_blocks_code_zone", blocks)
	print("DEBUG: Signal emitted successfully")
