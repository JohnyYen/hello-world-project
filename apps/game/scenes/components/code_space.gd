extends Control
class_name CodeSpace
@onready var block_list: VBoxContainer = $HBoxContainer/BlockList/VBoxContainer/ScrollContainer/VBoxContainer
@onready var block_space: VBoxContainer = $HBoxContainer/BlockSpace/Control/MarginContainer/HScrollBar/VBoxContainer

var level_config : LevelConfiguration
var send_block_list : Array[BaseBlock]
# var block_scene = preload("res://scenes/components/CodeBlock.tscn")

# var execute_block_scene = preload("res://scenes/components/blocks/execute_block.tscn")

signal evaluate_signal(blocks : Array[Block])

func _ready():
	# When the code space is ready, connect to the level controller to receive allowed blocks
	# This would be connected by the parent scene (cafeteria_gameplay.gd)
	pass

func set_level_configuration(config : LevelConfiguration):
	level_config = config


# Method to receive blocks from the level controller
func receive_allowed_blocks(blocks: Array[Block]) -> void:
	print("DEBUG: CodeSpace received ", blocks.size(), " blocks")
	var code_block_factory = CodeBlockFactory.new()
	for i in range(blocks.size()):
		var block = blocks[i]
		if block != null:
			print("DEBUG: Processing block #", i, " name: ", block.name, ", ID: ", block.block_id, "Type: ", block.block_type)
			var code_block : CodeBlockComponent = code_block_factory.create_code_block(block.block_type)
			code_block.block_selected.connect(_on_block_selected)
			
			block_list.add_child(code_block)
			code_block.btn.pressed.connect(Callable(code_block, "_on_texture_button_pressed"))
			if code_block is ExecutionCodeBlock and level_config != null:
				(code_block as ExecutionCodeBlock).set_actions(level_config.defined_actions)

				
			# code_block.configure(block)
			code_block.connect("block_clicked", Callable(self, "_on_block_clicked"))
			code_block.connect("block_dropped", Callable(self, "_on_block_dropped"))
			# block_list.add_child(code_block)
		else:
			print("DEBUG: Received a null block at index ", i)
			
func _on_block_selected(block_data : Dictionary):
	print("Bloque seleccionado: ", block_data)

	var code_block_factory = CodeBlockFactory.new()
	var new_block : CodeBlockComponent = code_block_factory.create_code_block(block_data["type"])

	# Configurar datos en el nuevo bloque
	new_block.block_name = block_data["name"]
	new_block.description = block_data["description"]

	# --- DESACTIVAR TODAS LAS SEÑALES DEL BLOQUE ---
	# Esto incluye todas las señales declaradas en CodeBlockComponent
	for signal_name in new_block.get_signal_list():
		# Desconectar todas las conexiones existentes de esa señal
		var connections = new_block.get_signal_connection_list(signal_name.get("name", ""))
		for conn in connections:
			new_block.disconnect(conn.get("signal", "").get_name(), conn.get("callable", ""))
	
	# Ahora el bloque está “limpio” y no emitirá nada hasta que lo conectes tú mismo

	# Si quieres conectarlo manualmente solo a lo que necesitas:
	# new_block.block_selected.connect(_on_block_selected)
	# new_block.btn.pressed.connect(Callable(new_block, "_on_texture_button_pressed"))

	block_space.add_child(new_block)
	
	if new_block is ExecutionCodeBlock and level_config != null:
		(new_block as ExecutionCodeBlock).set_actions(level_config.defined_actions)
	new_block.btn.pressed.connect(_on_block_dropped.bind(new_block))
	



func _on_click():
	print("sadasdas")
# This method will be called when a block in the block list is clicked
 #func _on_block_clicked(block: Block):
 	## Create a copy of the clicked block and add it to the execution area
 	#var block_copy = block_scene.instantiate()
 	#block_copy.configure(block)
 	#block_space.add_child(block_copy)
	#
 	## Connect the signals of the copy to handle interactions in the execution area
 	#block_copy.connect("block_clicked", Callable(self, "_on_block_space_clicked"))
 	#block_copy.connect("block_dropped", Callable(self, "_on_block_dropped"))

# This method handles when a block is dropped (after dragging)
func _on_block_dropped(block_data: CodeBlockComponent):
	block_data.queue_free()
	# Determine whether the block was dropped in a valid area
	# For now, we'll just make sure it stays in the execution area if dropped there
	#var mouse_pos = get_global_mouse_position()
	#
	## Check if the block is in the execution area (right side)
	#var block_space_rect = block_space.get_global_rect()
	#if block_space_rect.has_point(mouse_pos):
		## Block is in the execution area, keep it there
		## Make sure it's properly parented to the block_space
		#for child in get_tree().get_nodes_in_group("dragged_block"):
			#if child.get_block().block_id == block_data.block_id and child.get_parent() != block_space:
				## Reparent to block_space if needed
				#block_space.add_child(child)
	#else:
		## Block is outside execution area, remove it
		#for child in block_space.get_children():
			#if child.get_block().block_id == block_data.block_id:
				#child.queue_free()
				#break

# This method removes a block from the execution area when clicked
func _on_block_space_clicked(block_data: Block):
	for child in block_space.get_children():
		if child.get_block().block_id == block_data.block_id:
			child.queue_free()
			break

func clear_blocks_in_zone():
	for node in block_space.get_children():
		node.queue_free()

# Method to evaluate the current solution
func evaluate_solution() -> Array[BaseBlock]:
	var result : Array[BaseBlock] = []
	print("DEBUG [Code Space]: Evaluate Solution")
	for block_node in block_space.get_children():
		print("Processing block in space: ", block_node.block_name)
		result.append(block_node.get_block())
		# EventBus.execute_block.emit(block_node.get_block())
	return result

func _on_texture_button_pressed():
	var list_block : Array[BaseBlock] = evaluate_solution()
	print("Final block list: ", list_block)
	send_block_list = list_block
	emit_signal("evaluate_signal", list_block)
