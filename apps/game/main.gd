extends Node

func _ready():
	_load_game()
	_load_database()
	_load_main_menu()

func _load_game():
	_SaveController.load_game()

func _load_database():
	var connect_db: Connect = Connect.new();

func _load_main_menu():
	var main_menu = load("res://scenes/pages/menu.tscn")
	add_child(main_menu.instantiate())
