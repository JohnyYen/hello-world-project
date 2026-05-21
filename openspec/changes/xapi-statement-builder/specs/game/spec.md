# Game xAPI Statement Builder Specification

## Purpose

This specification defines the requirements for the xAPI Statement Builder Service implemented in Godot 4.x (GDScript). The system transforms raw game events into valid xAPI statements, stores them locally in SQLite, and synchronizes them with the backend API when connectivity is available while maintaining full offline functionality.

## Requirements

### Requirement: XAPIBuilderService Statement Creation

The system MUST provide an `XAPIBuilderService` that constructs valid xAPI statements from game events. Each statement SHALL contain the verb identifier, object definition, actor reference, optional result data, timestamp, and unique identifier conforming to xAPI 1.0.3 specification.

The builder MUST validate all required fields before persisting a statement and MUST reject malformed statements with descriptive error messages.

#### Scenario: Build completed level statement

- GIVEN the player has finished level "level_1" with a score of 85 and duration of 150 seconds
- WHEN `XAPIBuilderService.build("completed", object_data, result_data)` is invoked
- THEN a valid xAPI statement SHALL be returned with verb `http://adlnet.gov/expapi/verbs/completed`, object type `level`, object id `level_1`, score_raw `85`, score_scaled `0.85`, and duration `PT2M30S`
- AND the statement SHALL be assigned a unique UUID
- AND the statement SHALL include the actor's UUID from the current game session

#### Scenario: Build answered question statement

- GIVEN the player has answered assessment question "q1" correctly
- WHEN `XAPIBuilderService.build("answered", object_data, result_data)` is invoked
- THEN a valid xAPI statement SHALL be returned with verb `http://adlnet.gov/expapi/verbs/answered`, object type `assessment`, and result_success `true`

#### Scenario: Reject statement with missing required field

- GIVEN the game event provides an object without an id
- WHEN `XAPIBuilderService.build("completed", incomplete_object, result_data)` is invoked
- THEN the builder SHALL reject the statement
- AND an error SHALL be logged indicating the missing required field

### Requirement: xapi_statement SQLite Persistence

The system MUST persist all constructed xAPI statements to the `xapi_statement` SQLite table immediately upon creation. The repository SHALL store all statement fields including verb, object, actor, result, timestamp, and batch association.

Each statement MUST be assigned to a batch for synchronization purposes and MUST retain its creation timestamp.

#### Scenario: Persist statement to SQLite

- GIVEN `XAPIBuilderService` has created a valid statement
- WHEN the statement is passed to `XAPIStatementRepository.create(statement)`
- THEN the statement SHALL be inserted into the `xapi_statement` table
- AND a batch_id SHALL be assigned if not already present
- AND `created_at` SHALL be set to the current timestamp

#### Scenario: Retrieve statements by batch

- GIVEN there are 10 statements assigned to batch_id "batch-uuid-123"
- WHEN `XAPIStatementRepository.get_by_batch("batch-uuid-123")` is invoked
- THEN exactly 10 statements SHALL be returned

### Requirement: pending_batch Queue Management

The system MUST maintain a queue of pending batches in the `pending_batch` SQLite table. Each batch SHALL track its statements, status (pending/sending/failed), retry count, last error, and timestamps.

The system SHOULD process pending batches in FIFO order and SHALL NOT process batches marked as failed unless explicitly requested.

#### Scenario: Create pending batch

- GIVEN there are 5 statements ready for synchronization
- WHEN `PendingBatchRepository.create_batch(statement_ids)` is invoked
- THEN a new batch SHALL be created with status `pending`, retry_count `0`
- AND the batch payload SHALL contain the formatted statements

#### Scenario: Mark batch as sending

- GIVEN a batch exists with status `pending`
- WHEN `PendingBatchRepository.mark_sending(batch_id)` is invoked
- THEN the batch status SHALL be updated to `sending`
- AND `last_attempt_at` SHALL be updated to current timestamp

#### Scenario: Mark batch as failed after max retries

- GIVEN a batch has retry_count of 5 and the last attempt failed with error "Connection timeout"
- WHEN `PendingBatchRepository.mark_failed(batch_id, error)` is invoked
- THEN the batch status SHALL be updated to `failed`
- AND `last_error` SHALL contain the provided error message
- AND no further automatic retries SHALL be attempted

### Requirement: SyncBatchService Batch Transmission

The system MUST provide a `SyncBatchService` that transmits batches to the backend API. The service SHALL format each statement according to the sync API schema and SHALL send batches via the existing `ApiClient`.

The service SHOULD implement exponential backoff for failed transmissions with initial delay of 1 second, doubling on each retry, up to a maximum of 5 retries per batch.

#### Scenario: Successfully sync batch to backend

- GIVEN a batch with 3 statements exists with status `pending`
- WHEN `SyncBatchService.process_batch(batch_id)` is invoked
- AND the backend API is reachable
- THEN each statement SHALL be sent to `POST /api/v1/sync/sync-events`
- AND the batch SHALL be marked as completed after successful transmission
- AND statements belonging to the batch SHOULD be removed from local storage after confirmation

#### Scenario: Retry batch after transient failure

- GIVEN a batch fails to sync due to "Network timeout"
- WHEN `SyncBatchService.process_batch(batch_id)` is invoked
- THEN the retry_count SHALL be incremented
- AND the batch SHALL be rescheduled with exponential backoff (1s, 2s, 4s, 8s, 16s)
- AND the batch status SHALL remain `pending`

#### Scenario: Stop retry after max attempts

- GIVEN a batch has retry_count of 5 and fails again
- WHEN `SyncBatchService.process_batch(batch_id)` is invoked
- THEN the batch SHALL be marked as `failed`
- AND the last_error SHALL contain the failure reason
- AND the system SHALL NOT attempt further automatic retries

### Requirement: ConnectionDetector Connectivity Monitoring

The system MUST provide a `ConnectionDetector` that monitors network connectivity and emits signals when connectivity state changes. The detector SHOULD check connectivity periodically when idle and SHALL immediately check connectivity before initiating batch synchronization.

The detector MUST emit `connection_changed(online: bool)` signal when connectivity state transitions.

#### Scenario: Detect connectivity restored

- GIVEN the device was offline
- WHEN the device regains network connectivity
- THEN `ConnectionDetector` SHALL detect the change within 5 seconds
- AND the `connection_changed(true)` signal SHALL be emitted
- AND pending batches SHOULD be queued for synchronization

#### Scenario: Detect connectivity lost

- GIVEN the device was online
- WHEN network connectivity is lost
- THEN `ConnectionDetector` SHALL detect the change within 5 seconds
- AND the `connection_changed(false)` signal SHALL be emitted
- AND in-progress batch transmissions SHOULD be gracefully paused

#### Scenario: Periodic connectivity check when idle

- GIVEN no user activity has occurred for 30 seconds
- WHEN `ConnectionDetector` is in idle state
- THEN periodic connectivity checks SHALL be performed every 30 seconds
- AND signal SHALL only emit on state change, not on every check

### Requirement: Offline Operation Mode

The system MUST function completely offline without any network connectivity. All statement creation, SQLite persistence, and batch queue management SHALL work without internet access.

The system SHOULD automatically synchronize pending batches when connectivity is restored.

#### Scenario: Create statements while offline

- GIVEN the device has no network connectivity
- WHEN `XAPIBuilderService.build("completed", object_data, result_data)` is invoked
- THEN the statement SHALL be created and persisted to SQLite
- AND the batch SHALL be marked as `pending`
- AND no error SHALL be raised regarding network availability

#### Scenario: Automatic sync when connectivity restored

- GIVEN there are 3 pending batches in the queue
- AND the device regains network connectivity
- WHEN `ConnectionDetector` emits `connection_changed(true)`
- THEN `SyncBatchService` SHALL automatically begin processing pending batches
- AND batches SHALL be processed in order of creation (FIFO)

### Requirement: Statement Batching Strategy

The system SHOULD batch statements for transmission to reduce API overhead. Each batch SHOULD contain up to 50 statements. The system MAY create smaller batches if fewer than 50 statements are pending.

The batch payload MUST be formatted according to the backend sync API schema with proper JSON structure.

#### Scenario: Create batch with 50 statements

- GIVEN there are 55 statements pending synchronization
- WHEN a new batch is created
- THEN the first batch SHALL contain exactly 50 statements
- AND the remaining 5 statements SHALL be assigned to a second batch

#### Scenario: Create batch with remaining statements

- GIVEN there are 23 statements pending synchronization
- WHEN a new batch is created
- THEN the batch SHALL contain exactly 23 statements (no padding required)

### Requirement: xAPI Verb Registry

The system MUST include a predefined registry of xAPI verbs conforming to ADL xAPI specification. The registry SHALL map verb keys to their canonical URIs and multilingual display strings.

Supported verbs SHALL include: attempted, completed, answered, initialized, terminated, passed, failed.

#### Scenario: Retrieve verb definition

- GIVEN the application requires the "completed" verb
- WHEN `Verbs.get("completed")` is invoked
- THEN the verb definition SHALL be returned with id `http://adlnet.gov/expapi/verbs/completed`
- AND display strings SHALL include both English and Spanish variants

#### Scenario: Request undefined verb

- GIVEN the application requests a verb not in the registry
- WHEN `Verbs.get("custom_verb")` is invoked
- THEN `null` SHALL be returned
- AND no error SHALL be raised

### Requirement: Data Integrity on Application Crash

The system MUST ensure no statements are lost if the application crashes or is forcefully closed. All statements SHALL be persisted to SQLite immediately upon creation, not held in memory.

Batch operations MUST use database transactions to prevent partial batch state.

#### Scenario: Statement persists after crash

- GIVEN a statement has been created and saved to SQLite
- WHEN the application crashes before sync occurs
- THEN the statement SHALL remain in the `xapi_statement` table after restart
- AND the batch SHALL remain in `pending` status

#### Scenario: Transaction rollback on failure

- GIVEN a batch operation is in progress
- WHEN a database error occurs mid-operation
- THEN the entire batch operation SHALL be rolled back
- AND no partial state SHALL be persisted
