# test_game_controller.gd
extends GutTest

var controller: GameController

func before_each() -> void:
    controller = GameController.new()
    add_child(controller)

func after_each() -> void:
    if controller and controller.get_parent():
        remove_child(controller)
    if controller:
        controller.queue_free()
    controller = null

# =============================================================================
# begin_segment tests
# =============================================================================

func test_begin_segment_sets_level_id() -> void:
    controller.begin_segment(5, "student1")

    assert_eq(controller._current_level_id, 5)
    assert_eq(controller._current_actor_id, "student1")

func test_begin_segment_delegates_to_xapi() -> void:
    _XAPIService.start_segment_tracking(0, "")
    controller.begin_segment(10, "test_actor")

    assert_eq(_XAPIService._current_segment_id, 10)
    assert_eq(_XAPIService._current_actor_id, "test_actor")

func test_begin_segment_creates_attempted_xapi_statement() -> void:
    _XAPIService.start_segment_tracking(0, "")
    var initial_pending := _XAPIService.get_pending_statements(100).size()

    controller.begin_segment(7, "actor_for_test")

    var pending := _XAPIService.get_pending_statements(100)
    var attempted_found := false
    for stmt in pending:
        if stmt.object_id == "7" and stmt.verb_display == "intentó":
            attempted_found = true
            break
    assert_eq(attempted_found, true,
        "begin_segment debe crear un statement 'intentó' para el segmento")

# =============================================================================
# begin_attempt tests
# =============================================================================

func test_begin_attempt_increments_counter() -> void:
    assert_eq(controller._attempts_count, 0)
    controller.begin_attempt()

    assert_eq(controller._attempts_count, 1)

func test_begin_attempt_multiple_calls() -> void:
    controller.begin_attempt()
    controller.begin_attempt()
    controller.begin_attempt()

    assert_eq(controller._attempts_count, 3)

func test_begin_attempt_delegates_to_xapi() -> void:
    _XAPIService.start_segment_tracking(1, "actor1")
    var initial_count := _XAPIService._attempts_count

    controller.begin_attempt()

    assert_eq(_XAPIService._attempts_count, initial_count + 1)

# =============================================================================
# record_attempt tests
# =============================================================================

func test_record_attempt_delegates_to_xapi() -> void:
    _XAPIService.start_segment_tracking(1, "actor1")
    controller.record_attempt(["block_a"], true, 1.5)

    assert_eq(_XAPIService._attempts_history.size(), 1)
    assert_eq(_XAPIService._attempts_history[0].success, true)
    assert_eq(_XAPIService._attempts_history[0].blocks.size(), 1)

func test_record_attempt_multiple() -> void:
    _XAPIService.start_segment_tracking(1, "actor1")
    controller.record_attempt(["a"], false, 1.0)
    controller.record_attempt(["b", "c"], true, 2.5)

    assert_eq(_XAPIService._attempts_history.size(), 2)
    assert_eq(_XAPIService._attempts_history[0].success, false)
    assert_eq(_XAPIService._attempts_history[1].blocks_count, 2)

# =============================================================================
# add_tracking_event tests
# =============================================================================

func test_add_tracking_event_delegates_to_xapi() -> void:
    _XAPIService.start_segment_tracking(1, "actor1")
    controller.add_tracking_event("custom_event", {"key": "val"})

    assert_eq(_XAPIService._custom_events.size(), 1)
    assert_eq(_XAPIService._custom_events[0].event_name, "custom_event")

# =============================================================================
# reset_level_tracking tests
# =============================================================================

func test_reset_level_tracking_clears_state() -> void:
    _XAPIService.start_segment_tracking(1, "actor1")
    controller.begin_attempt()
    controller.record_attempt(["a"], true, 1.0)
    controller.reset_level_tracking()

    assert_eq(controller._attempts_count, 0)
    assert_eq(controller._is_retry_mode, false)
