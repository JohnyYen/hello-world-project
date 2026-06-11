# 002_create_raw_stats_table.gd
# Migration for offline-first raw statistics tracking
class_name CreateRawStatsTableMigration
extends Node

func run(db: SQLite) -> bool:
    var success := _create_raw_stats_table(db)
    if success:
        _create_indexes(db)
        print("Migration 002_create_raw_stats_table: OK")
    return success

func _create_raw_stats_table(db: SQLite) -> bool:
    var raw_stats_schema := {
        "id": {"data_type": "text", "primary_key": true},
        "segment_id": {"data_type": "integer", "not_null": true},
        "actor_id": {"data_type": "text", "not_null": true},
        "attempt_count": {"data_type": "integer", "default": "0"},
        "error_count": {"data_type": "integer", "default": "0"},
        "hints_used_count": {"data_type": "integer", "default": "0"},
        "errors_details": {"data_type": "text", "default": "{}"},  # JSON string
        "efficiency_rating": {"data_type": "real", "default": "0.0"},
        "objectives_completed": {"data_type": "integer", "default": "0"},
        "status": {"data_type": "text", "not_null": true, "default": "pending_sync"},
        "retry_count": {"data_type": "integer", "not_null": true, "default": "0"},
        "error_message": {"data_type": "text", "default": ""},
        "created_at": {"data_type": "text", "not_null": true},
        "last_sync_at": {"data_type": "text"}
    }
    var result := db.create_table("raw_stats", raw_stats_schema)
    return result

func _create_indexes(db: SQLite) -> void:
    db.query("CREATE INDEX IF NOT EXISTS idx_raw_stats_status ON raw_stats(status);")
    db.query("CREATE INDEX IF NOT EXISTS idx_raw_stats_segment ON raw_stats(segment_id);")
    db.query("CREATE INDEX IF NOT EXISTS idx_raw_stats_actor ON raw_stats(actor_id);")