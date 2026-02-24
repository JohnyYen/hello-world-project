extends Control
class_name DialogueBox

signal dialogue_update
@onready var character : TextureRect = $Character
@onready var background : TextureRect = $Fondo
@onready var dialogue_box = $DialogBox/RichTextLabel
@onready var name_character = $PanelContainer/Control/Name 

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	
func update_ui(dialogue_json):
	print(dialogue_json)
	character.texture = load(dialogue_json.character)
	background.texture = load(dialogue_json.background)
	dialogue_box.text = dialogue_json.dialogue
	name_character.text = dialogue_json.name


func _on_texture_button_pressed():
	emit_signal("dialogue_update")
	pass # Replace with function body.
