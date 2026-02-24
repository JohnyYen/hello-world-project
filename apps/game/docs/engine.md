# Game Execution Engine Documentation

## Overview

The Execution Engine is the core component that powers the educational programming puzzle game. It interprets and executes visual programs created by players using a limited set of programming blocks. The engine is designed to be flexible and extensible, allowing for different game scenarios while maintaining a consistent core architecture.

## Core Concepts

### 1. Execution Context

The execution context represents the complete state of the game world at any point during program execution. It consists of two main components:

#### Program Execution State
This part manages the flow of the visual program:
- **Program Counter**: Tracks which block will be executed next
- **Variables**: Stores named values that can be manipulated by the program
- **Call Stack**: Manages nested control structures (loops and conditionals)
- **Execution Status**: Indicates whether the program is still running

#### Level-Specific State
This part represents the unique elements of each game scenario:
- **Inputs**: Initial data the player's program must process
- **Outputs**: Results produced by the player's program
- **Expected Outputs**: Target results used to verify if the player's solution is correct
- **Domain-Specific Properties**: Scenario-specific elements (e.g., student queue in a cafeteria level)

### 2. Base Problem Context

The BaseProblemContext is an abstract class that defines the generic interface for all execution contexts. It contains:
- All program execution state properties
- Generic input/output handling
- Basic variable management
- Default solution verification logic
- Utility methods for block interaction

This class is never instantiated directly but serves as the foundation for all scenario-specific contexts.

### 3. Scenario-Specific Contexts

Each game level extends BaseProblemContext to create a scenario-specific context. For example:
- CafeteriaProblemContext for cafeteria management levels
- LibraryProblemContext for library organization levels

These specialized contexts add properties and methods relevant to their domain while inheriting all generic functionality.

## Execution Engine

The ExecutionEngine is responsible for interpreting and executing the player's visual program. It operates as a state machine that:

1. Takes an array of blocks representing the player's program
2. Receives an execution context (scenario-specific)
3. Processes each block according to its type
4. Updates the execution context as blocks are executed
5. Manages control flow for structured programming constructs
6. Returns the final context after program completion

### Block Processing

The engine supports these block types:
- **Inicio/Fin**: Mark the beginning and end of program sections
- **Ejecutar**: Executes a domain-specific action stored in the block
- **If**: Conditional execution based on a variable comparison
- **While**: Looping construct based on a variable condition

### Control Flow Management

The engine properly handles nested control structures using a call stack:
- When entering an If or While block, the engine records the start and end positions
- When reaching a Fin block, it checks the call stack to determine where to jump next
- This allows for proper execution of nested conditions and loops

## Extending the Engine

### Adding New Scenarios

To create a new game scenario:

1. Create a new context class that extends BaseProblemContext
2. Add scenario-specific properties and methods
3. Override the `is_solution_correct()` method with scenario-specific validation logic
4. Create or modify blocks to interact with the new context properties

### Adding New Block Types

New block types can be added by:
1. Creating a new block class that extends the base Block class
2. Implementing any required methods (execute, evaluate_condition, etc.)
3. Updating the ExecutionEngine to recognize and process the new block type

## Design Principles

### Separation of Concerns
- The engine handles program execution flow
- Context objects manage state
- Blocks define specific behaviors
- Level controllers orchestrate the entire process

### Extensibility
- New scenarios can be added without modifying the core engine
- Block behaviors can be extended or modified independently
- Context validation logic can be customized per scenario

### Type Safety
- The engine works with BaseProblemContext, allowing any specialized context
- Blocks can safely cast the context to access scenario-specific properties
- Clear interfaces prevent inappropriate context-block combinations

## Usage Flow

1. Level controller creates and configures a scenario-specific context
2. Player builds a program using visual blocks in the CodeSpace
3. ExecutionEngine.execute() is called with the block array and context
4. Engine processes each block, updating the context
5. Final context is returned to the level controller
6. Level controller verifies solution correctness using context.is_solution_correct()