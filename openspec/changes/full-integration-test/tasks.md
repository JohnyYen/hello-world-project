# Tasks: Full Integration Test for Godot Game Flow

## Phase 1: Infrastructure / Foundation

- [ ] 1.1 Create directory structure `apps/game/test/integrations/` if it doesn't exist
- [ ] 1.2 Create `apps/game/test/integrations/test_full_integration.gd` file
- [ ] 1.3 Define `extends Node` and `_ready()` as main entry point
- [ ] 1.4 Import all required classes (CafeteriaProblemContext, ExecutionEngine, AdaptiveAgent, LevelOneModifier, XAPIService, ApiClient, SyncService, SyncBatchService, PerformanceAnalyzer, RuleBasedInference)
- [ ] 1.5 Declare global variables for services (xapi_service, sync_service, api_client, token, user_data)
- [ ] 1.6 Define helper variables (test_instance_id, batch_id)

## Phase 2: Helper Functions

- [ ] 2.1 Create `_format_duration(total_seconds: float) -> String` for ISO 8601 formatting
- [ ] 2.2 Create `_determine_agent_action(avg_score: float) -> String` helper
- [ ] 2.3 Create `_print_section(title: String)` helper for consistent section headers
- [ ] 2.4 Implement `_determine_agent_action()` to return "increase" (score > 0.7), "decrease" (score <= 0.5), "keep" (otherwise)

## Phase 3: Level Run Functions

- [ ] 3.1 Create `_run_level_complete_high_performance()` function
  - 3.1.1 Call `_print_section("=== RUN: Nivel Completado - Alto Rendimiento ===")`
  - 3.1.2 Create CafeteriaProblemContext with 3 students (Ana, Luis, Maria), menu items (cafe=5, te=3, pan=2), cash_register=0, level_goal={"all_served": true}
  - 3.1.3 Call ExecutionEngine.execute() with minimal blocks (StartBlock + EndBlock only)
  - 3.1.4 Call AdaptiveAgent.analyze_and_decide({"score": 0.85, "errors": 2, "time": 90.0})
  - 3.1.5 Print agent action and new difficulty level
  - 3.1.6 Verify agent action is "increase" (expected behavior)
  - 3.1.7 Call LevelOneModifier.modify_level("increase", 1.1)
  - 3.1.8 Call XAPIService.track_level_started("level_1", "Nivel Completado - Alto Rendimiento", "estudiante1")
  - 3.1.9 Call XAPIService.track_level_completed("level_1", ..., 0.85, 0.85, true, "90s")
  - 3.1.10 Print pending statements count via `xapi._builder.get_pending_statements().size()`
  - 3.1.11 Call XAPIService.create_batch() and store batch_id
  - 3.1.12 Print ">>> PASS: Action matches expected (increase) <<<" or failure message

- [ ] 3.2 Create `_run_level_fail_low_performance()` function
  - 3.2.1 Call `_print_section("=== RUN: Nivel Fallido - Bajo Rendimiento ===")`
  - 3.2.2 Create fresh CafeteriaProblemContext (independent instance)
  - 3.2.3 Execute with ExecutionEngine (empty blocks)
  - 3.2.4 Call AdaptiveAgent.analyze_and_decide({"score": 0.20, "errors": 15, "time": 200.0})
  - 3.2.5 Print agent action and new difficulty
  - 3.2.6 Verify agent action is "decrease" (expected behavior)
  - 3.2.7 Apply modification via LevelOneModifier.modify_level("decrease", 0.9)
  - 3.2.8 Track xAPI events with score=0.20, success=false
  - 3.2.9 Print pending statements count and create batch
  - 3.2.10 Print ">>> PASS: Action matches expected (decrease) <<<" or failure message

- [ ] 3.3 Create `_run_level_complete_slow()` function
  - 3.3.1 Call `_print_section("=== RUN: Nivel Completado - Lento ===")`
  - 3.3.2 Create fresh CafeteriaProblemContext (independent instance)
  - 3.3.3 Execute with ExecutionEngine (empty blocks)
  - 3.3.4 Call AdaptiveAgent.analyze_and_decide({"score": 0.70, "errors": 3, "time": 300.0})
  - 3.3.5 Print agent action and new difficulty
  - 3.3.6 Verify agent action is "keep" (expected behavior)
  - 3.3.7 Apply modification via LevelOneModifier.modify_level("keep", 1.0)
  - 3.3.8 Track xAPI events with score=0.70, success=true, time=300s
  - 3.3.9 Print pending statements count and create batch
  - 3.3.10 Print ">>> PASS: Action matches expected (keep) <<<" or failure message

## Phase 4: Login Function

- [ ] 4.1 Create `_login_to_backend()` async function
  - 4.1.1 Call `_print_section("=== LOGIN ===")`
  - 4.1.2 Instantiate ApiClient and add as child node
  - 4.1.3 Await get_tree().process_frame to let `_ready()` fire
  - 4.1.4 Call `SyncService.api_client.login("estudiante1", "", "password123")` and await result
  - 4.1.5 If result.OK:
    - 4.1.5a Store token and user_data in global variables
    - 4.1.5b Print truncated JWT token (first 20 chars + "...")
    - 4.1.5c Print user_data dictionary
  - 4.1.6 If result.OK is false:
    - 4.1.6a Print warning "WARNING: Backend offline - {error}"
    - 4.1.6b Print "Continuing with offline test..."
  - 4.1.7 Queue free ApiClient child node
  - 4.1.8 Return dictionary {"OK": bool, "token": String, "user_data": Dictionary}

## Phase 5: Sync Function

- [ ] 5.1 Create `_sync_to_backend()` async function
  - 5.1.1 Call `_print_section("=== SYNC ===")`
  - 5.1.2 If no token stored:
    - 5.1.2a Print "SKIP: No JWT token (backend was offline)"
    - 5.1.2b Return {"OK": false, "reason": "no_token"}
  - 5.1.3 Instantiate XAPIService, add as child node
  - 5.1.4 Await get_tree().process_frame
  - 5.1.5 Call `XAPIService._batch_service.process_batch("pending")` and await result
  - 5.1.6 Print xAPI batch sync result
  - 5.1.7 Instantiate SyncService, add as child node
  - 5.1.8 Await get_tree().process_frame
  - 5.1.9 Call `SyncService.sync_all_pending(test_instance_id)` to trigger legacy event sync
  - 5.1.10 Print legacy sync trigger confirmation
  - 5.1.11 Queue free both SyncService and XAPIService child nodes
  - 5.1.12 Print "--- Sync complete ---" footer

## Phase 6: Main Orchestration

- [ ] 6.1 Implement `_ready()` as main entry point
  - 6.1.1 Print "=== FULL INTEGRATION TEST ===" header with timestamp
  - 6.1.2 Initialize test_instance_id = "integration-test-" + str(Time.get_ticks_msec())
  - 6.1.3 Call `_login_to_backend()` and await result
  - 6.1.4 Print "Token obtained: %s" % str(result.get("token", "none") if result.OK else "none")
  - 6.1.5 Print "User data: %s" % str(result.get("user_data", {}) if result.OK else "none")
  - 6.1.6 Call `_run_level_complete_high_performance()` and await result
  - 6.1.7 Call `_run_level_fail_low_performance()` and await result
  - 6.1.8 Call `_run_level_complete_slow()` and await result
  - 6.1.9 Instantiate XAPIService for sync, add as child, await _ready()
  - 6.1.10 Instantiate SyncService for sync, add as child, await _ready()
  - 6.1.11 Call `_sync_to_backend()` and await result
  - 6.1.12 Print final summary with stats from XAPIService.get_stats()

## Phase 7: Testing / Verification

- [ ] 7.1 Verify backend is running at localhost:8010 before test run
- [ ] 7.2 Run test in Godot 4 editor (attach script to Node, press F5)
- [ ] 7.3 Verify all three level scenarios produce correct difficulty decisions
  - 7.3a "Nivel Completado - Alto Rendimiento" should show agent action "increase"
  - 7.3b "Nivel Fallido - Bajo Rendimiento" should show agent action "decrease"
  - 7.3c "Nivel Completado - Lento" should show agent action "keep"
- [ ] 7.4 Verify login returns valid JWT token and user_data when backend is online
- [ ] 7.5 Verify login prints warning and continues when backend is offline
- [ ] 7.6 Verify sync flow completes without crashes (may fail gracefully if no backend)
- [ ] 7.7 Verify all output uses print() with clear section headers
- [ ] 7.8 Verify no state leakage between runs (fresh context/agent/agent per run)
- [ ] 7.9 Verify no Node child nodes leak (queue_free all XAPIService, SyncService, ApiClient instances)

## Phase 8: Cleanup / Documentation

- [ ] 8.1 Document manual test procedure in `apps/game/test/integrations/README.md`
  - 8.1a Describe prerequisites (backend running, Godot 4.x)
  - 8.1b Describe execution steps (attach script, press F5, inspect output)
  - 8.1c Describe expected output format
- [ ] 8.2 Add inline comments for complex sections (agent decision logic, node lifecycle management)
- [ ] 8.3 Verify no hardcoded secrets in test file
- [ ] 8.4 Remove test file if rollback is required (delete `apps/game/test/integrations/test_full_integration.gd`)
