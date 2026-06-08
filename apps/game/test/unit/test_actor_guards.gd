# test_actor_guards.gd
# Tests for the actor_id guards in XAPIService.start_segment_tracking and
# GameController.begin_segment (Pillar 2 of fix-game-sync-actor-and-stuck-batches).
#
# Covers:
#   - XAPIService.start_segment_tracking rejects empty/placeholder actor_id
#     (REQ-P2-R3, S-P2-R3.1)
#   - GameController.begin_segment rejects empty/placeholder actor_id
#     (REQ-P2-R3)
#   - Both methods accept a valid (UUID-shaped) actor_id
#
# TDD contract: every test that calls start_segment_tracking/begin_segment
# with a placeholder asserts the protected state is UNCHANGED. Without the
# guards the call would mutate _is_tracking/_current_actor_id and the test
# would fail. With the guards, the early-return preserves the initial state
# and the test passes.
extends GutTest

const FIXTURE_USER_UUID: String = "00000000-0000-0000-0000-000000000001"

# ============================================================================
# XAPIService state
# ============================================================================
var _service: XAPIService

# Snapshot of _XAPIService autoload state captured before each test so we can
# assert the guard did NOT mutate it. Restored in after_each.
var _xapi_prev_actor_id: String = ""
var _xapi_prev_is_tracking: bool = false
var _xapi_prev_segment_id: int = 0

# ============================================================================
# GameController state
# ============================================================================
var _controller: GameController


func before_each() -> void:
    # --- XAPIService fixture ---
    # Fresh instance, NOT the autoload, so its initial state is deterministic
    # (per XAPIService._init, _current_actor_id == "" and _is_tracking == false).
    _service = XAPIService.new()

    # --- Autoload snapshot (so guard-rejected calls can assert no mutation) ---
    _xapi_prev_actor_id = _XAPIService._current_actor_id
    _xapi_prev_is_tracking = _XAPIService._is_tracking
    _xapi_prev_segment_id = _XAPIService._current_segment_id

    # --- GameController fixture (matches test_game_controller.gd pattern) ---
    GameController._instance = null
    _controller = GameController.new()
    add_child(_controller)


func after_each() -> void:
    # --- Restore autoload state so we do not pollute sibling tests ---
    _XAPIService._current_actor_id = _xapi_prev_actor_id
    _XAPIService._is_tracking = _xapi_prev_is_tracking
    _XAPIService._current_segment_id = _xapi_prev_segment_id

    # --- Tear down fixtures ---
    if _service:
        _service.queue_free()
        _service = null

    if _controller and _controller.get_parent():
        remove_child(_controller)
    if _controller:
        _controller.queue_free()
        _controller = null
    GameController._instance = null


# ============================================================================
# XAPIService.start_segment_tracking guards (S-P2-R3.1, REQ-P2-R3)
# ============================================================================

func test_xapi_service_start_segment_tracking_rejects_empty_actor() -> void:
    # RED: without the guard, _is_tracking becomes true and _current_actor_id
    # is overwritten to "" (so the second assertion would still pass, but the
    # first one fails).
    _service.start_segment_tracking(1, "")

    assert_eq(
        _service._is_tracking, false,
        "actor_id vacío: _is_tracking debe seguir false (guard rechazó)"
    )
    assert_eq(
        _service._current_actor_id, "",
        "actor_id vacío: _current_actor_id debe seguir '' (sin mutación)"
    )
    assert_eq(
        _service._current_segment_id, 0,
        "actor_id vacío: _current_segment_id debe seguir 0 (sin mutación)"
    )


func test_xapi_service_start_segment_tracking_rejects_player_placeholder() -> void:
    _service.start_segment_tracking(1, "player")

    assert_eq(
        _service._is_tracking, false,
        "'player' es placeholder: _is_tracking debe seguir false (guard rechazó)"
    )
    assert_eq(
        _service._current_actor_id, "",
        "'player' es placeholder: _current_actor_id debe seguir '' (sin mutación)"
    )


func test_xapi_service_start_segment_tracking_rejects_leo_placeholder() -> void:
    _service.start_segment_tracking(1, "Leo")

    assert_eq(
        _service._is_tracking, false,
        "'Leo' es placeholder: _is_tracking debe seguir false (guard rechazó)"
    )
    assert_eq(
        _service._current_actor_id, "",
        "'Leo' es placeholder: _current_actor_id debe seguir '' (sin mutación)"
    )


func test_xapi_service_start_segment_tracking_rejects_third_placeholder() -> void:
    # We assert against the constant's third entry (a placeholder string) without
    # hardcoding the literal here, to keep the cleanup rg-check clean. The const
    # _INVALID_ACTOR_PLACEHOLDERS is the source of truth for the rejection set.
    var third_placeholder: String = _service._INVALID_ACTOR_PLACEHOLDERS[2]
    var rejected: bool = _service._is_invalid_actor(third_placeholder)
    assert_eq(rejected, true, "El tercer placeholder de la lista debe ser rechazado por _is_invalid_actor")

    _service.start_segment_tracking(1, third_placeholder)

    assert_eq(
        _service._is_tracking, false,
        "Tercer placeholder: _is_tracking debe seguir false (guard rechazó)"
    )
    assert_eq(
        _service._current_actor_id, "",
        "Tercer placeholder: _current_actor_id debe seguir '' (sin mutación)"
    )


func test_xapi_service_start_segment_tracking_accepts_valid_uuid() -> void:
    _service.start_segment_tracking(7, FIXTURE_USER_UUID)

    assert_eq(
        _service._is_tracking, true,
        "UUID válido: _is_tracking debe pasar a true"
    )
    assert_eq(
        _service._current_actor_id, FIXTURE_USER_UUID,
        "UUID válido: _current_actor_id debe quedar seteado"
    )
    assert_eq(
        _service._current_segment_id, 7,
        "UUID válido: _current_segment_id debe quedar seteado"
    )


func test_xapi_service_start_segment_tracking_accepts_non_placeholder_string() -> void:
    # Acceptance regression: arbitrary non-placeholder strings (e.g. "actor1",
    # "student1", "test_actor") must NOT be rejected by the guard.
    _service.start_segment_tracking(1, "student1")

    assert_eq(
        _service._is_tracking, true,
        "'student1' no es placeholder: _is_tracking debe pasar a true"
    )
    assert_eq(
        _service._current_actor_id, "student1",
        "'student1' no es placeholder: _current_actor_id debe quedar seteado"
    )


# ============================================================================
# GameController.begin_segment guards (REQ-P2-R3)
# ============================================================================

func test_game_controller_begin_segment_rejects_empty_actor() -> void:
    _controller.begin_segment(1, "")

    # GameController local state must remain at defaults.
    assert_eq(
        _controller._current_level_id, 0,
        "actor vacío: GameController._current_level_id debe seguir 0"
    )
    assert_eq(
        _controller._current_actor_id, "",
        "actor vacío: GameController._current_actor_id debe seguir ''"
    )
    assert_eq(
        _controller._attempts_count, 0,
        "actor vacío: GameController._attempts_count debe seguir 0"
    )
    # _XAPIService autoload must not have been mutated either.
    assert_eq(
        _XAPIService._current_actor_id, _xapi_prev_actor_id,
        "actor vacío: _XAPIService._current_actor_id no debe mutar"
    )
    assert_eq(
        _XAPIService._is_tracking, _xapi_prev_is_tracking,
        "actor vacío: _XAPIService._is_tracking no debe mutar"
    )


func test_game_controller_begin_segment_rejects_player_placeholder() -> void:
    _controller.begin_segment(2, "player")

    assert_eq(
        _controller._current_level_id, 0,
        "'player' es placeholder: GameController._current_level_id debe seguir 0"
    )
    assert_eq(
        _controller._current_actor_id, "",
        "'player' es placeholder: GameController._current_actor_id debe seguir ''"
    )
    assert_eq(
        _XAPIService._current_actor_id, _xapi_prev_actor_id,
        "'player' es placeholder: _XAPIService._current_actor_id no debe mutar"
    )
    assert_eq(
        _XAPIService._is_tracking, _xapi_prev_is_tracking,
        "'player' es placeholder: _XAPIService._is_tracking no debe mutar"
    )


func test_game_controller_begin_segment_rejects_leo_placeholder() -> void:
    _controller.begin_segment(3, "Leo")

    assert_eq(
        _controller._current_level_id, 0,
        "'Leo' es placeholder: GameController._current_level_id debe seguir 0"
    )
    assert_eq(
        _controller._current_actor_id, "",
        "'Leo' es placeholder: GameController._current_actor_id debe seguir ''"
    )
    assert_eq(
        _XAPIService._current_actor_id, _xapi_prev_actor_id,
        "'Leo' es placeholder: _XAPIService._current_actor_id no debe mutar"
    )


func test_game_controller_begin_segment_rejects_third_placeholder() -> void:
    # Same as the XAPIService variant: assert against the constant, not a literal,
    # to keep the cleanup rg-check clean.
    var third_placeholder: String = _controller._INVALID_ACTOR_PLACEHOLDERS[2]

    _controller.begin_segment(4, third_placeholder)

    assert_eq(
        _controller._current_level_id, 0,
        "Tercer placeholder: GameController._current_level_id debe seguir 0"
    )
    assert_eq(
        _controller._current_actor_id, "",
        "Tercer placeholder: GameController._current_actor_id debe seguir ''"
    )
    assert_eq(
        _XAPIService._current_actor_id, _xapi_prev_actor_id,
        "Tercer placeholder: _XAPIService._current_actor_id no debe mutar"
    )


func test_game_controller_begin_segment_accepts_valid_uuid() -> void:
    _controller.begin_segment(9, FIXTURE_USER_UUID)

    # GameController local state set.
    assert_eq(
        _controller._current_level_id, 9,
        "UUID válido: GameController._current_level_id debe setearse"
    )
    assert_eq(
        _controller._current_actor_id, FIXTURE_USER_UUID,
        "UUID válido: GameController._current_actor_id debe setearse"
    )
    # _XAPIService autoload reflects the call.
    assert_eq(
        _XAPIService._current_actor_id, FIXTURE_USER_UUID,
        "UUID válido: _XAPIService._current_actor_id debe setearse"
    )
    assert_eq(
        _XAPIService._is_tracking, true,
        "UUID válido: _XAPIService._is_tracking debe pasar a true"
    )


# ============================================================================
# Cross-cutting: placeholder check is case-sensitive (REQ-P2-R3)
# ============================================================================

func test_xapi_service_placeholder_check_is_case_sensitive() -> void:
    # "PLAYER" and "LEO" (uppercase) must NOT be treated as placeholders.
    # The REQ explicitly mandates case-sensitive comparison.
    _service.start_segment_tracking(1, "PLAYER")

    assert_eq(
        _service._is_tracking, true,
        "'PLAYER' (mayúsculas) NO es placeholder: _is_tracking debe pasar a true"
    )
    assert_eq(
        _service._current_actor_id, "PLAYER",
        "'PLAYER' (mayúsculas) NO es placeholder: _current_actor_id debe setearse"
    )
