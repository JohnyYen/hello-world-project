# PendingBatchRepository.gd
class_name PendingBatchRepository

const STATUS_PENDING: String = "pending"
const STATUS_SENDING: String = "sending"
const STATUS_FAILED: String = "failed"
const STATUS_COMPLETED: String = "completed"

var _db: SQLite

func _init() -> void:
	_db = SQLite.new()
	_db.path = Env.DATABASE_URL
	if not _db.open_db():
		push_error("No se pudo abrir la base de datos para pending batches")

## Crea un nuevo batch pendiente
func create(payload: Dictionary) -> String:
	var batch_id := _generate_uuid()
	var statements_json := JSON.stringify(payload.get("statements", []))
	var payload_json := JSON.stringify(payload.get("payload", {}))
	
	var query := """
		INSERT INTO pending_batch (id, statements, payload, status, retry_count, created_at)
		VALUES (?, ?, ?, ?, 0, ?)
	"""
	
	var params := [
		batch_id,
		statements_json,
		payload_json,
		STATUS_PENDING,
		Time.get_datetime_string_from_system()
	]
	
	if not _db.query_with_bindings(query, params):
		push_error("Error al crear pending batch")
		return ""
	
	return batch_id

## Obtiene un batch por ID
func get_by_id(batch_id: String) -> Dictionary:
	var rows := _db.select_rows("pending_batch", "id = '%s'" % batch_id, ["*"])
	if rows.is_empty():
		return {}
	return rows[0]

## Obtiene batches pendientes para procesar
func get_pending(limit: int = 10) -> Array[Dictionary]:
	var query := "status = '%s'" % STATUS_PENDING
	var rows := _db.select_rows("pending_batch", query, ["*"])
	var result: Array[Dictionary] = []
	for i in range(min(limit, rows.size())):
		result.append(rows[i])
	return result

## Obtiene batches que fallaron y pueden reintentarse
func get_retryable(max_retries: int = 5) -> Array[Dictionary]:
	var query := "status = '%s' AND retry_count < %d" % [STATUS_FAILED, max_retries]
	var rows := _db.select_rows("pending_batch", query, ["*"])
	var result: Array[Dictionary] = []
	for row in rows:
		result.append(row)
	return result

## Actualiza el estado de un batch
func update_status(batch_id: String, status: String, error_message: String = "") -> bool:
	var query := """
		UPDATE pending_batch 
		SET status = ?, last_error = ?, last_attempt_at = ?
		WHERE id = ?
	"""
	
	var params := [
		status,
		error_message,
		Time.get_datetime_string_from_system(),
		batch_id
	]
	
	return _db.query_with_bindings(query, params)

## Incrementa el contador de reintentos
func increment_retry(batch_id: String) -> bool:
	var query := "UPDATE pending_batch SET retry_count = retry_count + 1, last_attempt_at = ? WHERE id = ?"
	return _db.query_with_bindings(query, [Time.get_datetime_string_from_system(), batch_id])

## Limpia batches completados (opcional, para mantenimiento)
func cleanup_completed(max_age_days: int = 7) -> int:
	var query := "DELETE FROM pending_batch WHERE status = '%s'" % STATUS_COMPLETED
	# Esta es una versión simple, en producción filtrar por fecha
	_db.query(query)
	return 0

## Obtiene el conteo de batches por estado
func get_stats() -> Dictionary:
	var stats := {
		"pending": 0,
		"sending": 0,
		"failed": 0,
		"completed": 0
	}
	
	for status in ["pending", "sending", "failed", "completed"]:
		var query := "status = '%s'" % status
		var rows := _db.select_rows("pending_batch", query, ["COUNT(*) as count"])
		if not rows.is_empty():
			stats[status] = int(rows[0].get("count", 0))
	
	return stats

## Genera un UUID v4 simple
func _generate_uuid() -> String:
	var uuid := ""
	var hex_chars := "0123456789abcdef"
	
	for i in range(32):
		var random_index := randi() % 16
		uuid += hex_chars[random_index]
		if i == 7 or i == 11 or i == 15 or i == 19:
			uuid += "-"
	
	return uuid