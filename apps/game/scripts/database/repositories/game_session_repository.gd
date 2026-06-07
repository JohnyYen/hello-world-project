# GameSessionRepository.gd
# Gestiona el cache local de game_id e instance_id en SQLite.
# Sigue el mismo patrón que BlockRepository.gd y ProgressRepository.gd:
#   - Constructor sin parámetros, usa Env.DATABASE_URL
#   - Solo queries (sin schema management)
#   - El schema se crea en connect.gd::on_create_game_session_table()
#   - Usa query_with_values() con ? placeholders (prepared statements, sin SQL injection)
class_name GameSessionRepository

# Nombre de la tabla (constante para evitar magic strings)
const TABLE_NAME: String = "game_session"

# Conexión a la base de datos SQLite
var _db: SQLite

# Inicializar la conexión a la base de datos
func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL
	if !_db.open_db():
		push_error("No se pudo abrir la base de datos.")

# Obtener todas las sesiones (singleton: 0 o 1 resultado)
func get_all_sessions() -> Array:
	var rows: Array = _db.select_rows(TABLE_NAME, "", ["id", "game_id", "instance_id", "student_id", "created_at", "updated_at"])
	var result: Array = []
	for row in rows:
		var session: GameSession = _row_to_session(row)
		result.append(session)
	return result

# Obtener la sesión cacheada (la única fila, id=1) o null
func get_session() -> GameSession:
	var rows: Array = _db.select_rows(TABLE_NAME, "id = 1", ["game_id", "instance_id", "student_id", "created_at", "updated_at"])
	if rows.is_empty():
		return null
	return _row_to_session(rows[0])

# Verificar si hay una sesión válida cacheada
func has_session() -> bool:
	return get_session() != null

# Guardar o actualizar la sesión (upsert).
# Como la tabla es singleton (id=1), primero verifica si la fila existe:
#   - Si existe: UPDATE preserva created_at y solo actualiza los otros campos + updated_at
#   - Si no: INSERT con created_at=now y updated_at=now
# Usa query_with_values con ? placeholders (sin SQL injection).
# Antes usaba `_db.get_changes() == 0` para detectar si el UPDATE había afectado una fila,
# pero el plugin godot-sqlite v4.4 no expone `get_changes()`. Se reemplaza con un
# SELECT previo de la fila singleton (mismo número de queries, semántica idéntica).
func save_session(game_id: String, instance_id: String, student_id: String = "") -> void:
	var now: String = Time.get_datetime_string_from_system(true)

	# 1) Verificar si la fila singleton (id=1) ya existe
	var existing: Array = _db.select_rows(TABLE_NAME, "id = 1", ["id"])

	# 2) Si existe, UPDATE; si no, INSERT
	if existing.is_empty():
		var insert_query: String = "INSERT INTO %s (id, game_id, instance_id, student_id, created_at, updated_at) VALUES (1, ?, ?, ?, ?, ?)" % TABLE_NAME
		_db.query_with_values(insert_query, [game_id, instance_id, student_id, now, now])
	else:
		var update_query: String = "UPDATE %s SET game_id = ?, instance_id = ?, student_id = ?, updated_at = ? WHERE id = 1" % TABLE_NAME
		_db.query_with_values(update_query, [game_id, instance_id, student_id, now])

# Eliminar la sesión cacheada
func clear_session() -> void:
	var query: String = "DELETE FROM %s WHERE id = 1" % TABLE_NAME
	_db.query(query)

# Convierte una fila de la DB (Dictionary) a un GameSession
func _row_to_session(row: Dictionary) -> GameSession:
	var session: GameSession = GameSession.new()
	session.game_id = str(row.get("game_id", ""))
	session.instance_id = str(row.get("instance_id", ""))
	session.student_id = str(row.get("student_id", ""))
	session.created_at = str(row.get("created_at", ""))
	session.updated_at = str(row.get("updated_at", ""))
	return session
