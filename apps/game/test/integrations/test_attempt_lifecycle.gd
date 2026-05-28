# test_attempt_lifecycle.gd
extends GutTest

var service: XAPIService

func before_each() -> void:
    service = XAPIService.new()

func after_each() -> void:
    if service:
        service.queue_free()
    service = null

func test_full_attempt_lifecycle() -> void:
    # 1. Start segment tracking
    service.start_segment_tracking(1, "student1")
    assert_eq(service._is_tracking, true)
    assert_eq(service._current_segment_id, 1)

    # 2. Begin attempt
    service.increment_attempt()
    assert_eq(service._attempts_count, 1)

    # 3. Execute blocks
    service.block_executed("block_a")
    service.block_executed("block_b")
    service.block_executed("block_c")
    assert_eq(service._blocks_executed.size(), 3)

    # 4. End attempt
    service.end_attempt(["block_a", "block_b", "block_c"], true, 5.0)
    assert_eq(service._attempts_history.size(), 1)
    assert_eq(service._attempts_history[0].success, true)
    assert_eq(service._attempts_history[0].blocks_count, 3)
    assert_eq(service._attempts_history[0].time, 5.0)
    assert_eq(service._is_new_attempt, true)

    # 5. End segment tracking
    var analytics: Dictionary = service.end_segment_tracking(true)
    assert_eq(analytics.segment_id, 1)
    assert_eq(analytics.actor_id, "student1")
    assert_eq(analytics.summary.success, true)
    assert_eq(analytics.summary.attempts, 1)
    assert_eq(analytics.summary.blocks_count, 3)
    assert_gt(analytics.summary.time, 0.0)
    assert_eq(analytics.summary.errors, 0)
    assert_eq(analytics.attempts.size(), 1)
    assert_eq(analytics.retry_count, 1)

    # 6. Verify tracking is now inactive
    assert_eq(service._is_tracking, false)

func test_attempt_lifecycle_with_multiple_attempts() -> void:
    service.start_segment_tracking(1, "student1")

    # Attempt 1 - fail
    service.increment_attempt()
    service.block_executed("block_a")
    service.end_attempt(["block_a"], false, 2.0)

    # Attempt 2 - success (blocks get cleared by _is_new_attempt due to end_attempt)
    service.increment_attempt()
    service.block_executed("block_b")
    service.block_executed("block_c")
    service.end_attempt(["block_b", "block_c"], true, 3.0)

    var analytics: Dictionary = service.end_segment_tracking(true)

    assert_eq(analytics.summary.attempts, 2)
    assert_eq(analytics.summary.blocks_count, 2)
    assert_eq(analytics.attempts.size(), 2)
    assert_eq(analytics.attempts[0].success, false)
    assert_eq(analytics.attempts[1].success, true)
