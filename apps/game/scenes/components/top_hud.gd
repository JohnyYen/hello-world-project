class_name TopHUDController
extends Node

@export var coin_label: Label
@export var attempts_label: Label


var attempts := 0
var coin := 0

func _ready() -> void:
	self.attempts = 0
	self.coin = 0
	self.attempts_label.text = "Intentos X 0"
	self.coin_label.text = "X 0"

func set_active_coin(active: bool = true):
	var parent := self.coin_label.get_parent() as HBoxContainer
	parent.visible = active

func add_attempts():
	self.attempts += 1
	self.attempts_label.text = "Intentos X %d" % self.attempts


func add_coin(coin : int):
	self.coin = coin
	self.coin_label.text = "X %d" % self.coin
