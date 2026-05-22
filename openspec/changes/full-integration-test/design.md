# Design: Full Integration Test for Godot Game Flow

## Technical Approach

A single GDScript file (`test/integrations/test_full_integration.gd`) that extends `Node` and uses `_ready()` as the entry point. Each integration concern (login, level run, sync) is a separate private function. The script instantiates production components via `class_name`, sequences async operations with `await`, and prints structured output for manual verification. No GUT, no assertions — pure orchestration and print-based validation.

The approach is modeled after `simple_test.gd` in `test/unit/engine/` — same `extends Node`, `_ready()` pattern — but scaled to exercise the full pipeline.

### Key Difference from Unit Tests

Unlike unit tests (which mock/stub), this test instantiates REAL components. `XAPIService`, `ApiClient`, `SyncBatchService` all extend `Node` and need `add_child()` for their `_ready()` to fire. This means the test script must manage the node lifecycle: add children, let `_ready()` execute, then proceed.

## Architecture Decisions

### Decision: Single-file Script (no TSCN)

**Choice**: Pure GDScript file, no `.tscn` scene companion.

**Alternatives considered**: TSCN + script pair (like `TestScene_3Runs.tscn`)

**Rationale**: The existing `TestScene_3Runs.tscn` references a `test_3runs_real.gd` that doesn't exist — the TSCN is vestigial. A single-file script is simpler to run: just attach it to any Node in the Godot editor, or instantiate from another scene. The test has no visual elements, so a TSCN adds zero value.

### Decision: Node Lifecycle Management via add_child + await _ready

**Choice**: Components that extend `Node` (`XAPIService`, `ApiClient`, `SyncService`) MUST be added as children of the test node and given a frame to initialize via `await get_tree().process_frame`.

**Alternatives considered**: Calling `_init()` only (skipping `_ready()`), or manually calling setup methods.

**Rationale**: `XAPIService._ready()` creates child nodes (`ApiClient`, `SyncBatchService`) and configures them via `setup()`. `SyncService._ready()` creates `ApiClient` and connects signals. These MUST fire for the components to be functional. The `await get_tree().process_frame` pattern (common in Godot 4 tests) gives the engine one frame to process all `_ready()` calls.

### Decision: Sequential Async Orchestration with Fail-Continue

**Choice**: Each async step returns a `Dictionary` with `{"OK": bool, ...}`, and the orchestrator checks `result.OK` — if false, prints a warning and continues.

**Alternatives considered**: Try/catch via `assert()`, crashing on first failure, full skip-on-failure.

**Rationale**: The proposal explicitly requires resilience: "If no backend, print warning and continue with offline test." The `ApiClient._make_request()` already returns `{"OK": false, "error": "..."}` on failure — this is the existing convention. Each runner function wraps its body in a `print("=== ... ===")` header and returns a result dict, so failures are scoped to a single run.

### Decision: Fresh Context per Run (no shared state)

**Choice**: Each `_run_nivel_*` function creates its own `CafeteriaProblemContext`, `AdaptiveAgent`, and `LevelOneModifier` instances.

**Alternatives considered**: Reusing a single agent across runs (accumulating score history).

**Rationale**: Each run tests independent scenarios (high/low/slow). The `AdaptiveAgent` accumulates scores in `PerformanceAnalyzer.scores` — reusing it would create cross-run contamination. The spec explicitly requires fresh instances per run. `LevelOneModifier` modifies the DB via `LevelRepository`, so reusing it would compound state changes. Fresh instances give clean, deterministic results per run.

### Decision: Explicit Agent Action Assertion via print()

**Choice**: After `analyze_and_decide()`, print the agent's difficulty before/after and the action, then label the run as "PASS" or "FAIL" based on expected outcome.

**Alternatives considered**: Using GUT `assert_eq()` — but the test is manual and extends Node, not GutTest.

**Rationale**: The test is a manual verification tool. The output must be self-documenting. The pattern is: print header → run → print agent decision → print "PASS" or "FAIL" vs expected → print footer. This makes the Godot output panel the test report. A human reading the output can instantly see which runs passed and which failed.

### Decision: XAPIService Instance per Run (not global autoload)

**Choice**: Each level run instantiates a fresh `XAPIService`, adds it as a child, and lets it initialize naturally.

**Alternatives considered**: Using a global `XAPIService` autoload singleton.

**Rationale**: There is no global autoload for `XAPIService` — it's designed as an instantiable class (`class_name XAPIService`). Each run creates its own so xAPI statements are isolated per run. In production, a single `XAPIService` lives on the game scene; here, we simulate "per-level" lifecycle.

### Decision: Sync via XAPIService + SyncService (two paths)

**Choice**: The sync flow exercises BOTH `XAPIService.create_batch()` → `XAPIService._batch_service.process_batch()` AND `SyncService.sync_all_pending()`.

**Alternatives considered**: Syncing only through `XAPIService` (the new path) or only through `SyncService` (the legacy path).

**Rationale**: The system has two parallel tracking paths: the new xAPI pipeline (`XAPIBuilderService` → `XAPIStatementRepository` → `SyncBatchService`) and the legacy path (`SyncService` → `ApiClient.sync_all()`). Both need to work in production. The integration test validates both. The xAPI path tests statement generation and batch creation; the legacy path tests the event queue and sync session lifecycle.

## Data Flow

### Complete Flow (Sequence Diagram)

```
_ready()
  │
  ├── _login()
  │     │
  │     └── ApiClient.login("estudiante1", "", "password123")
  │           │
  │           └── await http_request.request_completed
  │                 │
  │                 ├── [OK] → print token, user_data → continue
  │                 └── [FAIL] → print warning → continue with no token
  │
  ├── _run_nivel_completado_alto()
  │     │
  │     ├── CafeteriaProblemContext.new()
  │     │   student_queue = [estudiante1..3], menu, cash_register, level_goal
  │     │
  │     ├── XAPIService: add_child → await process_frame
  │     │   └── track_level_started("level_1", "Completado Alto", "estudiante1")
  │     │
  │     ├── ExecutionEngine.execute(blocks=[], context)
  │     │
  │     ├── AdaptiveAgent.analyze_and_decide({"score": 0.85, "errors": 2, "time": 90})
  │     │   ├── PerformanceAnalyzer.normalize()
  │     │   ├── RuleBasedInference.decide_action()
  │     │   └── emit "action_decided"("increase", 1.1)
  │     │
  │     ├── print agent decision + PASS/FAIL
  │     │
  │     ├── LevelOneModifier.modify_level("increase", 1.1)
  │     │   └── LevelRepository.update_configuration_segment()
  │     │
  │     ├── XAPIService.track_level_completed("level_1", ..., 0.85, true, "90s")
  │     │
  │     ├── print pending statements count
  │     └── XAPIService.create_batch()
  │
  ├── _run_nivel_fallido_bajo()
  │     └── same structure with score=0.2, errors=15, time=200s
  │           → agent decides "decrease"
  │
  ├── _run_nivel_completado_lento()
  │     └── same structure with score=0.7, errors=3, time=300s
  │           → agent decides "keep"
  │
  ├── _sync_flow()
  │     │
  │     ├── XAPIService._batch_service.process_batch(batch_id)
  │     │   └── await _send_to_backend() (uses JWT from login)
  │     │
  │     ├── SyncService.sync_all_pending(instance_id)
  │     │   └── ApiClient.sync_all() → start_session → register_events → end_session
  │     │
  │     └── print sync results
  │
  └── print final summary
```

### Agent Adaptation Flow (Detail)

```
Context config → ExecutionEngine.execute(blocks, context)
    ↓
result_context returned (modified by blocks)
    ↓
AdaptiveAgent.analyze_and_decide({"score", "errors", "time"})
    ├── analyzer.normalize(raw) → processed_data (score, errors, avg_score, time)
    ├── inference_engine.decide_action(processed_data) → "increase"|"decrease"|"keep"
    └── _apply_action(action)
          └── difficulty +=|-=|0 delta (clamped to [min, max])
          └── emit "action_decided"(action, new_difficulty)
    ↓
LevelOneModifier.modify_level(action, difficulty)
    └── match action → _apply_easy_changes|_apply_hard_changes|_apply_maintain_changes
          └── repo.update_configuration_segment(1, self.segment_id, new_config)
    ↓
XAPIService.track_level_started / track_level_completed
    └── _builder.on_level_*(...) → XAPIStatementRepository.save()
    ↓
XAPIService.create_batch()
    └── _batch_service.create_batch()
          └── _xapi_repository.get_unbatched(BATCH_SIZE)
          └── _batch_repository.create({statements, payload})
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `apps/game/test/integrations/test_full_integration.gd` | Create | Full integration test script |

No existing files are modified. The test is a new addition.

## Interfaces / Contracts

### Test Script Structure

```gdscript
# test/integrations/test_full_integration.gd
extends Node

func _ready() -> void
func _login() -> Dictionary                    # returns {"OK": bool, "token": String, ...}
func _run_nivel_completado_alto(has_token: bool) -> Dictionary
func _run_nivel_fallido_bajo(has_token: bool) -> Dictionary
func _run_nivel_completado_lento(has_token: bool) -> Dictionary
func _run_single_level(label: String, score: float, errors: int, time: float, success: bool, expected_action: String, has_token: bool) -> Dictionary
func _sync_flow(xapi: XAPIService, sync: SyncService, has_token: bool) -> Dictionary
```

### Async Orchestration Pattern

Each run function follows the same pattern:

```gdscript
func _run_single_level(
    label: String,
    score: float,
    errors: int,
    time: float,
    success: bool,
    expected_action: String,
    has_token: bool
) -> Dictionary:
    print("\n=== %s ===" % label)
    print("Score: %.2f, Errors: %d, Time: %.0fs, Success: %s" % [score, errors, time, str(success)])
    print("Expected action: %s" % expected_action)

    # 1. Create context
    var context := CafeteriaProblemContext.new()
    context.student_queue = [
        {"nombre": "Ana", "pedido": "cafe"},
        {"nombre": "Luis", "pedido": "te"},
        {"nombre": "Maria", "pedido": "pan"}
    ]
    context.menu = {"cafe": 5, "te": 3, "pan": 2}
    context.cash_register = 0
    context.level_goal = {"all_served": true}
    print("Context created with %d students" % context.student_queue.size())

    # 2. Create XAPIService
    var xapi := XAPIService.new()
    add_child(xapi)
    await get_tree().process_frame  # Let _ready() fire

    if has_token:
        xapi.track_level_started("level_1", label, "estudiante1")

    # 3. Execute blocks (empty blocks — testing pipeline, not block logic)
    var blocks: Array = []
    var start_block := StartBlock.new()
    var end_block := EndBlock.new()
    blocks.append(start_block)
    blocks.append(end_block)

    var result_context := ExecutionEngine.execute(blocks, context)
    print("Execution result: %s" % ("OK" if result_context != null else "NULL"))

    # 4. Agent analysis
    var agent := AdaptiveAgent.new()
    var initial_difficulty := agent.difficulty
    agent.analyze_and_decide({"score": score, "errors": errors, "time": time})
    var action := ""
    var new_difficulty := agent.difficulty

    # Connect signal to capture the action
    var signal_action := ""
    var signal_received := false
    var callback := func(a: String, d: float):
        signal_action = a
        signal_received = true
    agent.action_decided.connect(callback)
    # Signal was already emitted during analyze_and_decide,
    # but we can check agent.difficulty directly instead

    if agent.difficulty > initial_difficulty:
        action = "increase"
    elif agent.difficulty < initial_difficulty:
        action = "decrease"
    else:
        action = "keep"

    print("Agent: initial=%.1f, final=%.1f, action=%s" % [initial_difficulty, agent.difficulty, action])
    print("Expected: %s" % expected_action)

    if action == expected_action:
        print(">>> PASS: Action matches expected <<<")
    else:
        print(">>> FAIL: Expected %s but got %s <<<" % [expected_action, action])

    # 5. Level modifier
    var modifier := LevelOneModifier.new()
    modifier.modify_level(action, agent.difficulty)
    print("Level modifier applied")

    # 6. xAPI tracking
    if has_token:
        var duration_str := "%ds" % time
        xapi.track_level_completed("level_1", label, "estudiante1", score, score, success, duration_str)
        var pending := xapi._builder.get_pending_statements().size()
        print("Pending xAPI statements: %d" % pending)
        var batch_id := xapi.create_batch()
        print("Batch created: %s" % batch_id)

    # 7. Cleanup child nodes to avoid leaking
    remove_child(xapi)
    xapi.queue_free()

    var test_passed := (action == expected_action)
    print("--- End %s: %s ---" % [label, "PASS" if test_passed else "FAIL"])

    return {
        "OK": true,
        "label": label,
        "action": action,
        "initial_difficulty": initial_difficulty,
        "final_difficulty": agent.difficulty,
        "test_passed": test_passed
    }
```

### Login Function Contract

```gdscript
func _login() -> Dictionary:
    print("\n=== Login ===")
    var api := ApiClient.new()
    add_child(api)
    await get_tree().process_frame

    var result := await api.login("estudiante1", "", "password123")

    if result.OK:
        var token := api.jwt_token
        var truncated := token.substr(0, 20) + "..."
        print("Token: %s" % truncated)
        print("User: %s" % str(api.current_user))
        remove_child(api)
        api.queue_free()
        return {"OK": true, "token": token, "user_data": api.current_user, "api_client": api}
    else:
        print("WARNING: Backend offline - %s" % result.get("error", "unknown"))
        print("Continuing with offline test...")
        remove_child(api)
        api.queue_free()
        return {"OK": false}
```

### Sync Function Contract

```gdscript
func _sync_flow(xapi_instance: XAPIService, has_token: bool) -> Dictionary:
    print("\n=== Sync Flow ===")
    if not has_token:
        print("SKIP: No JWT token (backend was offline)")
        return {"OK": false, "reason": "no_token"}

    var results := {}

    # Path 1: xAPI batch sync
    var batch_result := await xapi_instance._batch_service.process_batch("pending")
    results["xapi_batch"] = batch_result
    print("xAPI batch sync: %s" % str(batch_result))

    # Path 2: Legacy event sync
    var sync_service := SyncService.new()
    add_child(sync_service)
    await get_tree().process_frame

    sync_service.sync_all_pending("integration-test-instance")
    print("Legacy sync triggered")

    remove_child(sync_service)
    sync_service.queue_free()

    print("Sync results: %s" % str(results))
    print("--- Sync complete ---")
    return {"OK": true, "results": results}
```

## Error Handling Strategy

| Failure Point | Behavior | Output |
|---|---|---|
| Backend offline at login | Login returns `{"OK": false}`, test skips sync, continues with level runs | `WARNING: Backend offline` |
| ExecutionEngine returns null | Each run checks `result_context != null` | `Execution result: NULL` (non-fatal) |
| AdaptiveAgent signal not received | Level run inspects `agent.difficulty` directly as fallback | `Agent action: fallback` |
| LevelOneModifier DB not available | `repo.update_configuration_segment()` may fail silently | `Level modifier applied` (no crash) |
| XAPIService batch creation fails | `create_batch()` returns empty string | `Batch created: ` (empty) |
| Sync fails | Sync functions return `{"OK": false}` | `SKIP: No JWT token` or `FAIL` |
| Any await times out | Godot 4 `await` has no timeout by default — if the signal never fires, the coroutine pauses indefinitely | N/A (won't block — HTTP requests always complete) |

## Dependencies

| Component | Instantiation | Node Lifecycle | Async |
|---|---|---|---|
| `CafeteriaProblemContext` | `CafeteriaProblemContext.new()` | None (no `extends Node`) | None |
| `ExecutionEngine` | `ExecutionEngine.execute()` (static) | None | None |
| `AdaptiveAgent` | `AdaptiveAgent.new()` | None (no `extends Node`) | None |
| `LevelOneModifier` | `LevelOneModifier.new()` | None | None |
| `XAPIService` | `XAPIService.new()` + `add_child()` | Requires `_ready()` to fire | `create_batch()` sync |
| `ApiClient` | `ApiClient.new()` + `add_child()` | Requires `_ready()` to fire | `await login()` |
| `SyncService` | `SyncService.new()` + `add_child()` | Requires `_ready()` to fire | `sync_all_pending()` |
| `SyncBatchService` | Created by `XAPIService._init()` as non-child | `_ready()` fires via parent | `process_batch()` async |

## Async Orchestration Pattern

```
_ready() ──→ _login() ──await──→ result
               │                    │
               │          ┌─────────┘
               │          ↓
               │     has_token? ──yes──→ _run_nivel_*(has_token=true)
               │          │                │
               │          no               │ await each step
               │          ↓                ↓
               │     _run_nivel_*(false)  _run_nivel_alto()
               │          │                ↓
               │          │           _run_fallido_bajo()
               │          │                ↓
               │          │           _run_lento()
               │          │                ↓
               │          └────────── _sync_flow()
               │                            ↓
               └─────────────────── print summary
```

All `await` calls are at the top level of `_ready()` or within `_run_*` functions. Godot 4's `await` returns the value from the signal/function — no callbacks needed.

Each `await` is on a separate line with the result captured:

```gdscript
var login_result := await _login()
var alto_result := await _run_nivel_completado_alto(login_result.OK)
```

There are NO concurrent awaits — the flow is strictly sequential. This keeps the orchestration simple and deterministic.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Integration | Full pipeline: context → engine → agent → modifier → xAPI → sync | Manual test run via Godot editor (attach script to Node, run scene, inspect `print()` output) |
| Integration | Offline resilience: no backend | Disconnect backend, run test, verify graceful degradation |
| Integration | Agent decision correctness | Verify each run produces expected action: increase (0.85), decrease (0.2), keep (0.7) |

This is a manual test — no automated test runner integration. All validation is visual via the Godot output panel.

## Migration / Rollout

No migration required. The test file is added to `test/integrations/` and can be run immediately in any Godot 4 session. Rollback: delete the file.

## Open Questions

- None — the design is fully resolved from the proposal and spec.
