# test_raw_stats_repository.gd
# Tests for RawStatsRepository - offline-first stats persistence
extends GutTest

var repo: RawStatsRepository

func before_each() -> void:
	repo = RawStatsRepository.new()

func after_each() -> void:
	if repo:
		repo.queue_free()
	repo = null

# =============================================================================
# create_table tests
# =============================================================================

func test_create_table_executes_idempotently() -> void:
	var result_1 := repo.create_table()
	assert_eq(result_1, true, "First create_table should succeed")
	
	# Second call should also succeed (idempotent)
	var result_2 := repo.create_table()
	assert_eq(result_2, true, "Second create_table should also succeed (idempotent)")

# =============================================================================
# save tests
# =============================================================================

func test_save_inserts_record_with_pending_status() -> void:
	repo.create_table()
	
	var stats := {
		"segment_id": 1,
		"actor_id": "test_actor_123",
		"attempt_count": 1,
		"error_count": 0,
		"hints_used_count": 0,
		"errors_details": {},
		"efficiency_rating": 100.0,
		"objectives_completed": 1
	}
	
	var record_id := repo.save(stats)
	assert_false(record_id.is_empty(), "save should return a record ID")
	
	# Verify the record was saved correctly
	var record := repo.get_by_id(record_id)
	assert_eq(record.segment_id, 1)
	assert_eq(record.actor_id, "test_actor_123")
	assert_eq(record.status, "pending_sync")

func test_save_generates_uuid_if_missing() -> void:
	repo.create_table()
	
	var stats := {
		"segment_id": 1,
		"actor_id": "test_actor"
	}
	
	var record_id := repo.save(stats)
	assert_false(record_id.is_empty())
	# UUID format check (basic)
	assert_true(record_id.length() >= 36, "Should be a valid UUID")

# =============================================================================
# get_pending_all tests
# =============================================================================

func test_get_pending_all_returns_only_pending() -> void:
	repo.create_table()
	
	# Save some records
	var id1 := repo.save({"segment_id": 1, "actor_id": "actor1"})
	var id2 := repo.save({"segment_id": 2, "actor_id": "actor2"})
	
	# Mark one as completed
	repo.mark_completed(id1)
	
	var pending := repo.get_pending_all(50)
	assert_eq(pending.size(), 1, "Only the uncompleted record should be pending")
	assert_eq(pending[0].id, id2)

func test_get_pending_all_orders_by_created_at() -> void:
	repo.create_table()
	
	var id1 := repo.save({"segment_id": 1, "actor_id": "a1"})
	# Simulate time passing
	OS.delay_msec(100)  # Small delay
	var id2 := repo.save({"segment_id": 2, "actor_id": "a2"})
	
	var pending := repo.get_pending_all(50)
	assert_eq(pending.size(), 2)
	assert_eq(pending[0].id, id1, "First record should come first chronologically")

# =============================================================================
# update_status tests
# =============================================================================

func test_update_status_changes_record_status() -> void:
	repo.create_table()
	
	var record_id := repo.save({"segment_id": 1, "actor_id": "actor1"})
	repo.update_status(record_id, "sending")
	
	var record := repo.get_by_id(record_id)
	assert_eq(record.status, "sending")

func test_update_status_clears_error_message_on_success() -> void:
	repo.create_table()
	
	var record_id := repo.save({"segment_id": 1, "actor_id": "actor1"})
	repo.update_status(record_id, "failed", "Initial error")
	repo.update_status(record_id, "pending_sync", "")  # Clear error
	
	var record := repo.get_by_id(record_id)
	assert_eq(record.error_message, "")

# =============================================================================
# mark_completed tests
# =============================================================================

func test_mark_completed_sets_status_completed() -> void:
	repo.create_table()
	
	var record_id := repo.save({"segment_id": 1, "actor_id": "actor1"})
	repo.mark_completed(record_id)
	
	var record := repo.get_by_id(record_id)
	assert_eq(record.status, "completed")

# =============================================================================
# mark_failed tests
# =============================================================================

func test_mark_failed_increments_retry_count() -> void:
	repo.create_table()
	
	var record_id := repo.save({"segment_id": 1, "actor_id": "actor1"})
	repo.mark_failed(record_id, 5)
	
	var record := repo.get_by_id(record_id)
	assert_eq(record.retry_count, 1)
	assert_eq(record.status, "pending_sync", "Should remain pending for retry")

func test_mark_failed_sets_failed_when_max_retries_reached() -> void:
	repo.create_table()
	
	var record_id := repo.save({"segment_id": 1, "actor_id": "actor1"})
	
	# Reach max retries - retry_count becomes 1 which equals max_retries 1
	repo.mark_failed(record_id, 1)
	
	var record := repo.get_by_id(record_id)
	assert_eq(record.status, "failed")
	assert_eq(record.error_message, "Max retries exceeded")

# =============================================================================
# get_stats tests
# =============================================================================

func test_get_stats_returns_counts() -> void:
	repo.create_table()
	
	repo.save({"segment_id": 1, "actor_id": "a1"})
	repo.save({"segment_id": 2, "actor_id": "a2"})
	repo.mark_completed(repo.save({"segment_id": 3, "actor_id": "a3"}))
	
	var stats := repo.get_stats()
	assert_eq(stats.pending_sync, 2)
	assert_eq(stats.completed, 1)
	assert_eq(stats.failed, 0)