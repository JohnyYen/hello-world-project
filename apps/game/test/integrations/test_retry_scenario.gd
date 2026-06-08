# test_retry_scenario.gd
extends GutTest

var service: XAPIService

func before_each() -> void:
    service = XAPIService.new()

func after_each() -> void:
    if service:
        service.queue_free()
    service = null

func test_retry_flow_without_reset() -> void:
    service.start_segment_tracking(1, "actor1")

    # Attempt 1 - fails
    service.increment_attempt()
    service.end_attempt(["block_a"], false, 1.0)

    # Attempt 2 - fails
    service.increment_attempt()
    service.end_attempt(["block_b"], false, 2.0)

    # Attempt 3 - succeeds
    service.increment_attempt()
    service.end_attempt(["block_c"], true, 1.5)

    var analytics: Dictionary = service.end_segment_tracking(true)

    assert_eq(service._attempts_history.size(), 3)
    assert_eq(service._attempts_history[0].success, false)
    assert_eq(service._attempts_history[1].success, false)
    assert_eq(service._attempts_history[2].success, true)
    assert_eq(analytics.retry_count, 3)
    assert_eq(analytics.summary.success, true)

func test_retry_with_reset_preserves_history() -> void:
    service.start_segment_tracking(1, "actor1")
    service.set_retry_mode(true)

    # Attempt 1 - fails → reset
    service.increment_attempt()
    service.block_executed("block_a")
    service.end_attempt(["block_a"], false, 1.0)
    service.reset_tracking()

    assert_eq(service._blocks_executed.size(), 0)
    assert_eq(service._attempts_count, 0)

    # Attempt 2 - fails → reset
    service.increment_attempt()
    service.block_executed("block_b")
    service.end_attempt(["block_b"], false, 2.0)
    service.reset_tracking()

    # Attempt 3 - succeeds (no reset needed after final attempt)
    service.increment_attempt()
    service.block_executed("block_c")
    service.end_attempt(["block_c"], true, 1.5)

    var analytics: Dictionary = service.end_segment_tracking(true)

    assert_eq(service._attempts_history.size(), 3)
    assert_eq(service._attempts_history[0].success, false)
    assert_eq(service._attempts_history[1].success, false)
    assert_eq(service._attempts_history[2].success, true)

    assert_eq(analytics.summary.success, true)
    assert_eq(analytics.attempts.size(), 3)

func test_retry_count_after_reset() -> void:
    service.start_segment_tracking(1, "actor1")
    service.set_retry_mode(true)

    service.increment_attempt()
    service.end_attempt(["block_a"], false, 1.0)
    service.reset_tracking()

    service.increment_attempt()
    service.end_attempt(["block_b"], false, 2.0)
    service.reset_tracking()

    service.increment_attempt()
    service.end_attempt(["block_c"], true, 1.5)

    var analytics: Dictionary = service.end_segment_tracking(true)

    assert_eq(analytics.attempts.size(), 3)
    assert_eq(analytics.retry_count, 1)
    assert_eq(analytics.summary.attempts, 1)

func test_reset_tracking_preserves_history_in_retry_mode() -> void:
    service.start_segment_tracking(1, "actor1")
    service.set_retry_mode(true)

    service.end_attempt(["block_a"], false, 1.0)
    assert_eq(service._attempts_history.size(), 1)

    service.reset_tracking()

    assert_eq(service._attempts_history.size(), 1)
    assert_eq(service._attempts_history[0].success, false)
