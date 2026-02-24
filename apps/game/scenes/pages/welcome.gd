extends Control

@onready var dialogue_controller : DialogueController
@onready var dialogue_box : DialogueBox = $dialogBox
# Called when the node enters the scene tree for the first time.
func _ready():
	dialogue_controller = DialogueController.new("res://assets/dialogues/init.json", dialogue_box)
	dialogue_controller.next_dialogue()
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if dialogue_controller.finish_dialogue():
		var new_scene = preload("res://scenes/pages/arrive_faculty.tscn")  
		var instance = new_scene.instantiate()
		get_tree().root.add_child(instance)
		get_tree().current_scene.queue_free()
		get_tree().current_scene = instance

func _on_dialog_box_dialogue_update():
	dialogue_controller.next_dialogue()
