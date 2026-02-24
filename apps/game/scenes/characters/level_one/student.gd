extends Node2D

var normal = "res://assets/character/student/female/coffe_girl_normal.png"
var happy = "res://assets/character/student/female/coffe_girl_happy.png"
var petition = "res://assets/character/student/female/coffe_girl_petition.png"
var recive = "res://assets/character/student/female/coffe_girl.png"

@onready var character : Sprite2D = $CoffeGirlNormal

func _ready():
	EventBus.execute_block.connect(_on_execute_block)
	
func _on_execute_block(block : Block):
	if block.block_type_id == 1:
		character.texture = load(happy)
		character.texture = load(recive)
		character.texture = load(normal)
		character.texture = load(petition)
	print("dsdsdsds")
