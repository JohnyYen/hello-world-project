# Proposal: Full Integration Test for Godot Game Flow

## Intent

Currently the game has unit tests for individual components (engine, agent, contexts) but lacks an end-to-end integration test that validates the complete game flow: level execution → adaptive agent analysis → difficulty modification → xAPI tracking → backend sync. Without this, regressions in component interactions go undetected, and there's no way to manually verify the entire pipeline before releases.

This proposal creates a manual integration test script (not GUT) that exercises the full system with `print()`-based output, covering three performance scenarios (high, low, slow) plus login + sync.

## Scope

### In Scope
- `apps/game/test/integrations/test_full_integration.gd` — main test script
- Three level run functions covering all adaptive agent outcomes (increase, decrease, keep)
- Login function against backend at localhost:8010
- Sync flow using JWT from login
- Follows `simple_test.gd` pattern: `extends Node`, `func _ready()`, `print()` output
- All existing components used via `class_name` instantiation

### Out of Scope
- GUT assertions or test runner integration (manual test only)
- UI/Scene testing — pure logic
- Backend mocking — requires live backend at localhost:8010
- Error recovery beyond what components already handle
- Automated CI pipeline integration
- Godot 3 yield-based patterns (uses Godot 4 await)

## Approach

The test is structured as a single GDScript file with:

1. **`_ready()`** → Entry point that orchestrates the flow:
   - Login first (async via await)
   - Run 3 level scenarios in sequence
   - Sync xAPI batches to backend
   - Sync legacy events
   - Print summary

2. **`_run_nivel_completado_alto()`** → Score=0.85, errors=2, time=90s
   - Creates CafeteriaProblemContext with 3 students, menu items, cash_register, level_goal
   - Executes with ExecutionEngine (empty blocks since we test the adaptation, not block logic)
   - Feeds results to AdaptiveAgent → analyze_and_decide
   - Uses LevelOneModifier to apply changes via repo
   - Tracks via XAPIService (track_level_started, track_level_completed)
   - Creates xAPI batch

3. **`_run_nivel_fallido_bajo()`** → Score=0.2, errors=15, time=200s
   - Same structure, different performance metrics
   - Expects difficulty decrease

4. **`_run_nivel_completado_lento()`** → Score=0.7, errors=3, time=300s
   - Same structure, different performance metrics
   - Expects difficulty maintained

5. **`_login()`** → Authenticates with estudiante1/password123 to localhost:8010
   - Uses ApiClient directly
   - Prints JWT token and user_data

6. **`_sync_flow()`** → Syncs xAPI batches and legacy events
   - Uses XAPIService to create_batch and sync_now
   - Uses SyncService for legacy event sync

Components are instantiated as needed (not reusing state between runs unless noted).

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `apps/game/test/integrations/test_full_integration.gd` | New | Full integration test script |
| `apps/game/scripts/agent/adaptive_agent.gd` | None | Consumed as-is |
| `apps/game/scripts/agent/analizer/performance_analizer.gd` | None | Consumed as-is |
| `apps/game/scripts/agent/inference/rule_inference.gd` | None | Consumed as-is |
| `apps/game/scripts/agent/level_modifier/level_one_modifier.gd` | None | Consumed as-is |
| `apps/game/scripts/engine/execution_engine.gd` | None | Consumed as-is |
| `apps/game/scripts/engine/problems_context/cafeteria_problem_context.gd` | None | Consumed as-is |
| `apps/game/scripts/xapi/xapi_service.gd` | None | Consumed as-is |
| `apps/game/scripts/controllers/service/sync_service.gd` | None | Consumed as-is |
| `apps/game/scripts/http/api_client.gd` | None | Consumed as-is |
| `apps/game/scripts/xapi/verbs.gd` | None | Consumed as-is |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Backend not running at localhost:8010 | Medium | Test prints clear error if login fails; sync gracefully handles connection errors |
| LevelOneModifier requires DB + LevelRepository | High | Requires running game scene with SQLite initialized; modifier calls may fail silently in test |
| Async timing (await) in _ready may behave unexpectedly | Low | Follows same pattern as existing Godot 4 Node scripts in project |
| Components reference autoloads (Env) not available in headless test | Medium | May need to set Env.API_BASE_URL manually or handle missing autoload gracefully |

## Rollback Plan

This is a new file addition with no changes to existing code. Rollback is simple: delete `apps/game/test/integrations/test_full_integration.gd`.

## Dependencies

- Backend server running at `http://localhost:8010` with user `estudiante1` / `password123` seeded
- Godot 4.x engine to run the test script
- Existing components fully implemented and autoloaded (Env autoload)

## Success Criteria

- [ ] Test script runs without errors in Godot 4 (manual run via editor or command line)
- [ ] Three level scenarios produce correct difficulty decisions: increase, decrease, keep
- [ ] Login returns valid JWT token and user_data
- [ ] Sync flow completes without crashes (may fail gracefully if no backend is running)
- [ ] All output uses `print()` with clear section headers for manual verification
