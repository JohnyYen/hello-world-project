# RawStatsRepository.gd
# Repositorio para estadisticas crudas del juego con soporte offline-first
# Los stats se persisten localmente y se sincronizan con el backend cuando hay conexion

class_name RawStatsRepository

const STATUS_PENDING_SYNC: String = "pending_sync"
const STATUS_SENDING: String = "sending"
const STATUS_COMPLETED: String = "completed"
const STATUS_FAILED: String = "failed"

var _db: SQLite

func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL
	if not _db.open_db():
		push_error("No se pudo abrir la base de datos para raw stats")

## Crea la tabla raw_stats si no existe (idempotente)
func create_table() -> bool:
	var schema := {
		"id": {"data_type": "text", "primary_key": true, "not_null": true},
		"segment_id": {"data_type": "INTEGER", "not_null": true},
		"actor_id": {"data_type": "text", "not_null": true},
		"attempt_count": {"data_type": "INTEGER", "default": "0"},
		"error_count": {"data_type": "INTEGER", "default": "0"},
		"hints_used_count": {"data_type": "INTEGER", "default": "0"},
		"errors_details": {"data_type": "text"},
		"efficiency_rating": {"data_type": "REAL", "default": "0"},
		"objectives_completed": {"data_type": "INTEGER", "default": "0"},
		"status": {"data_type": "text", "default": "pending_sync", "not_null": true},
		"retry_count": {"data_type": "INTEGER", "default": "0"},
		"error_message": {"data_type": "text"},
		"created_at": {"data_type": "text", "not_null": true},
		"updated_at": {"data_type": "text", "not_null": true},
		"batch_id": {"data_type": "text"}
	}
	
	return _db.create_table("raw_stats", schema)

## Guarda un registro de raw stats
func save(stats: Dictionary) -> String:
	var stats_id = stats.get("id", UUID.generate())
	
	var query := """
		INSERT INTO raw_stats (
			id, segment_id, actor_id, attempt_count, error_count, hints_used_count,
			errors_details, efficiency_rating, objectives_completed, status,
			retry_count, error_message, created_at, updated_at, batch_id
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	"""
	
	var params := [
		stats_id,
		stats.get("segment_id", 0),
		stats.get("actor_id", ""),
		stats.get("attempt_count", 0),
		stats.get("error_count", 0),
		stats.get("hints_used_count", 0),
		JSON.stringify(stats.get("errors_details", {})),
		stats.get("efficiency_rating", 0.0),
		stats.get("objectives_completed", 0),
		STATUS_PENDING_SYNC,
		0,
		"",
		Time.get_datetime_string_from_system(),
		Time.get_datetime_string_from_system(),
		stats.get("batch_id", "")
	]
	
	if not _db.query_with_bindings(query, params):
		push_error("Error al guardar raw stats: %s" % stats_id)
		return ""
	
	return stats_id

## Obtiene un registro por ID
func get_by_id(stats_id: String) -> Dictionary:
	var rows: Array = _db.select_rows("raw_stats", "id = '%s'" % stats_id, ["*"])
	if rows.is_empty():
		return {}
	return rows[0]

## Obtiene todos los registros pendientes de sincronizar (limit = 50)
func get_pending_all(limit: int = 50) -> Array[Dictionary]:
	var rows: Array = _db.select_rows("raw_stats", "status = '%s'" % STATUS_PENDING_SYNC, ["*"])
	var result: Array[Dictionary] = []
	
	# Order by created_at for sync ordering
	var ordered_rows: Array = rows.duplicate()
	ordered_rows.sort_custom(_sort_by_created_at)
	
	# Apply limit
	for i in range(min(limit, ordered_rows.size())):
		result.append(ordered_rows[i])
	
	return result

## Sorting helper for pending records
func _sort_by_created_at(a: Dictionary, b: Dictionary) -> bool:
	return a.get("created_at", "") < b.get("created_at", "")

## Actualiza el estado de un registro
func update_status(stats_id: String, status: String, error_message: String = "") -> bool:
	var query := """
		UPDATE raw_stats
		SET status = ?, error_message = ?, updated_at = ?
		WHERE id = ?
	"""
	
	return _db.query_with_bindings(
		query,
		[status, error_message, Time.get_datetime_string_from_system(), stats_id]
	)

## Marca un registro como completado
func mark_completed(stats_id: String) -> bool:
	return update_status(stats_id, STATUS_COMPLETED)

## Marca un registro como fallido con retry
func mark_failed(stats_id: String, max_retries: int = 5) -> bool:
	var record: Dictionary = get_by_id(stats_id)
	if record.is_empty():
		return false
	
	var retry_count: int = record.get("retry_count", 0) + 1
	
	if retry_count >= max_retries:
		return update_status(stats_id, STATUS_FAILED, "Max retries exceeded")
	else:
		# Increment retry count but keep pending
		var query := "UPDATE raw_stats SET retry_count = ?, updated_at = ? WHERE id = ?"
		return _db.query_with_bindings(
			query,
			[retry_count, Time.get_datetime_string_from_system(), stats_id]
		)

## Asigna batch_id a un registro
func assign_batch(stats_id: String, batch_id: String) -> bool:
	var query := "UPDATE raw_stats SET batch_id = ?, status = 'sending' WHERE id = ?"
	return _db.query_with_bindings(query, [batch_id, stats_id])

## Asigna batch_id a multiples registros
func assign_batch_to_all(stats_ids: Array[String], batch_id: String) -> bool:
	for sid in stats_ids:
		if not assign_batch(sid, batch_id):
			return false
	return true

## Obtiene estadisticas de la tabla
func get_stats() -> Dictionary:
	return {
		"pending_sync": _count_by_status(STATUS_PENDING_SYNC),
		"sending": _count_by_status(STATUS_SENDING),
		"completed": _count_by_status(STATUS_COMPLETED),
		"failed": _count_by_status(STATUS_FAILED)
	}

func _count_by_status(status: String) -> int:
	var rows: Array = _db.select_rows("raw_stats", "status = '%s'" % status, ["COUNT(*) as count"])
	if rows.is_empty():
		return 0
	return int(rows[0].get("count", 0))
