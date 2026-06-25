class_name LoginPage
extends Control

@export var username_input : TextEdit
@export var password_input : TextEdit
@export var email_input : TextEdit

@onready var api_client: ApiClient


func _ready() -> void:
	api_client = ApiClient.new()
	add_child(api_client)

func _on_enter_pressed() -> void:
	var username = self.username_input.get("text")
	var password = self.password_input.get("text")
	var email = email_input.get("text")
	
	var result
	if username:
		result = await self.api_client.login(username, password)
	elif password:
		result = await self.api_client.login("", email, password)
	
	
	if result.OK:
		#FeedbackBalloon.show_feedback("Hola")
		LoadingScreen.change_scene("res://scenes/pages/menu.tscn")
	else:
		var error_msg = result.get("error", "Error desconocido")
		print("ERROR DETALLE: ", error_msg)
		AlertComponent.show_alert("Credenciales incorrectas", "error", 3.0)


func _on_exit_pressed() -> void:
	self.visible = false
