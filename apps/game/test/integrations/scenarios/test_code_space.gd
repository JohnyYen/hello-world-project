# test_control_script_sin_gdscript_v2.gd
extends GutTest

# Mocks
class MockBlockRepository:
	func get_blocks_by_block_type(block_type_id: int) -> Array:
		var block1 = {"name": "Normal", "block_id": 1}
		var block2 = {"name": "Ejecutar", "block_id": 2}
		return [block1, block2]

class MockBlock:
	var block_data: Dictionary
	var clicked_event_connected = false

	func configure(block_data: Dictionary):
		self.block_data = block_data

	func get_block_data() -> Dictionary:
		return block_data

	func connect_click_event():
		clicked_event_connected = true

var emitted_events = [] # Array para registrar eventos emitidos

func emit_event(event_name, data): # Función para simular la emisión de eventos
	emitted_events.append({"name": event_name, "data": data})

func test_ready():
	var control_node = {} # Simula el nodo Control
	control_node.block_list = [] # Simula la lista de bloques
	control_node.block_space = [] # Simula el espacio de bloques
	control_node.block_repository = MockBlockRepository.new()
	control_node.block_scene = MockBlock
	control_node.execute_block_scene = MockBlock

	# Simula _ready()
	var block_list_data = control_node.block_repository.get_blocks_by_block_type(1)
	for block_data in block_list_data:
		var code_block = control_node.block_scene.new()
		code_block.configure(block_data)
		code_block.connect_click_event()
		control_node.block_list.append(code_block)

	assert_eq(control_node.block_list.size(), 2, "Dos bloques deben ser añadidos")
	assert_not_null(control_node.block_list[0], "Bloque 1 creado")
	assert_eq(control_node.block_list[1].block_data.name, "Ejecutar", "Bloque 2 es de ejecución")
	assert_true(control_node.block_list[0].clicked_event_connected, "Evento clic conectado")

func test_on_block_clicked():
	var control_node = {}
	control_node.block_space = []
	var block_data = {"block_id": 1}
	# Simula _on_block_clicked()
	var copy = MockBlock.new()
	copy.configure(block_data)
	copy.connect_click_event()
	control_node.block_space.append(copy)

	assert_eq(control_node.block_space.size(), 1, "Un bloque debe ser añadido")
	assert_true(control_node.block_space[0].clicked_event_connected, "Evento clic conectado")

func test_on_block_space_clicked():
	var control_node = {}
	control_node.block_space = []
	var block_data1 = {"block_id": 1}
	var block_data2 = {"block_id": 2}
	var code_block1 = MockBlock.new()
	code_block1.configure(block_data1)
	var code_block2 = MockBlock.new()
	code_block2.configure(block_data2)
	control_node.block_space.append(code_block1)
	control_node.block_space.append(code_block2)
	# Simula _on_block_space_clicked()
	control_node.block_space.erase(control_node.block_space[0])

	assert_eq(control_node.block_space.size(), 1, "Un bloque debe ser eliminado")

func test_evaluate_solution():
	var control_node = {}
	control_node.block_space = []
	var block_data1 = {"block_id": 1}
	var block_data2 = {"block_id": 2}
	var code_block1 = MockBlock.new()
	code_block1.configure(block_data1)
	var code_block2 = MockBlock.new()
	code_block2.configure(block_data2)
	control_node.block_space.append(code_block1)
	control_node.block_space.append(code_block2)
	# Simula _on_texture_button_pressed()
	for block in control_node.block_space:
		emit_event("execute_block", block.get_block_data())

	assert_eq(emitted_events.size(), 2, "Dos eventos deben ser emitidos")
	assert_eq(emitted_events[0].data.block_id, 1, "Bloque 1 emitido incorrectamente")
	assert_eq(emitted_events[1].data.block_id, 2, "Bloque 2 emitido incorrectamente")
