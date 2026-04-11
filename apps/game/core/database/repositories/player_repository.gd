# PlayerRepository.gd
class_name PlayerRepository

# Conexión a la base de datos SQLite
var _db: SQLite

# Inicializar la conexión a la base de datos
func _init(db_path: String) -> void:
	_db = SQLite.new()
	if _db.open(db_path) != OK:
		push_error("No se pudo abrir la base de datos.")

# Crear un nuevo jugador
func create_player(username: String, password: String):
	var query = """
		INSERT INTO players (username, password)
		VALUES ('%s', '%s', '%s');
	""" % [username, password]
	_db.query(query)

# Obtener un jugador por su ID
func get_player_by_id(player_id: String) -> Player:
	var query = """
		SELECT * FROM players WHERE user_id = '%s';
	""" % player_id
	_db.query(query)
	if _db.fetch_row():
		var user_id = _db.get_data("user_id")
		var username = _db.get_data("username")
		var password = _db.get_data("password")
		return Player.new(user_id, username, password)
	return null
