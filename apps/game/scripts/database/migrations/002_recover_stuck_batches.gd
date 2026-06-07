# 002_recover_stuck_batches.gd
# Migration que recupera los 30 batches stuck en `pending_batch`:
#   - 9 batches con `status='sending'` (crash) → `status='pending'`
#   - 21 batches con `status='failed' AND retry_count >= 5` (exhausted)
#     → `status='pending', retry_count=0`
# Crea la tabla `meta` si no existe y bumpea `schema_version` 1→2.
# Es idempotente: si `meta.schema_version >= '2'`, retorna applied=false
# sin tocar filas. Corre dentro de una sola transacción SQLite.
class_name Migration002RecoverStuckBatches

const TARGET_VERSION: String = "2"
const SCHEMA_VERSION_KEY: String = "schema_version"
const INITIAL_VERSION: String = "1"
const META_TABLE: String = "meta"

## Ejecuta la migración contra la DB provista.
## @param db: instancia abierta de SQLite.
## @return: Dictionary {applied: bool, recovered_sending: int, requeued_failed: int}
static func run(db: SQLite) -> Dictionary:
	if db == null:
		push_error("Migration002.run: db es null")
		return {"applied": false, "recovered_sending": 0, "requeued_failed": 0}

	_ensure_meta_table(db)

	var current_version: String = _get_schema_version(db)
	if _version_gte(current_version, TARGET_VERSION):
		print("DEBUG [Migration002]: schema_version=%s >= %s, no-op" % [current_version, TARGET_VERSION])
		return {"applied": false, "recovered_sending": 0, "requeued_failed": 0}

	if current_version.is_empty():
		_seed_initial_schema_version(db)

	return _apply_recovery(db)

## Crea la tabla `meta(key TEXT PRIMARY KEY, value TEXT)` si no existe.
static func _ensure_meta_table(db: SQLite) -> void:
	var schema := {
		"key": {"data_type": "text", "primary_key": true},
		"value": {"data_type": "text"}
	}
	db.create_table(META_TABLE, schema)

## Lee la versión actual del schema. Devuelve "" si la fila no existe.
static func _get_schema_version(db: SQLite) -> String:
	var rows := db.select_rows(META_TABLE, "key = '%s'" % SCHEMA_VERSION_KEY, ["value"])
	if rows.is_empty():
		return ""
	return str(rows[0].get("value", ""))

## Inserta ('schema_version', '1') si no existe (DB pre-meta).
static func _seed_initial_schema_version(db: SQLite) -> void:
	var sql := "INSERT OR IGNORE INTO %s (key, value) VALUES (?, ?)" % META_TABLE
	db.query_with_bindings(sql, [SCHEMA_VERSION_KEY, INITIAL_VERSION])

## Compara versiones como strings (válido para "1" < "2" < "10").
static func _version_gte(current: String, target: String) -> bool:
	if current.is_empty():
		return false
	return current >= target

## Aplica los UPDATEs y el bump de versión dentro de una transacción.
## El conteo de filas afectadas se hace con un pre-count vía SELECT COUNT(*)
## (el plugin godot-sqlite v4.4 no expone `get_changes()`).
## Dentro de la transacción, el pre-count es consistente con la UPDATE siguiente
## (snapshot estable, sin writers concurrentes en SQLite local).
static func _apply_recovery(db: SQLite) -> Dictionary:
	db.query("BEGIN")

	# Pre-counts dentro de la transacción
	var recovered_sending: int = _count_sending(db)
	var requeued_failed: int = _count_failed_stale(db)

	# 1) sending → pending (preserva last_attempt_at y retry_count)
	var q_recover := "UPDATE pending_batch SET status = 'pending' WHERE status = 'sending'"
	if not db.query(q_recover):
		db.query("ROLLBACK")
		push_error("Migration002: fallo UPDATE sending->pending")
		return {"applied": false, "recovered_sending": 0, "requeued_failed": 0}

	# 2) failed (retry>=5) → pending, retry_count=0
	#    Preserva payload, statements, last_attempt_at, last_error
	var q_requeue := "UPDATE pending_batch SET status = 'pending', retry_count = 0 WHERE status = 'failed' AND retry_count >= 5"
	if not db.query(q_requeue):
		db.query("ROLLBACK")
		push_error("Migration002: fallo UPDATE failed->pending")
		return {"applied": false, "recovered_sending": recovered_sending, "requeued_failed": 0}

	# 3) Bump schema_version a '2'
	var q_bump := "INSERT OR REPLACE INTO %s (key, value) VALUES (?, ?)" % META_TABLE
	if not db.query_with_values(q_bump, [SCHEMA_VERSION_KEY, TARGET_VERSION]):
		db.query("ROLLBACK")
		push_error("Migration002: fallo bump schema_version")
		return {"applied": false, "recovered_sending": recovered_sending, "requeued_failed": requeued_failed}

	db.query("COMMIT")

	print("DEBUG [Migration002]: aplicada v1->v2 - recovered_sending=%d, requeued_failed=%d" % [recovered_sending, requeued_failed])
	return {
		"applied": true,
		"recovered_sending": recovered_sending,
		"requeued_failed": requeued_failed
	}

## Cuenta batches en estado 'sending'. Usado como pre-count dentro de _apply_recovery.
static func _count_sending(db: SQLite) -> int:
	var rows := db.select_rows("pending_batch", "status = 'sending'", ["COUNT(*) as c"])
	if rows.is_empty():
		return 0
	return int(rows[0].get("c", 0))

## Cuenta batches en estado 'failed' con retry_count >= 5. Usado como pre-count.
static func _count_failed_stale(db: SQLite) -> int:
	var rows := db.select_rows("pending_batch", "status = 'failed' AND retry_count >= 5", ["COUNT(*) as c"])
	if rows.is_empty():
		return 0
	return int(rows[0].get("c", 0))
