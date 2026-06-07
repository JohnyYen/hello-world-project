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
## @param error_message: Variant. Acepta String (escrita literal) o Dictionary
##                       (serializada a JSON para persistir el error estructurado).
##                       Si está vacío, persiste NULL.
func update_status(batch_id: String, status: String, error_message: Variant = "") -> bool:
	var query := """
		UPDATE pending_batch
		SET status = ?, last_error = ?, last_attempt_at = ?
		WHERE id = ?
	"""

	var stored_error: Variant = null
	if error_message is Dictionary:
		stored_error = JSON.stringify(error_message)
	elif error_message is String:
		var as_string: String = error_message
		if not as_string.is_empty():
			stored_error = as_string
	elif error_message != null:
		stored_error = str(error_message)

	var params := [
		status,
		stored_error,
		Time.get_datetime_string_from_system(),
		batch_id
	]

	return _db.query_with_bindings(query, params)

## Incrementa el contador de reintentos
func increment_retry(batch_id: String) -> bool:
	var query := "UPDATE pending_batch SET retry_count = retry_count + 1, last_attempt_at = ? WHERE id = ?"
	return _db.query_with_bindings(query, [Time.get_datetime_string_from_system(), batch_id])

## Elimina batches en estado terminal (completed o failed) más antiguos que N días.
## El filtro de edad se aplica sobre `last_attempt_at` (cae a `created_at` si nunca intentó).
## @return: número de filas eliminadas. Retorna 0 si no hay candidatas (idempotente).
func cleanup_terminal(max_age_days: int = 7) -> int:
	var where := "status IN ('%s', '%s') AND last_attempt_at < datetime('now', '-%d days')" % [STATUS_COMPLETED, STATUS_FAILED, max_age_days]
	var deleted: int = _count_where(where)
	if not _db.query("DELETE FROM pending_batch WHERE " + where):
		return 0
	print("DEBUG [PendingBatchRepository | cleanup_terminal]: Eliminados %d batches terminal más antiguos que %d días" % [deleted, max_age_days])
	return deleted

## Cuenta filas en `pending_batch` que matchean la condición dada (string SQL crudo).
## Usado como pre-count antes de UPDATE/DELETE para devolver el affected_rows count
## (el plugin godot-sqlite v4.4 no expone `get_changes()`).
## @return: número de filas que matchean.
func _count_where(condition: String) -> int:
	var rows := _db.select_rows("pending_batch", condition, ["COUNT(*) as c"])
	if rows.is_empty():
		return 0
	return int(rows[0].get("c", 0))

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

## Ejecuta las migraciones locales pendientes en orden.
## Por ahora solo corre Migration002 (recover stuck batches).
## @return: Dictionary con el resultado agregado de la última migración aplicada
##          (o un no-op si schema_version ya está al día).
func run_migrations() -> Dictionary:
	var result := Migration002RecoverStuckBatches.run(_db)
	print("DEBUG [PendingBatchRepository | run_migrations]: applied=%s, recovered_sending=%d, requeued_failed=%d" % [str(result.get("applied", false)), int(result.get("recovered_sending", 0)), int(result.get("requeued_failed", 0))])
	return result

## Recupera batches stuck en estado 'sending' (crash) y los regresa a 'pending'.
## Filtra por antigüedad de `last_attempt_at` para no tocar envíos activos.
## Preserva `last_attempt_at` y `retry_count` para auditoría.
## @param max_age_minutes: filas con last_attempt_at más viejo que N minutos son recuperadas.
## @return: número de filas actualizadas.
func recover_sending(max_age_minutes: int = 5) -> int:
	var where := "status = 'sending' AND last_attempt_at < datetime('now', '-%d minutes')" % max_age_minutes
	var recovered: int = _count_where(where)
	if not _db.query("UPDATE pending_batch SET status = 'pending' WHERE " + where):
		push_error("PendingBatchRepository.recover_sending: query falló")
		return 0
	print("DEBUG [PendingBatchRepository | recover_sending]: Recovered %d sending batches older than %d minutes" % [recovered, max_age_minutes])
	return recovered

## Re-encola batches en estado 'failed' cuyo retry_count llegó al threshold.
## Resetea `retry_count=0` y mueve a `pending`. Preserva payload, statements,
## last_attempt_at y last_error para auditoría.
## @param threshold: filas con retry_count >= threshold son re-encoladas.
## @return: número de filas actualizadas.
func requeue_failed(threshold: int = 5) -> int:
	var where := "status = 'failed' AND retry_count >= %d" % threshold
	var requeued: int = _count_where(where)
	if not _db.query("UPDATE pending_batch SET status = 'pending', retry_count = 0 WHERE " + where):
		push_error("PendingBatchRepository.requeue_failed: query falló")
		return 0
	print("DEBUG [PendingBatchRepository | requeue_failed]: Re-queued %d failed batches with retry_count >= %d" % [requeued, threshold])
	return requeued

## Genera un UUID v4 simple
static func _generate_uuid() -> String:
	return UUID.generate()
