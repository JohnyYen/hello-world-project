# Game Framework Specification

## Requirement 1: Core Framework Separation

The system SHALL provide a `core/` directory containing all agnostic framework components that are NOT tied to any specific educational domain.

### Scenario 1.1: Core contains engine abstractions
- **Given** the framework is organized into `core/`
- **When** a developer looks in `core/engine/`
- **Then** they SHALL find: `execution_engine.gd`, `base_problem_context.gd`, `abstract_action.gd`
- **And** NONE of these files SHALL reference "cafeteria", "library", or any domain name

### Scenario 1.2: Core contains agent abstractions
- **Given** the adaptive difficulty system is part of the framework
- **When** a developer looks in `core/agent/`
- **Then** they SHALL find: `adaptive_agent.gd`, `inference/`, `analizer/`, `level_modifier/base_level_modifier.gd`
- **And** NONE of these files SHALL reference domain-specific level modifiers

### Scenario 1.3: Core contains controller abstractions
- **Given** the controller layer is part of the framework
- **When** a developer looks in `core/controllers/`
- **Then** they SHALL find: `game_controller.gd`, `feedback_controller.gd`, `save_controller.gd`, `levels/level_controller.gd` (abstract), `levels/level_configuration.gd` (abstract), `levels/level_strategy.gd`, `levels/level_enum.gd`

### Scenario 1.4: Core contains database layer
- **Given** persistence is part of the framework
- **When** a developer looks in `core/database/`
- **Then** they SHALL find: `connect.gd`, `repositories/` (6 files), `seed/` (3 generic seed files)

### Scenario 1.5: Core contains models
- **Given** domain models are part of the framework
- **When** a developer looks in `core/models/`
- **Then** they SHALL find: `block.gd`, `block_type.gd`, `block_type_enum.gd`, `execute_block.gd`, `level.gd`, `player.gd`, `progress.gd`, `segment.gd`, `segment_block.gd`, `dto/progress_data.gd`

### Scenario 1.6: Core contains config and utils
- **Given** configuration and utilities are framework-level concerns
- **When** a developer looks in `core/`
- **Then** they SHALL find: `config/` (3 files), `globals/` (2 files), `http/` (2 files), `utils/eventBus.gd`, `utils/util.gd`, `env.gd`

## Requirement 2: Content Separation

Domain-specific content SHALL be organized under `content/level_N_name/` directories.

### Scenario 2.1: Cafeteria content is isolated
- **Given** Level 1 is the cafeteria scenario
- **When** a developer looks in `content/level_1_cafeteria/`
- **Then** they SHALL find: `engine/problems_context/cafeteria_problem_context.gd`, `engine/actions/` (all cafeteria actions), `agent/level_modifier/level_one_modifier.gd`, `controllers/levels/level_one_controller.gd`, `controllers/levels/level_one_configuration.gd`, `blocks/execute_block.gd`, `database/seed/seed_levels.gd`, `database/seed/seed_segments.gd`

### Scenario 2.2: Cafeteria scenes remain accessible
- **Given** scene files (`.tscn`) stay at root level
- **When** cafeteria-specific scene scripts exist
- **THEN** their `.gd` scripts SHALL be in `content/level_1_cafeteria/scenes/` or remain at root if they are shared

## Requirement 3: Import Path Resolution

All import paths, `preload()`, and `load()` calls SHALL be updated to reflect the new file locations.

### Scenario 3.1: project.godot autoloads are updated
- **Given** the game uses 10 autoload singletons
- **When** the refactor is complete
- **Then** all autoload paths in `project.godot` SHALL point to files under `core/` or `content/` as appropriate

### Scenario 3.2: Cross-references work correctly
- **Given** core files reference each other
- **When** the game runs
- **Then** NO import errors SHALL occur for moved files

## Requirement 4: Backwards Compatibility

The application layer (scenes, root-level structure) SHALL continue to function.

### Scenario 4.1: Scenes still reference controllers
- **Given** `.tscn` scenes reference GDScript files
- **When** the refactor is complete
- **Then** all scene script paths SHALL be valid and scenes SHALL load without errors

### Scenario 4.2: Game compiles in Godot
- **Given** the project opens in Godot 4.4
- **When** the refactor is complete
- **Then** Godot SHALL report zero script errors in the output console

## Requirement 5: No Behavioral Changes

The refactor SHALL NOT alter runtime behavior.

### Scenario 5.1: Same execution output
- **Given** the game runs Level 1
- **When** the refactor is complete
- **Then** the game SHALL behave identically from the player's perspective (same menus, same dialogue, same level flow)

### Scenario 5.2: Tests still pass
- **Given** 15 GUT test files exist
- **When** the refactor is complete
- **Then** all tests SHALL be relocated and SHALL pass with the same results as before

## Requirement 7: Framework Extension Points — Interaction Mechanism

The framework SHALL provide an abstract `InteractionMechanism` base class that defines how players interact with the game, WITHOUT assuming any specific input method (blocks, drag-drop, text, selection, etc.).

### Scenario 7.1: InteractionMechanism is abstract and domain-agnostic
- **Given** a developer wants to create a new interaction type
- **When** they look in `core/engine/interaction/interaction_mechanism.gd`
- **Then** they SHALL find an abstract base class with:
  - A `get_player_solution()` method that returns a `SolutionData` object
  - Virtual method placeholders that subclasses MUST override
- **And** the class SHALL NOT reference blocks, cafeteria, or any specific input type

### Scenario 7.2: BlockInteraction extends InteractionMechanism
- **Given** the current game uses visual programming blocks
- **When** a developer looks in `core/engine/interaction/block_interaction.gd`
- **Then** they SHALL find a concrete implementation of `InteractionMechanism`
- **And** it SHALL provide `get_player_solution()` returning block data as `SolutionData`

### Scenario 7.3: New interaction types can be created without modifying core
- **Given** a developer wants a drag-and-drop interaction for a circuit-building game
- **When** they create `content/level_X/engine/interaction/circuit_interaction.gd`
- **Then** they SHALL extend `InteractionMechanism`
- **And** they SHALL NOT need to modify any file in `core/`

## Requirement 8: Framework Extension Points — Executor

The framework SHALL provide an abstract `Executor` base class that defines how player solutions are executed against the problem context, WITHOUT assuming sequential execution.

### Scenario 8.1: Executor is abstract and domain-agnostic
- **Given** a developer needs a custom execution strategy
- **When** they look in `core/engine/execution/executor.gd`
- **Then** they SHALL find an abstract base class with:
  - An `execute(solution: SolutionData, context: BaseProblemContext)` method that returns `ExecutionContext`
  - Virtual method placeholders
- **And** the class SHALL NOT assume linear or block-based execution

### Scenario 8.2: SequentialExecutor exists for current use case
- **Given** the current game executes blocks in order
- **When** a developer looks in `core/engine/execution/sequential_executor.gd`
- **Then** they SHALL find it extends `Executor`
- **And** the current `ExecutionEngine` logic SHALL be encapsulated within it

### Scenario 8.3: ExecutionEngine delegates to Executor
- **Given** the framework has both ExecutionEngine and Executor
- **When** `ExecutionEngine.execute()` is called
- **Then** it SHALL delegate to the configured `Executor` instance
- **And** backwards compatibility SHALL be maintained for existing callers

## Requirement 9: Framework Extension Points — Validation Strategy

The framework SHALL provide an abstract `ValidationStrategy` base class that defines how solutions are validated, WITHOUT assuming exact-match validation.

### Scenario 9.1: ValidationStrategy is abstract and domain-agnostic
- **Given** a developer needs custom validation logic
- **When** they look in `core/engine/validation/validation_strategy.gd`
- **Then** they SHALL find an abstract base class with:
  - A `validate(execution_context: ExecutionContext, problem_context: BaseProblemContext)` method returning `ValidationResult`
- **And** the class SHALL NOT assume outputs == expected_outputs

### Scenario 9.2: Context-based validation is the default
- **Given** the current system validates via `BaseProblemContext.is_solution_correct()`
- **When** a developer looks in `core/engine/validation/context_validation.gd`
- **Then** they SHALL find a `ValidationStrategy` that delegates to `context.is_solution_correct()`
- **And** this SHALL preserve current behavior

## Requirement 10: Framework Extension Points — Metrics Collector

The framework SHALL provide an abstract `MetricsCollector` base class that defines what performance data is collected for the adaptive agent.

### Scenario 10.1: MetricsCollector is abstract and configurable
- **Given** different games need different metrics
- **When** they look in `core/agent/analyzer/metrics_collector.gd`
- **Then** they SHALL find an abstract base class with:
  - A `collect(execution_context: ExecutionContext) -> Dictionary` method
- **And** the class SHALL NOT hardcode specific metric names

### Scenario 10.2: PerformanceMetricsCollector extends MetricsCollector
- **Given** the current agent tracks score, errors, time
- **When** a developer looks in `core/agent/analyzer/performance_metrics_collector.gd`
- **Then** they SHALL find a concrete implementation
- **And** it SHALL be compatible with the existing `PerformanceAnalyzer`

## Requirement 11: Framework Extension Points — Difficulty Modifier

The framework SHALL improve the `BaseLevelModifier` to accept composable modifier strategies instead of hardcoding modification logic per level.

### Scenario 11.1: BaseLevelModifier provides generic interface
- **Given** difficulty modification varies by level
- **When** a developer looks in `core/agent/level_modifier/base_level_modifier.gd`
- **Then** they SHALL find an abstract method `modify_level(segment_config: Dictionary, action: String) -> Dictionary`
- **And** it SHALL define helper methods common to all modifiers

### Scenario 11.2: LevelOneModifier extends BaseLevelModifier
- **Given** Level 1 has specific modifier needs
- **When** they look in `content/level_1_cafeteria/agent/level_modifier/level_one_modifier.gd`
- **Then** it SHALL extend `BaseLevelModifier`
- **And** its logic SHALL remain functionally identical

## Requirement 12: Level Configuration from JSON

The framework SHALL support loading level definitions from JSON configuration files, reducing hardcoded GDScript for level data.

### Scenario 12.1: LevelConfig loader reads from JSON
- **Given** level data is currently embedded in seed scripts
- **When** a developer uses `core/config/level_json_config.gd`
- **Then** they SHALL be able to load level definitions from `data/levels/{level_id}_config.json`
- **And** the returned structure SHALL match the `Level` and `Segment` models

### Scenario 12.2: Cafeteria level config is loaded from existing JSON file
- **Given** `data/levels/cafeteria_level_config.json` already exists
- **When** `LevelOneConfiguration` loads its data
- **Then** it SHALL read from the JSON file instead of having inline data
- **And** the behavior SHALL be identical to before

## Requirement 13: BaseProblemContext Improvement

The `BaseProblemContext` SHALL be improved to support the new abstractions while maintaining backward compatibility.

### Scenario 13.1: BaseProblemContext works with SolutionData
- **Given** the executor now uses `SolutionData` instead of raw block arrays
- **When** `BaseProblemContext` is used
- **Then** it SHALL accept `SolutionData` as input
- **And** it SHALL convert to internal representation as needed

### Scenario 13.2: Backward compatibility with block arrays
- **Given** existing code calls `ExecutionEngine.execute(blocks, context)`
- **When** that method is called
- **Then** it SHALL internally wrap blocks in `SolutionData`
- **And** existing callers SHALL NOT break
