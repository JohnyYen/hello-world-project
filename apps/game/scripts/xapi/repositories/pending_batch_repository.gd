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
	var batch_id := UUID.generate()
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

## Ejecuta migraciones de schema pendientes.
## Delega en Migration002RecoverStuckBatches que maneja schema_version y meta table.
## @return: Dictionary {applied: bool, recovered_sending: int, requeued_failed: int}
func run_migrations() -> Dictionary:
	return Migration002RecoverStuckBatches.run(_db)

## Recupera batches 'sending' que quedaron trabados más tiempo del permitido.
## Los pasa a 'pending' preservando last_attempt_at y retry_count para auditoría.
## @param max_age_minutes: Edad máxima en minutos. Batches con last_attempt_at
##   más viejo que esto se consideran stall y se recuperan.
## @return: Cantidad de batches recuperados.
func recover_sending(max_age_minutes: int) -> int:
	var count_rows := _db.select_rows(
		"pending_batch",
		"status = 'sending' AND last_attempt_at IS NOT NULL AND datetime(last_attempt_at) <= datetime('now', '-%d minutes')" % max_age_minutes,
		["COUNT(*) as c"]
	)
	var count: int = int(count_rows[0].get("c", 0)) if not count_rows.is_empty() else 0

	if count == 0:
		return 0

	var query := "UPDATE pending_batch SET status = 'pending' WHERE status = 'sending' AND last_attempt_at IS NOT NULL AND datetime(last_attempt_at) <= datetime('now', '-%d minutes')" % max_age_minutes
	_db.query(query)
	return count

## Re-encola batches 'failed' que agotaron sus reintentos (retry_count >= threshold).
## Los pasa a 'pending' con retry_count=0 para que se reintenten desde cero.
## Preserva payload y last_error para auditoría post-mortem.
## @param threshold: retry_count mínimo para considerar el batch como agotado.
## @return: Cantidad de batches re-encolados.
func requeue_failed(threshold: int) -> int:
	var count_rows := _db.select_rows(
		"pending_batch",
		"status = 'failed' AND retry_count >= %d" % threshold,
		["COUNT(*) as c"]
	)
	var count: int = int(count_rows[0].get("c", 0)) if not count_rows.is_empty() else 0

	if count == 0:
		return 0

	var query := "UPDATE pending_batch SET status = 'pending', retry_count = 0 WHERE status = 'failed' AND retry_count >= %d" % threshold
	_db.query(query)
	return count

## Limpia batches terminales ('completed' y 'failed') más viejos que max_age_days.
## No toca batches 'pending' ni 'sending'.
## @param max_age_days: Edad máxima en días. Batches con last_attempt_at
##   más viejo que esto se eliminan permanentemente.
## @return: Cantidad de batches eliminados.
func cleanup_terminal(max_age_days: int) -> int:
	var count_rows := _db.select_rows(
		"pending_batch",
		"(status = 'completed' OR status = 'failed') AND last_attempt_at IS NOT NULL AND datetime(last_attempt_at) <= datetime('now', '-%d days')" % max_age_days,
		["COUNT(*) as c"]
	)
	var count: int = int(count_rows[0].get("c", 0)) if not count_rows.is_empty() else 0

	if count == 0:
		return 0

	var query := "DELETE FROM pending_batch WHERE (status = 'completed' OR status = 'failed') AND last_attempt_at IS NOT NULL AND datetime(last_attempt_at) <= datetime('now', '-%d days')" % max_age_days
	_db.query(query)
	return count

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
static func _generate_uuid() -> String:
	return UUID.generate()
