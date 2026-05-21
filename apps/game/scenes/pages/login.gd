extends Control

@onready var username_input := $Panel/VBoxContainer/NameContainer/Username
@onready var password_input := $Panel/VBoxContainer/PassContainer/Password

func _ready() -> void:
	pass

func _on_enter_pressed() -> void:
	var username = self.username_input.get("text")
	var password = self.password_input.get("text")
	
	


func _on_exit_pressed() -> void:
	self.visible = false
