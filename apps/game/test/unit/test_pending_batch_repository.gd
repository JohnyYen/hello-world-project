# test_pending_batch_repository.gd
# Tests for PendingBatchRepository and Migration002RecoverStuckBatches.
# Covers:
#   - recover_sending()     (REQ-P1-R1, S-P1-R1.1, NFR-IDEM-2)
#   - requeue_failed()      (REQ-P1-R2, S-P1-R2.1, NFR-IDEM-2)
#   - cleanup_terminal()    (REQ-P1-R3, NFR-IDEM-5)
#   - run_migrations()      (REQ-P1-R7, S-P1-R7.1, S-P1-R7.2, NFR-IDEM-1)
#   ** run_migrations idempotence is the 1st of 2 NEW TESTS required by the change **
#
# Uses an in-memory SQLite DB (via :memory:) for full isolation between tests.
# Schema is bootstrapped in before_each() by running the 001_create_xapi_tables migration.
extends GutTest
## @gut_test sqlite


# ============================================================================
# Test subclass: forces :memory: SQLite so tests do not touch the real DB.
# PendingBatchRepository._init() hardcodes Env.DATABASE_URL, so we override
# _init() to redirect to an in-memory DB. Production code is NOT modified.
# ============================================================================
class TestablePendingBatchRepository extends PendingBatchRepository:
    func _init() -> void:
        _db = SQLite.new()
        _db.path = ":memory:"
        if not _db.open_db():
            push_error("Test: no se pudo abrir la DB :memory:")


# ============================================================================
# State (re-initialized in before_each for full isolation)
# ============================================================================
var _repo: TestablePendingBatchRepository


# ============================================================================
# Setup / teardown
# ============================================================================
func before_each() -> void:
    _repo = TestablePendingBatchRepository.new()
    # Bootstrap schema: create pending_batch + xapi_statement + indexes
    # (the meta table is created lazily by Migration002 on first run_migrations).
    var migration_001 := CreateXAPITablesMigration.new()
    migration_001.run(_repo._db)


func after_each() -> void:
    # In-memory DB is GC'd with the repo; nothing to clean up.
    _repo = null


# ============================================================================
# Helpers
# ============================================================================

# Inserts a pending_batch row with the given attributes.
# @param last_attempt_expr: raw SQLite expression for last_attempt_at.
#   Use "NULL" to insert SQL NULL, or e.g. "datetime('now', '-10 minutes')"
#   to insert a relative timestamp. Default is "NULL" (no last attempt).
# @return: the generated batch_id
func _insert_batch(
    status: String,
    retry_count: int = 0,
    last_attempt_expr: String = "NULL",
    payload: Dictionary = {}
) -> String:
    var batch_id: String = "batch-%s" % UUID.generate()
    var payload_json: String = JSON.stringify(payload)
    var q: String = "INSERT INTO pending_batch (id, statements, payload, status, retry_count, created_at, last_attempt_at) VALUES (?, ?, ?, ?, ?, datetime('now'), %s)" % last_attempt_expr
    _repo._db.query_with_values(q, [batch_id, "[]", payload_json, status, retry_count])
    return batch_id


# Counts rows in pending_batch with the given status.
func _count_status(status: String) -> int:
    var rows: Array = _repo._db.select_rows("pending_batch", "status = '%s'" % status, ["COUNT(*) as c"])
    if rows.is_empty():
        return 0
    return int(rows[0].get("c", 0))


# Reads the schema_version from the meta table (returns "" if not set).
func _read_schema_version() -> String:
    var rows: Array = _repo._db.select_rows("meta", "key = 'schema_version'", ["value"])
    if rows.is_empty():
        return ""
    return str(rows[0].get("value", ""))


# ============================================================================
# run_migrations() tests (S-P1-R7.1, S-P1-R7.2, NFR-IDEM-1)
# *** 1st of 2 NEW TESTS required by the change ***
# ============================================================================

func test_run_migrations_first_run_applies_and_bumps_version():
    # Arrange: 3 sending + 2 failed(retry=5) en pending_batch, meta NO existe aún
    for i in range(3):
        _insert_batch("sending", 0)
    for i in range(2):
        _insert_batch("failed", 5)

    # Act
    var result: Dictionary = _repo.run_migrations()

    # Assert: applied + counts
    assert_eq(result.get("applied", false), true, "applied debe ser true en 1ra corrida")
    assert_eq(int(result.get("recovered_sending", 0)), 3, "Debió recuperar 3 sending")
    assert_eq(int(result.get("requeued_failed", 0)), 2, "Debió requeue 2 failed")
    # Assert: stuck data flipped
    assert_eq(_count_status("sending"), 0, "No deben quedar sending")
    assert_eq(_count_status("failed"), 0, "No deben quedar failed")
    assert_eq(_count_status("pending"), 5, "Los 5 deben estar pending")
    # Assert: schema_version bumped to '2'
    assert_eq(_read_schema_version(), "2", "schema_version debe ser '2' tras la migración")


func test_run_migrations_second_run_is_noop():
    # Arrange: 1ra corrida aplica
    _insert_batch("sending", 0)
    var first_result: Dictionary = _repo.run_migrations()
    assert_eq(first_result.get("applied", false), true, "Pre: 1ra corrida aplicó")

    # Insert NUEVOS stuck rows DESPUÉS de la migración
    _insert_batch("sending", 0)
    _insert_batch("failed", 5)

    # Act: 2da corrida
    var second_result: Dictionary = _repo.run_migrations()

    # Assert: 2da corrida es no-op
    assert_eq(second_result.get("applied", false), false, "2da corrida debe ser no-op")
    assert_eq(int(second_result.get("recovered_sending", 0)), 0, "0 recovered en no-op")
    assert_eq(int(second_result.get("requeued_failed", 0)), 0, "0 requeued en no-op")
    # Los nuevos stuck NO fueron tocados (idempotente: schema_version='2' bloquea)
    assert_eq(_count_status("sending"), 1, "Sending nuevo NO se toca en 2da corrida")
    assert_eq(_count_status("failed"), 1, "Failed nuevo NO se toca en 2da corrida")
    # schema_version sigue en '2'
    assert_eq(_read_schema_version(), "2", "schema_version debe seguir en '2'")


func test_run_migrations_creates_meta_table_if_missing():
    # Arrange: pending_batch con 1 sending (no se necesita más). No tocamos meta.
    _insert_batch("sending", 0)

    # Act
    var result: Dictionary = _repo.run_migrations()

    # Assert: la tabla meta fue creada internamente
    assert_eq(result.get("applied", false), true, "Migración aplicó (creó meta internamente)")
    assert_eq(_read_schema_version(), "2", "schema_version debe ser '2' tras crear meta")


# ============================================================================
# recover_sending() tests (S-P1-R1.1, NFR-IDEM-2)
# ============================================================================

func test_recover_sending_returns_count_and_flips_status():
    # Arrange: 9 sending con last_attempt_at viejo (10 min) + 1 pending
    for i in range(9):
        _insert_batch("sending", 0, "datetime('now', '-10 minutes')")
    _insert_batch("pending", 0)

    # Act
    var recovered: int = _repo.recover_sending(5)

    # Assert
    assert_eq(recovered, 9, "Debió recuperar 9")
    assert_eq(_count_status("sending"), 0, "No deben quedar sending")
    assert_eq(_count_status("pending"), 10, "Los 10 deben estar pending (9 recovered + 1 untouched)")


func test_recover_sending_preserves_last_attempt_at_and_retry_count():
    # Arrange: 1 sending con retry_count=3 y last_attempt_at específico
    var old_time_expr: String = "datetime('now', '-10 minutes')"
    var batch_id: String = _insert_batch("sending", 3, old_time_expr)

    # Act
    _repo.recover_sending(5)

    # Assert: el row ahora está pending pero conserva last_attempt_at y retry_count
    var rows: Array = _repo._db.select_rows("pending_batch", "id = '%s'" % batch_id, ["status", "retry_count", "last_attempt_at"])
    assert_eq(rows.size(), 1, "Debe haber 1 row")
    assert_eq(str(rows[0].get("status")), "pending", "Status debe ser pending")
    assert_eq(int(rows[0].get("retry_count")), 3, "retry_count se preserva (auditoría)")
    # last_attempt_at no es NULL (preservado)
    assert_ne(str(rows[0].get("last_attempt_at")), "", "last_attempt_at se preserva")


func test_recover_sending_respects_max_age_minutes():
    # Arrange: 5 sending recientes (1 min) + 5 sending viejos (10 min)
    for i in range(5):
        _insert_batch("sending", 0, "datetime('now', '-1 minutes')")
    for i in range(5):
        _insert_batch("sending", 0, "datetime('now', '-10 minutes')")

    # Act
    var recovered: int = _repo.recover_sending(5)

    # Assert
    assert_eq(recovered, 5, "Solo los 5 viejos (>=5 min) se recuperan")
    assert_eq(_count_status("sending"), 5, "Los 5 recientes quedan en sending")
    assert_eq(_count_status("pending"), 5, "Los 5 viejos van a pending")


func test_recover_sending_ignores_non_sending_rows():
    # Arrange: 3 pending, 2 failed, 1 completed (todos con last_attempt_at viejo)
    for i in range(3):
        _insert_batch("pending", 0, "datetime('now', '-10 minutes')")
    for i in range(2):
        _insert_batch("failed", 0, "datetime('now', '-10 minutes')")
    _insert_batch("completed", 0, "datetime('now', '-10 minutes')")

    # Act
    var recovered: int = _repo.recover_sending(5)

    # Assert
    assert_eq(recovered, 0, "Solo se recuperan sending; otros estados NO se tocan")
    assert_eq(_count_status("pending"), 3, "Pending intactos")
    assert_eq(_count_status("failed"), 2, "Failed intactos")
    assert_eq(_count_status("completed"), 1, "Completed intactos")


func test_recover_sending_is_idempotent():
    # Arrange: 3 sending viejos
    for i in range(3):
        _insert_batch("sending", 0, "datetime('now', '-10 minutes')")

    # Act
    var first: int = _repo.recover_sending(5)
    var second: int = _repo.recover_sending(5)

    # Assert
    assert_eq(first, 3, "1ra llamada recupera 3")
    assert_eq(second, 0, "2da llamada es no-op (idempotente — ya no hay sending)")


# ============================================================================
# requeue_failed() tests (S-P1-R2.1, NFR-IDEM-2)
# ============================================================================

func test_requeue_failed_resets_retry_count_and_status():
    # Arrange: 21 failed con retry_count=5
    for i in range(21):
        _insert_batch("failed", 5, "datetime('now', '-1 hours')")

    # Act
    var requeued: int = _repo.requeue_failed(5)

    # Assert
    assert_eq(requeued, 21, "Debió requeue 21")
    assert_eq(_count_status("failed"), 0, "No quedan failed")
    assert_eq(_count_status("pending"), 21, "Los 21 van a pending")
    # Verificar que retry_count se reseteó
    var rows: Array = _repo._db.select_rows("pending_batch", "status = 'pending'", ["retry_count"])
    assert_eq(rows.size(), 21, "21 rows pending")
    for row in rows:
        assert_eq(int(row.get("retry_count")), 0, "retry_count se resetea a 0")


func test_requeue_failed_does_not_touch_below_threshold():
    # Arrange: 4 failed con retry_count=3 (no deben tocarse) + 2 con retry_count=5 (sí)
    for i in range(4):
        _insert_batch("failed", 3, "datetime('now', '-1 hours')")
    for i in range(2):
        _insert_batch("failed", 5, "datetime('now', '-1 hours')")

    # Act
    var requeued: int = _repo.requeue_failed(5)

    # Assert
    assert_eq(requeued, 2, "Solo los 2 con retry_count >= 5 se requeuean")
    assert_eq(_count_status("failed"), 4, "Los 4 con retry_count=3 quedan en failed")
    assert_eq(_count_status("pending"), 2, "Los 2 con retry_count=5 van a pending")


func test_requeue_failed_preserves_payload_and_last_error():
    # Arrange: 1 failed con payload custom y last_error
    var custom_payload: Dictionary = {"session_id": "sess-1", "foo": "bar", "statements": [1, 2, 3]}
    var batch_id: String = _insert_batch("failed", 5, "datetime('now', '-1 hours')", custom_payload)
    var q_err: String = "UPDATE pending_batch SET last_error = ? WHERE id = ?"
    _repo._db.query_with_values(q_err, ["previous failure context", batch_id])

    # Act
    _repo.requeue_failed(5)

    # Assert: row ahora pending, payload preservado, last_error preservado
    var rows: Array = _repo._db.select_rows("pending_batch", "id = '%s'" % batch_id, ["status", "payload", "last_error", "retry_count"])
    assert_eq(rows.size(), 1)
    var row: Dictionary = rows[0]
    assert_eq(str(row.get("status")), "pending", "Status pasó a pending")
    assert_eq(int(row.get("retry_count")), 0, "retry_count se reseteó a 0")
    assert_eq(str(row.get("last_error")), "previous failure context", "last_error preservado para auditoría")
    var stored_payload: String = str(row.get("payload"))
    assert_true(stored_payload.contains("sess-1"), "payload.session_id preservado")
    assert_true(stored_payload.contains("bar"), "payload.foo preservado")


func test_requeue_failed_is_idempotent():
    # Arrange: 3 failed con retry_count=5
    for i in range(3):
        _insert_batch("failed", 5, "datetime('now', '-1 hours')")

    # Act
    var first: int = _repo.requeue_failed(5)
    var second: int = _repo.requeue_failed(5)

    # Assert
    assert_eq(first, 3, "1ra llamada requeue 3")
    assert_eq(second, 0, "2da llamada es no-op (ya no hay failed con retry>=5)")


# ============================================================================
# cleanup_terminal() tests (REQ-P1-R3, NFR-IDEM-5)
# ============================================================================

func test_cleanup_terminal_removes_completed_and_failed_aged():
    # Arrange: 3 completed + 2 failed viejos (10 días), 1 completed reciente
    for i in range(3):
        _insert_batch("completed", 0, "datetime('now', '-10 days')")
    for i in range(2):
        _insert_batch("failed", 0, "datetime('now', '-10 days')")
    _insert_batch("completed", 0, "datetime('now', '-1 days')")

    # Act
    var deleted: int = _repo.cleanup_terminal(7)

    # Assert
    assert_eq(deleted, 5, "Debió eliminar 5 (3 completed + 2 failed viejos)")
    assert_eq(_count_status("completed"), 1, "Queda 1 completed (el reciente)")
    assert_eq(_count_status("failed"), 0, "No quedan failed")


func test_cleanup_terminal_keeps_pending_and_sending():
    # Arrange: 2 pending + 2 sending (viejos pero no-terminal) + 1 completed viejo
    for i in range(2):
        _insert_batch("pending", 0, "datetime('now', '-10 days')")
    for i in range(2):
        _insert_batch("sending", 0, "datetime('now', '-10 days')")
    _insert_batch("completed", 0, "datetime('now', '-10 days')")

    # Act
    var deleted: int = _repo.cleanup_terminal(7)

    # Assert
    assert_eq(deleted, 1, "Solo el completed se elimina; pending/sending no son terminal")
    assert_eq(_count_status("pending"), 2, "Pending intactos (no son terminal)")
    assert_eq(_count_status("sending"), 2, "Sending intactos (no son terminal)")


func test_cleanup_terminal_is_idempotent():
    # Arrange: 1 completed viejo
    _insert_batch("completed", 0, "datetime('now', '-10 days')")

    # Act
    var first: int = _repo.cleanup_terminal(7)
    var second: int = _repo.cleanup_terminal(7)

    # Assert
    assert_eq(first, 1, "1ra llamada elimina 1")
    assert_eq(second, 0, "2da llamada es no-op (DELETE es naturalmente idempotente)")
