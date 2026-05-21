# Game Integration Test Specification

## Purpose

This specification defines the manual integration test for the Godot game pipeline: level execution → adaptive agent analysis → difficulty modification → xAPI tracking → backend sync. The test validates that all game components work together correctly across three performance scenarios plus authentication and data synchronization.

## Requirements

### Requirement: Test Entry Point

The test SHALL have a `_ready()` method as its single entry point that orchestrates the full integration flow.

The flow MUST execute in this order:
1. Login against backend
2. Run Nivel Completado (alto rendimiento)
3. Run Nivel Fallido (bajo rendimiento)
4. Run Nivel Completado (mucho tiempo)
5. Sync xAPI batches
6. Sync legacy events
7. Print final summary

#### Scenario: Full integration flow executes in sequence

- GIVEN the test script is attached to a Node in a running Godot scene
- WHEN `_ready()` is called
- THEN each step SHALL execute in the specified order
- AND each step SHALL wait for the previous step to complete via `await`
- AND a final summary SHALL be printed via `print()`

#### Scenario: Error in one step does not abort the entire test

- GIVEN the test is running
- WHEN login fails (backend offline)
- THEN the test SHALL print a warning
- AND the test SHALL continue with level runs
- AND the test SHALL attempt sync regardless

### Requirement: Login Authentication

The test SHALL authenticate against the backend API at `http://localhost:8010` using credentials `estudiante1` / `password123`.

The login function MUST:
- Send credentials via HTTP POST to the backend login endpoint
- Receive and print the JWT token
- Receive and print the `user_data` from the response
- Store the JWT token for later use in sync

#### Scenario: Backend is online and credentials are valid

- GIVEN the backend server is running at localhost:8010
- AND the user `estudiante1` with password `password123` exists
- WHEN the login function sends authentication request
- THEN a JWT token SHALL be returned
- AND `user_data` SHALL contain the user profile
- AND the token SHALL be available for sync flow

#### Scenario: Backend is offline

- GIVEN the backend server is NOT running at localhost:8010
- WHEN the login function sends authentication request
- THEN a warning message SHALL be printed indicating the backend is offline
- AND the test SHALL continue with level runs
- AND sync flow SHALL be skipped gracefully

### Requirement: Level Run — Alto Rendimiento (Difficulty Increases)

The test SHALL simulate a high-performance level completion and SHALL verify that the adaptive agent increases difficulty.

Input data:
- Score: `0.85`
- Errors: `2`
- Time: `90` seconds
- Success: `true`
- Expected agent decision: `increase`

For this run, the test MUST:
1. Create a `CafeteriaProblemContext` with students, menu items, cash register, and level goal
2. Execute blocks via `ExecutionEngine.execute(blocks, context)`
3. Feed results to `AdaptiveAgent.analyze_and_decide()`
4. Print the agent action and new difficulty value
5. Apply the modification via `LevelOneModifier`
6. Track via `XAPIService.track_level_started` and `XAPIService.track_level_completed`
7. Print pending xAPI statements count
8. Create an xAPI batch

#### Scenario: High performance triggers difficulty increase

- GIVEN a CafeteriaProblemContext is created with valid configuration
- WHEN the agent analyzes score=0.85, errors=2, time=90s, success=true
- THEN the agent action SHALL be `increase`
- AND the new difficulty SHALL be higher than the current
- AND the difficulty modification SHALL be applied via LevelOneModifier

#### Scenario: xAPI events are tracked for completed level

- GIVEN a level run with score=0.85
- WHEN track_level_started and track_level_completed are called
- THEN pending statements count SHALL be greater than zero
- AND a batch SHALL be created for sync

### Requirement: Level Run — Bajo Rendimiento (Difficulty Decreases)

The test SHALL simulate a failed level with very low performance and SHALL verify that the adaptive agent decreases difficulty.

Input data:
- Score: `0.20`
- Errors: `15`
- Time: `200` seconds
- Success: `false`
- Expected agent decision: `decrease`

The test MUST follow the same structure as the high-performance run but with these different input values.

#### Scenario: Low performance triggers difficulty decrease

- GIVEN a CafeteriaProblemContext is created with valid configuration
- WHEN the agent analyzes score=0.2, errors=15, time=200s, success=false
- THEN the agent action SHALL be `decrease`
- AND the new difficulty SHALL be lower than the current

### Requirement: Level Run — Mucho Tiempo (Difficulty Maintained)

The test SHALL simulate a slow but successful level completion and SHALL verify that the adaptive agent maintains the current difficulty.

Input data:
- Score: `0.70`
- Errors: `3`
- Time: `300` seconds
- Success: `true`
- Expected agent decision: `keep`

The test MUST follow the same structure as the previous runs but with these different input values.

#### Scenario: Slow but successful completion maintains difficulty

- GIVEN a CafeteriaProblemContext is created with valid configuration
- WHEN the agent analyzes score=0.7, errors=3, time=300s, success=true
- THEN the agent action SHALL be `keep`
- AND the difficulty SHALL remain unchanged

#### Scenario: xAPI events are tracked for slow completion

- GIVEN a level run with score=0.7, time=300s
- WHEN track_level_started and track_level_completed are called
- THEN pending statements count SHALL be printed

### Requirement: Difficulty Modification via LevelOneModifier

Each level run SHALL apply the adaptive agent's decision to the game state through `LevelOneModifier`.

The modifier MUST:
- Receive the agent's decision (increase, decrease, or keep)
- Apply the corresponding configuration changes
- Print confirmation of the modification

#### Scenario: LevelOneModifier applies difficulty change

- GIVEN a valid adaptive agent decision (increase, decrease, or keep)
- WHEN LevelOneModifier.apply() is called with the decision
- THEN the difficulty configuration SHALL be updated accordingly

### Requirement: CafeteriaProblemContext Creation

Each level run SHALL create a fresh `CafeteriaProblemContext` instance with:
- Students (at least 3)
- Menu items with prices
- Cash register configuration
- Level goal definition

The test MUST reuse the existing `CafeteriaProblemContext` class without modification.

#### Scenario: Context is configured per run

- GIVEN a new level run is starting
- WHEN a CafeteriaProblemContext is instantiated
- THEN it SHALL contain students, menu, cash_register, and level_goal
- AND each run SHALL use its own context instance (no state leaking between runs)

### Requirement: xAPI Tracking and Batch Creation

Each level run MUST track progression events via `XAPIService`:
- `track_level_started()` — called when the level run begins
- `track_level_completed()` — called after the agent decision is made

After each run, the test MUST:
- Print the count of pending statements
- Call `create_batch()` to prepare statements for sync

#### Scenario: xAPI events track level lifecycle

- GIVEN a level run is in progress
- WHEN track_level_started is called
- THEN a started event SHALL be recorded in pending statements
- WHEN track_level_completed is called
- THEN a completed event SHALL be recorded in pending statements
- AND create_batch SHALL prepare the statements for sync

### Requirement: Data Synchronization

After all three level runs are complete, the test SHALL synchronize xAPI data with the backend.

The sync flow MUST:
1. Use the JWT token obtained from login
2. Sync xAPI batches via XAPIService
3. Sync legacy events via SyncService
4. Print sync results (success or failure reason)

#### Scenario: Backend available — sync succeeds

- GIVEN a valid JWT token from login
- AND xAPI batches exist from level runs
- WHEN sync_flow executes
- THEN xAPI batches SHALL be synced via XAPIService
- AND legacy events SHALL be synced via SyncService
- AND sync results SHALL be printed

#### Scenario: Backend unavailable — sync fails gracefully

- GIVEN the backend is offline
- WHEN sync_flow executes
- THEN sync SHALL fail with a printed error message
- AND the test SHALL NOT crash

### Requirement: Test Output Format

All test output MUST use `print()` statements with clear section headers for manual verification.

Each section MUST include:
- A header line indicating the section name (e.g., `=== Login ===`)
- Relevant data values (scores, tokens, decisions, etc.)
- A footer or separator line

#### Scenario: Output is readable and self-documenting

- GIVEN the test is running
- WHEN any section executes
- THEN the output SHALL be prefixed with a descriptive header
- AND data values SHALL be printed for manual verification

## Coverage

- Happy paths: covered — all three performance scenarios, login success, sync success
- Edge cases: covered — backend offline (login and sync), three different agent decisions (increase, decrease, keep)
- Error states: covered — backend offline gracefully handled
