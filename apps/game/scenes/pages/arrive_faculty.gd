extends Control

@onready var dialogue_box : DialogueBox = $dialogBox

var dialogue_controller : DialogueController

var json_dir : String = "res://assets/dialogues/scene_03_arrive_faculty.json"


func _ready():
	dialogue_controller = DialogueController.new(json_dir, dialogue_box)
	dialogue_controller.next_dialogue()



# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if dialogue_controller.finish_dialogue():
		var new_scene = preload("res://scenes/pages/arrive_classroom.tscn")  
		var instance = new_scene.instantiate()
		get_tree().root.add_child(instance)
		get_tree().current_scene.queue_free()
		get_tree().current_scene = instance


func _on_dialog_box_dialogue_update():
	dialogue_controller.next_dialogue()
