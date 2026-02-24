extends Control

var dialogue_controller : DialogueController
@onready var dialog_box : DialogueBox = $dialogBox
var json_dir : String = "res://assets/dialogues/scene_01.arrive.json"
 
func _ready():
	dialogue_controller = DialogueController.new(json_dir, dialog_box)
	dialogue_controller.next_dialogue()
	pass 


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if dialogue_controller.finish_dialogue():
		var new_scene = preload("res://scenes/pages/welcome.tscn")  
		var instance = new_scene.instantiate()
		get_tree().root.add_child(instance)
		get_tree().current_scene.queue_free()
		get_tree().current_scene = instance


func _on_dialog_box_dialogue_update():
	dialogue_controller.next_dialogue()
