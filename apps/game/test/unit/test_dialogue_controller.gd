extends GutTest


# Mocks
class MockDialogueBox extends DialogueBox:
	var updated_data = null
	func update_ui(data):
		updated_data = data

func eliminar_archivo(ruta_archivo: String) -> void:
	var dir = DirAccess.open(".") # Abre el directorio actual
	if dir:
		var error = dir.remove_file(ruta_archivo)
		if error != OK:
			print("Error al eliminar el archivo: ", error)
	else:
		print("No se pudo abrir el directorio.")

# Setup
func setup():
	var mock_dialogue_box = MockDialogueBox.new()
	var dialogue_dir = "test_dialogue.json"
	var test_json = [{"character": "res://test_char.png", "background": "res://test_bg.png", "dialogue": "Hola", "name": "Personaje"}]
	
	var file = FileAccess.open(dialogue_dir, FileAccess.WRITE)
	file.store_string(JSON.stringify(test_json))
	file.close()
	
	return mock_dialogue_box # Return the mock
	
func teardown():
	eliminar_archivo("test_dialogue.json") # Elimina el archivo de prueba
	eliminar_archivo("invalid.json") # Elimina el archivo de prueba
	
# Test Cases
func test_init():
	var mock_dialogue_box = setup()
	var dialogue_dir = "test_dialogue.json"
	var controller = DialogueController.new(dialogue_dir, mock_dialogue_box)

	assert_eq(controller.dialogueBox, mock_dialogue_box)
	assert_eq(controller.dialogue_dir, dialogue_dir)
	assert_eq(controller.dialogue_json.size(), 1)

func test_load_json_valid_file():
	var mock_dialogue_box = setup()
	var controller = DialogueController.new("test_dialogue.json", mock_dialogue_box)
	var data = controller.load_json("test_dialogue.json")
	assert_eq(data.size(), 1)

func test_load_json_invalid_file():
	var mock_dialogue_box = setup()
	var controller = DialogueController.new("test_dialogue.json", mock_dialogue_box)
	var data = controller.load_json("non_existent.json")
	assert_eq(data.size(), 1) # Should return a default empty array

func test_load_json_invalid_json():
	var mock_dialogue_box = setup()
	var controller = DialogueController.new("test_dialogue.json", mock_dialogue_box)
	var file = FileAccess.open("invalid.json", FileAccess.WRITE)
	file.store_string("invalid json")
	file.close()

	var data = controller.load_json("invalid.json")
	assert_eq(data.size(), 1) # Should return a default empty array

func test_next_dialogue():
	var mock_dialogue_box = setup()
	var controller = DialogueController.new("test_dialogue.json", mock_dialogue_box)

	controller.next_dialogue()
	assert_not_null(mock_dialogue_box.updated_data)
	assert_eq(mock_dialogue_box.updated_data.dialogue, "Hola")

func test_finish_dialogue():
	var mock_dialogue_box = setup()
	var controller = DialogueController.new("test_dialogue.json", mock_dialogue_box)

	assert_false(controller.finish_dialogue())
	controller.next_dialogue()
	assert_true(controller.finish_dialogue())
