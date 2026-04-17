# Design: Game Framework Refactor

## Architecture Decision: File Move Over Logic Rewrite

**Decision**: Move files into `core/` and `content/` without changing their internal logic (except the 6 coupling fixes).

**Rationale**: The refactor's goal is organization and extensibility, not behavior change. Rewriting logic introduces regression risk. We will create abstractions (abstract classes) as part of the move but keep existing implementations intact.

## Architecture Decision: Scenes Stay at Root

**Decision**: `.tscn` scene files and their attached `.gd` scripts remain at root level under `scenes/`.

**Rationale**: Scenes are application-layer artifacts in Godot. Moving them would require updating every scene file's internal path references (complex, error-prone). Keeping them at root maintains Godot's expectations while the framework logic moves to `core/`.

## Directory Structure

```
apps/game/
├── core/                              ← Framework (agnostic)
│   ├── models/                        ← 10 entity/model files
│   ├── config/                        ← game_config, feedback_config, config
│   ├── database/
│   │   ├── connect.gd
│   │   ├── repositories/              ← 6 repos
│   │   └── seed/                      ← 3 generic seeds
│   ├── blocks/                        ← base_block, start, end, if, while
│   ├── engine/
│   │   ├── execution_engine.gd
│   │   ├── problems_context/base_problem_context.gd
│   │   └── actions/abstract_action.gd
│   ├── agent/
│   │   ├── adaptive_agent.gd
│   │   ├── inference/                 ← base + rule
│   │   ├── analizer/                  ← base + performance
│   │   └── level_modifier/base_level_modifier.gd
│   ├── controllers/
│   │   ├── game_controller.gd
│   │   ├── feedback_controller.gd
│   │   ├── dialogue_controller.gd
│   │   ├── dialogue_ui_controller.gd
│   │   ├── menu_controller.gd
│   │   ├── progress_controller.gd
│   │   ├── save_controller.gd
│   │   ├── service/sync_service.gd
│   │   └── levels/                    ← level_enum, level_controller, level_strategy, level_configuration
│   ├── globals/                       ← game_state, DialogueDirector
│   ├── http/                          ← http_client, http_request
│   ├── utils/                         ← eventBus, util
│   └── env.gd
│
├── content/
│   └── level_1_cafeteria/             ← Domain-specific
│       ├── blocks/execute_block.gd
│       ├── engine/
│       │   ├── problems_context/cafeteria_problem_context.gd
│       │   └── actions/               ← action_factory + cafeteria/
│       ├── agent/level_modifier/level_one_modifier.gd
│       ├── controllers/levels/
│       │   ├── level_one_controller.gd
│       │   └── level_one_configuration.gd
│       ├── scenes/                    ← cafeteria-specific scene scripts
│       └── database/seed/
│           ├── seed_levels.gd
│           └── seed_segments.gd
│
├── scenes/                            ← VIEW: all .tscn + scene scripts (stays)
├── scripts/                           ← Controller: thin re-export or app-specific
├── models/                            ← Model: thin re-export or app-specific
├── dialogue/                          ← Stays
├── data/                              ← Stays (JSON configs)
├── addons/                            ← Stays
├── test/                              ← Tests (relocated with sources)
├── config/                            ← Re-export from core or stays as app config
├── project.godot                      ← Updated autoloads
└── env.gd                             ← Removed (moved to core/)
```

## Migration Strategy

1. **Create directories** — `core/` and `content/level_1_cafeteria/`
2. **Move core files** — Use `git mv` to preserve history
3. **Update imports** — Fix all `preload()`, `load()`, type references
4. **Update project.godot** — Fix autoload paths
5. **Fix coupling issues** — 6 identified problems
6. **Move tests** — Alongside their source files
7. **Verify** — Compile + run tests

## Sequence Diagram: How Core and Content Interact After Refactor

```
[GameController] → create_level_controller(LevelEnum.LEVEL_ONE)
       │
       ▼
[LevelStrategy] → returns LevelOneController (from content/)
       │
       ▼
[LevelOneController._init()]
  ├── Creates CafeteriaProblemContext (from content/)
  ├── Creates LevelOneModifier (from content/)
  └── Connects agent.action_decided → modifier.modify_level()
       │
       ▼
[LevelOneController.get_problem_context()]
  ├── Loads LevelOneConfiguration (from content/)
  └── Returns configured CafeteriaProblemContext
       │
       ▼
[ExecutionEngine.execute(blocks, context)]
  └── Uses core/ engine, domain-specific context
       │
       ▼
[CafeteriaProblemContext.is_solution_correct()]
  └── Domain-specific validation (from content/)
```

## Coupling Fixes Detail

### Fix 1: ExecutionBlock
Currently casts to `CafeteriaProblemContext` directly.
**Fix**: Keep as-is in `content/` since it IS domain-specific. No change needed.

### Fix 2: LibraryExecutionBlock
Currently extends `Block` instead of `BaseBlock`.
**Fix**: Move to future `content/level_2_library/`, fix extends there.

### Fix 3: ActionFactory
Currently hardcodes cafeteria actions.
**Fix**: Move to `content/level_1_cafeteria/engine/actions/`. Core has only `abstract_action.gd`.

### Fix 4: LevelOneController hardcodes dependencies
**Fix**: Acceptable for now. Factory injection via LevelStrategy already works.

### Fix 5: cafeteria_gameplay.gd (356 lines)
**Fix**: Move to `content/level_1_cafeteria/scenes/`. Scene file stays at root, script moves.

### Fix 6: seed_segments.gd has 302 lines of JSON
**Fix**: The data already exists in `data/levels/cafeteria_level_config.json`. The seed script should `load()` the JSON file instead of having it inline. Defer to future improvement — keep as-is for now to avoid risk.
