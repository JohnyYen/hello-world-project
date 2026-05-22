class_name LoginPage
extends Control

@onready var username_input := $Panel/VBoxContainer/NameContainer/Username
@onready var password_input := $Panel/VBoxContainer/PassContainer/Password
@onready var email_input := $Panel/VBoxContainer/EmailContainer/Email

@onready var api_client: ApiClient


func _ready() -> void:
	api_client = ApiClient.new()
	add_child(api_client)

func _on_enter_pressed() -> void:
	var username = self.username_input.get("text")
	var password = self.password_input.get("text")
	var email = email_input.get("text")
		
	var result = await self.api_client.login(username, email, password)
	
	
	if result.OK:
		LoadingScreen.change_scene("res://scenes/pages/menu.tscn")
	else:
		var error_msg = result.get("error", "Error desconocido")
		print("ERROR DETALLE: ", error_msg)
		AlertComponent.show_alert("Credenciales incorrectas", "error", 3.0)


func _on_exit_pressed() -> void:
	self.visible = false
