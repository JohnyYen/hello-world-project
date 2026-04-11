extends Node
class_name DialogueController

var dialogueBox : DialogueBox
var dialogue_dir: String

var dialogue_json : Array
var index_dialogue = 0
# Called when the node enters the scene tree for the first time.
func _init(i_dialog_dir: String, dialogue_box : DialogueBox) -> void:
	self.dialogueBox = dialogue_box
	self.dialogue_dir = i_dialog_dir
	self.dialogue_json = load_json(self.dialogue_dir)
	
func load_json(path : String) -> Array:
	if not FileAccess.file_exists(path):
		push_error("El archivo JSON no existe en la ruta: " + path)
		return [{}]
	
	var file = FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Error al abrir el archivo")
		return [{}]
	
	var json_text = file.get_as_text()
	file.close() 
	
	var json_data = JSON.parse_string(json_text)
	if json_data == null:
		push_error("Error al parsear JSON")
		return [{}]
	
	return json_data
	
func next_dialogue():
	if index_dialogue < dialogue_json.size():
		dialogueBox.update_ui(dialogue_json[index_dialogue])
		index_dialogue += 1

func finish_dialogue():
	return index_dialogue == dialogue_json.size()
	
