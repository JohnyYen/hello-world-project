# test_xapi_service.gd
extends GutTest

var service: XAPIService

# State vars for signal test
var _signal_emitted: bool = false
var _received_data: Dictionary = {}

func _on_segment_analytics_ready(data: Dictionary) -> void:
    _signal_emitted = true
    _received_data = data

func before_each() -> void:
    service = XAPIService.new()
    _signal_emitted = false
    _received_data = {}

func after_each() -> void:
    if service:
        service.queue_free()
    service = null

# =============================================================================
# end_attempt tests
# =============================================================================

func test_end_attempt_appends_to_history() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_attempt(["block_a", "block_b"], true, 2.5)

    assert_eq(service._attempts_history.size(), 1)
    var entry: Dictionary = service._attempts_history[0]
    assert_eq(entry.attempt_number, 1)
    assert_eq(entry.blocks.size(), 2)
    assert_eq(entry.success, true)
    assert_gt(entry.time, 0.0)

func test_end_attempt_appends_multiple_attempts() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_attempt(["block_a"], false, 1.0)
    service.end_attempt(["block_b"], true, 2.0)

    assert_eq(service._attempts_history.size(), 2)
    assert_eq(service._attempts_history[0].attempt_number, 1)
    assert_eq(service._attempts_history[1].attempt_number, 2)
    assert_eq(service._attempts_history[0].success, false)
    assert_eq(service._attempts_history[1].success, true)

func test_end_attempt_stores_block_count() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_attempt(["a", "b", "c"], true, 1.0)

    assert_eq(service._attempts_history[0].blocks_count, 3)
    assert_eq(service._attempts_history[0].blocks.size(), 3)

func test_end_attempt_guarded_by_is_tracking() -> void:
    service.end_attempt(["block_a"], true, 1.0)
    assert_eq(service._attempts_history.size(), 0)

func test_end_attempt_sets_is_new_attempt() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_attempt(["block_a"], true, 1.0)
    assert_eq(service._is_new_attempt, true)

# =============================================================================
# track_event tests
# =============================================================================

func test_track_event_appends_to_custom_events() -> void:
    service.start_segment_tracking(1, "actor1")
    service.track_event("hint_shown", {"hint_id": 1})

    assert_eq(service._custom_events.size(), 1)
    var event: Dictionary = service._custom_events[0]
    assert_eq(event.event_name, "hint_shown")
    assert_eq(event.event_data.hint_id, 1)

func test_track_event_multiple_events() -> void:
    service.start_segment_tracking(1, "actor1")
    service.track_event("event_a")
    service.track_event("event_b", {"key": "val"})

    assert_eq(service._custom_events.size(), 2)
    assert_eq(service._custom_events[0].event_name, "event_a")
    assert_eq(service._custom_events[1].event_name, "event_b")

func test_track_event_guarded_by_is_tracking() -> void:
    service.track_event("some_event")
    assert_eq(service._custom_events.size(), 0)

func test_track_event_without_data() -> void:
    service.start_segment_tracking(1, "actor1")
    service.track_event("simple_event")

    assert_eq(service._custom_events.size(), 1)
    assert_eq(service._custom_events[0].event_name, "simple_event")
    assert_eq(service._custom_events[0].event_data, {})

# =============================================================================
# reset_tracking tests
# =============================================================================

func test_reset_tracking_clears_blocks_and_attempts() -> void:
    service.start_segment_tracking(1, "actor1")
    service.increment_attempt()
    service.block_executed("block_a")
    service.reset_tracking()

    assert_eq(service._blocks_executed.size(), 0)
    assert_eq(service._attempts_count, 0)
    assert_eq(service._is_new_attempt, false)

func test_reset_tracking_keeps_history_in_retry_mode() -> void:
    service.start_segment_tracking(1, "actor1")
    service.set_retry_mode(true)
    service.end_attempt(["block_a"], false, 1.0)
    service.reset_tracking()

    assert_eq(service._attempts_history.size(), 1)
    assert_eq(service._custom_events.size(), 0)

func test_reset_tracking_clears_history_when_not_retry() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_attempt(["block_a"], false, 1.0)
    service.track_event("evt")
    service.reset_tracking()

    assert_eq(service._attempts_history.size(), 0)
    assert_eq(service._custom_events.size(), 0)

func test_reset_tracking_sets_is_tracking_true() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_segment_tracking(true)
    service.reset_tracking()

    assert_eq(service._is_tracking, true)

# =============================================================================
# set_retry_mode tests
# =============================================================================

func test_set_retry_mode_enables() -> void:
    service.start_segment_tracking(1, "actor1")
    service.set_retry_mode(true)
    assert_eq(service._is_retry_mode, true)

func test_set_retry_mode_disables() -> void:
    service.start_segment_tracking(1, "actor1")
    service.set_retry_mode(false)
    assert_eq(service._is_retry_mode, false)

# =============================================================================
# end_segment_tracking tests
# =============================================================================

func test_end_segment_tracking_returns_full_structure() -> void:
    service.start_segment_tracking(42, "test_actor")
    service.end_attempt(["block_a"], true, 1.0)
    var result: Dictionary = service.end_segment_tracking(true)

    assert_has(result, "segment_id")
    assert_has(result, "actor_id")
    assert_has(result, "timestamp")
    assert_has(result, "summary")
    assert_has(result, "attempts")
    assert_has(result, "custom_events")
    assert_has(result, "retry_count")
    assert_eq(result.segment_id, 42)
    assert_eq(result.actor_id, "test_actor")

func test_end_segment_tracking_summary_shape() -> void:
    service.start_segment_tracking(1, "actor1")
    service.increment_attempt()
    service.end_attempt(["block_a"], true, 1.0)
    var result: Dictionary = service.end_segment_tracking(true)
    var summary: Dictionary = result.summary

    assert_has(summary, "time")
    assert_has(summary, "errors")
    assert_has(summary, "score")
    assert_has(summary, "success")
    assert_has(summary, "attempts")
    assert_has(summary, "blocks_count")
    assert_eq(summary.success, true)
    assert_eq(summary.attempts, 1)
    assert_ge(summary.time, 0.0)

func test_end_segment_tracking_contains_attempts() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_attempt(["block_a"], false, 1.0)
    service.end_attempt(["block_b", "block_c"], true, 2.0)
    var result: Dictionary = service.end_segment_tracking(true)

    assert_eq(result.attempts.size(), 2)
    assert_eq(result.attempts[0].success, false)
    assert_eq(result.attempts[1].success, true)
    assert_eq(result.attempts[1].blocks.size(), 2)

func test_end_segment_tracking_contains_custom_events() -> void:
    service.start_segment_tracking(1, "actor1")
    service.track_event("hint_shown", {"id": 1})
    var result: Dictionary = service.end_segment_tracking(true)

    assert_eq(result.custom_events.size(), 1)
    assert_eq(result.custom_events[0].event_name, "hint_shown")

func test_end_segment_tracking_retry_count() -> void:
    service.start_segment_tracking(1, "actor1")
    service.increment_attempt()
    service.end_attempt(["block_a"], true, 1.0)
    var result: Dictionary = service.end_segment_tracking(true)

    assert_eq(result.retry_count, 1)
    assert_eq(result.summary.attempts, 1)

func test_end_segment_tracking_sets_is_tracking_false() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_segment_tracking(true)
    assert_eq(service._is_tracking, false)

func test_end_segment_tracking_guarded_by_is_tracking() -> void:
    var result: Dictionary = service.end_segment_tracking(true)
    assert_eq(result, {})

func test_end_segment_tracking_emits_signal() -> void:
    service.start_segment_tracking(1, "actor1")
    service.segment_analytics_ready.connect(_on_segment_analytics_ready)

    var result: Dictionary = service.end_segment_tracking(true)

    assert_eq(_signal_emitted, true)
    assert_eq(_received_data.segment_id, result.segment_id)

func test_end_segment_tracking_error_calculation() -> void:
    service.start_segment_tracking(1, "actor1")
    service.increment_attempt()
    service.end_attempt(["block_a"], true, 1.0)
    var result: Dictionary = service.end_segment_tracking(true)

    assert_eq(result.summary.errors, 0)

func test_end_segment_tracking_score_fail() -> void:
    service.start_segment_tracking(1, "actor1")
    service.end_attempt(["block_a"], false, 1.0)
    var result: Dictionary = service.end_segment_tracking(false)

    assert_eq(result.summary.score, 0.0)
    assert_eq(result.summary.success, false)
