# XAPIStatementRepository.gd
class_name XAPIStatementRepository

var _db: SQLite

func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL
	if not _db.open_db():
		push_error("No se pudo abrir la base de datos para xAPI statements")

## Guarda un statement xAPI en la base de datos
func save(statement: Dictionary) -> bool:
	var query := """
		INSERT INTO xapi_statement (
			id, verb_id, verb_display, object_type, object_id, object_name,
			actor_id, result_score_raw, result_score_scaled, result_success,
			result_completion, result_duration, context_extensions, timestamp,
			created_at, batch_id
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	"""
	
	var params := [
		statement.get("id", ""),
		statement.get("verb_id", ""),
		statement.get("verb_display", ""),
		statement.get("object_type", ""),
		statement.get("object_id", ""),
		statement.get("object_name", ""),
		statement.get("actor_id", ""),
		statement.get("result_score_raw"),
		statement.get("result_score_scaled"),
		_to_int(statement.get("result_success")),
		_to_int(statement.get("result_completion")),
		statement.get("result_duration", ""),
		JSON.stringify(statement.get("context_extensions", {})),
		statement.get("timestamp", ""),
		statement.get("created_at", ""),
		statement.get("batch_id", "")
	]
	
	var result := _db.query_with_bindings(query, params)
	if not result:
		push_error("Error al guardar xAPI statement: %s" % statement.get("id", "unknown"))
	return result

## Obtiene un statement por su ID
func get_by_id(statement_id: String) -> Dictionary:
	var rows := _db.select_rows("xapi_statement", "id = '%s'" % statement_id, ["*"])
	if rows.is_empty():
		return {}
	return rows[0]

## Obtiene todos los statements sin batch (pendientes de sincronizar)
func get_unbatched(limit: int = 50) -> Array[Dictionary]:
	var rows := _db.select_rows("xapi_statement", "batch_id IS NULL OR batch_id = ''", ["*"])
	var result: Array[Dictionary] = []
	for i in range(min(limit, rows.size())):
		result.append(rows[i])
	return result

## Actualiza el batch_id de un statement
func assign_to_batch(statement_ids: Array[String], batch_id: String) -> bool:
	for stmt_id in statement_ids:
		var query := "UPDATE xapi_statement SET batch_id = ? WHERE id = ?"
		if not _db.query_with_bindings(query, [batch_id, stmt_id]):
			push_error("Error al asignar batch %s al statement %s" % [batch_id, stmt_id])
			return false
	return true

## Obtiene statements por actor
func get_by_actor(actor_id: String, limit: int = 100) -> Array[Dictionary]:
	var query := "actor_id = '%s'" % actor_id
	var rows := _db.select_rows("xapi_statement", query, ["*"])
	var result: Array[Dictionary] = []
	for i in range(min(limit, rows.size())):
		result.append(rows[i])
	return result

## Obtiene statements por tipo de objeto
func get_by_object_type(object_type: String, limit: int = 100) -> Array[Dictionary]:
	var query := "object_type = '%s'" % object_type
	var rows := _db.select_rows("xapi_statement", query, ["*"])
	var result: Array[Dictionary] = []
	for i in range(min(limit, rows.size())):
		result.append(rows[i])
	return result

## Cuenta statements pendientes de sincronizar
func count_unbatched() -> int:
	var rows := _db.select_rows("xapi_statement", "batch_id IS NULL OR batch_id = ''", ["COUNT(*) as count"])
	if rows.is_empty():
		return 0
	return int(rows[0].get("count", 0))

## Elimina un statement por ID
func delete(statement_id: String) -> bool:
	var query := "DELETE FROM xapi_statement WHERE id = ?"
	return _db.query_with_bindings(query, [statement_id])

## Convierte un valor a entero para SQLite (0/1 para booleanos)
func _to_int(value) -> int:
	if value == null:
		return 0
	if typeof(value) == TYPE_BOOL:
		return 1 if value else 0
	if typeof(value) == TYPE_INT:
		return value
	return 0