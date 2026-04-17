# Tasks: Game Framework Refactor

## Phase 1: Infrastructure

### 1.1 Create directory structure
- Create `core/` with all subdirectories: models/, config/, database/, blocks/, engine/, agent/, controllers/, globals/, http/, utils/
- Create `content/level_1_cafeteria/` with all subdirectories: blocks/, engine/, agent/, controllers/, scenes/, database/

### 1.2 Move core models
- `git mv` all 10 files from `models/` → `core/models/`

### 1.3 Move core config
- `git mv` all 3 files from `config/` → `core/config/`

### 1.4 Move core database
- `git mv` connect.gd → `core/database/connect.gd`
- `git mv` all 6 repos → `core/database/repositories/`
- `git mv` 3 generic seeds → `core/database/seed/`

### 1.5 Move core engine
- `git mv` execution_engine.gd → `core/engine/execution_engine.gd`
- `git mv` base_problem_context.gd → `core/engine/problems_context/base_problem_context.gd`
- `git mv` abstract_action.gd → `core/engine/actions/abstract_action.gd`

### 1.6 Move core blocks
- `git mv` base_block, start_block, end_block, if_block, while_block → `core/blocks/`

### 1.7 Move core agent
- `git mv` adaptive_agent.gd → `core/agent/adaptive_agent.gd`
- `git mv` inference_engine.gd → `core/agent/inference_engine.gd`
- `git mv` inference/ → `core/agent/inference/`
- `git mv` analizer/ → `core/agent/analizer/`
- `git mv` base_level_modifier.gd → `core/agent/level_modifier/base_level_modifier.gd`

### 1.8 Move core controllers
- `git mv` game_controller, feedback_controller, dialogue_controller, dialogue_ui_controller, menu_controller, progress_controller, save_controller → `core/controllers/`
- `git mv` sync_service.gd → `core/controllers/service/sync_service.gd`
- `git mv` levels/ (enum, controller, strategy, configuration) → `core/controllers/levels/`

### 1.9 Move core globals, http, utils
- `git mv` game_state.gd, DialogueDirector.gd → `core/globals/`
- `git mv` http_client.gd, http_request.gd → `core/http/`
- `git mv` eventBus.gd → `core/utils/eventBus.gd`
- `git mv` util.gd → `core/utils/util.gd`
- `git mv` env.gd → `core/env.gd`

## Phase 2: Content Separation

### 2.1 Move cafeteria engine
- `git mv` cafeteria_problem_context.gd → `content/level_1_cafeteria/engine/problems_context/`
- `git mv` action_factory.gd → `content/level_1_cafeteria/engine/actions/`
- `git mv` cafeteria_actions.gd → `content/level_1_cafeteria/engine/actions/`
- `git mv` all 6 cafeteria actions → `content/level_1_cafeteria/engine/actions/cafeteria/`

### 2.2 Move cafeteria blocks
- `git mv` execute_block.gd → `content/level_1_cafeteria/blocks/`

### 2.3 Move cafeteria controller
- `git mv` level_one_controller.gd → `content/level_1_cafeteria/controllers/levels/`
- `git mv` level_one_configuration.gd → `content/level_1_cafeteria/controllers/levels/`

### 2.4 Move cafeteria agent
- `git mv` level_one_modifier.gd → `content/level_1_cafeteria/agent/level_modifier/`

### 2.5 Move cafeteria seeds
- `git mv` seed_levels.gd → `content/level_1_cafeteria/database/seed/`
- `git mv` seed_segments.gd → `content/level_1_cafeteria/database/seed/`

### 2.6 Move cafeteria scene scripts
- `git mv` cafeteria_gameplay.gd → `content/level_1_cafeteria/scenes/pages/levels/cafeteria/`
- `git mv` tutorial_gameplay.gd → `content/level_1_cafeteria/scenes/pages/tutorial/`
- `git mv` student.gd → `content/level_1_cafeteria/scenes/characters/level_one/`

## Phase 3: Import Path Updates

### 3.1 Update project.godot autoloads
- Update all 10 autoload paths to point to new locations

### 3.2 Fix imports in core files
- Update all `preload()`, `load()`, and type references in `core/` files

### 3.3 Fix imports in content files
- Update all `preload()`, `load()`, and type references in `content/` files

### 3.4 Fix imports in scene scripts
- Update all imports in `scenes/` that reference moved files

### 3.5 Fix imports in test files
- Relocate tests alongside their sources
- Update test imports

## Phase 4: Verification

### 4.1 Verify project.godot
- Check all autoload paths are valid

### 4.2 Verify compilation
- Open project in Godot (headless check)
- Ensure zero script errors

### 4.3 Run tests
- Execute GUT tests
- Verify all pass

## Phase 5: Commit
- Conventional commit: `refactor(game): separate core framework from level 1 content`
