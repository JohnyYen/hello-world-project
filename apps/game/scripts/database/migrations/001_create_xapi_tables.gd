# 001_create_xapi_tables.gd
class_name CreateXAPITablesMigration
extends Node

func run(db: SQLite) -> bool:
    _create_xapi_statement_table(db)
    _create_pending_batch_table(db)
    _create_indexes(db)
    print("Migration 001_create_xapi_tables: OK")
    return true

func _create_xapi_statement_table(db: SQLite) -> void:
    var xapi_statement_schema := {
        "id": {"data_type": "text", "primary_key": true},
        "verb_id": {"data_type": "text", "not_null": true},
        "verb_display": {"data_type": "text", "not_null": true},
        "object_type": {"data_type": "text", "not_null": true},
        "object_id": {"data_type": "text", "not_null": true},
        "object_name": {"data_type": "text", "not_null": true},
        "actor_id": {"data_type": "text", "not_null": true},
        "result_score_raw": {"data_type": "real"},
        "result_score_scaled": {"data_type": "real"},
        "result_success": {"data_type": "integer"},
        "result_completion": {"data_type": "integer"},
        "result_duration": {"data_type": "text"},
        "context_extensions": {"data_type": "text"},
        "timestamp": {"data_type": "text", "not_null": true},
        "created_at": {"data_type": "text", "not_null": true},
        "batch_id": {"data_type": "text"}
    }
    db.create_table("xapi_statement", xapi_statement_schema)

func _create_pending_batch_table(db: SQLite) -> void:
    var pending_batch_schema := {
        "id": {"data_type": "text", "primary_key": true},
        "statements": {"data_type": "text", "not_null": true},
        "payload": {"data_type": "text", "not_null": true},
        "status": {"data_type": "text", "not_null": true},
        "retry_count": {"data_type": "integer", "not_null": true, "default": "0"},
        "last_error": {"data_type": "text"},
        "created_at": {"data_type": "text", "not_null": true},
        "last_attempt_at": {"data_type": "text"}
    }
    db.create_table("pending_batch", pending_batch_schema)

func _create_indexes(db: SQLite) -> void:
    db.query("CREATE INDEX IF NOT EXISTS idx_xapi_batch ON xapi_statement(batch_id);")
    db.query("CREATE INDEX IF NOT EXISTS idx_xapi_timestamp ON xapi_statement(timestamp);")
    db.query("CREATE INDEX IF NOT EXISTS idx_batch_status ON pending_batch(status);")
