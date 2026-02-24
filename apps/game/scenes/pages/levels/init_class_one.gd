extends Control

var previous_scene_path : String
var dialog_dir : String = "res://assets/dialogues/introduction_class_one.json"
@onready var dialog_box : DialogueBox = $dialogBox
var dialog_manager : DialogueController

# Called when the node enters the scene tree for the first time.
func _ready():
	dialog_manager = DialogueController.new(dialog_dir, dialog_box)
	dialog_manager.next_dialogue()
	pass

func _process(delta):
	if dialog_manager.finish_dialogue():
		get_tree().change_scene_to_file(previous_scene_path)
	pass


func _on_dialog_box_dialogue_update():
	dialog_manager.next_dialogue()
