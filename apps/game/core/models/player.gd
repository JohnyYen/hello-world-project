# Player.gd
class_name Player


var user_id: String  # Clave primaria (PK)
var username: String
var password: String

# Relación con Progress (uno a muchos)
var progress: Array = []  # Lista de progresos del jugador

func _init(p_player_id: String, p_username: String, p_password: String) -> void:
	self.user_id = p_player_id
	self.username = p_username
	self.password = p_password
