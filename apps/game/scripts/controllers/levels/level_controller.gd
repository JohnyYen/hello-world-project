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
	print("[LevelController | finish_level] Emitiendo level_completed - data keys=%s" % data.keys())
	print("[LevelController | finish_level] score=%.2f, errors=%d, level_id=%d, actor_id=%s" % [
		data.get("score", 0.0), data.get("errors", 0), data.get("level_id", 0), data.get("actor_id", "?")
	])
	var signal_connections := get_signal_connection_list("level_completed")
	print("[LevelController | finish_level] Conexiones a level_completed: %d" % signal_connections.size())
	for conn in signal_connections:
		print("[LevelController | finish_level]   -> callable=%s" % str(conn["callable"]))
	emit_signal('level_completed', data)
	print("[LevelController | finish_level] Señal level_completed emitida")

func get_level_configuration(segment_id : int) -> LevelConfiguration:
	push_error("METHOD_NOT_IMPLEMENTED");
	return null

func send_blocks_to_code_zone(blocks: Array[Block]) -> void:
	for i in range(blocks.size()):
		var block = blocks[i]
		#if block != null:
			#print("DEBUG: Sending block #", i, " name: ", block.name, ", ID: ", block.block_id)
		#else:
			#print("DEBUG: Found a null block at index ", i)
	emit_signal("send_blocks_code_zone", blocks)
	#print("DEBUG: Signal emitted successfully")
