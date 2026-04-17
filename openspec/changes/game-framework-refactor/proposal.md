# Game Framework Refactor

## Problem
The current Godot game codebase mixes framework-level logic (execution engine, adaptive agent, controllers) with domain-specific content (cafeteria actions, contexts, level configs). This makes it impossible to create new educational games without modifying core code.

## Solution
Separate the codebase into two distinct layers:
- **`core/`** — Agnostic framework: execution engine, adaptive agent, base blocks, abstract controllers, database layer, models, utils
- **`content/level_1_cafeteria/`** — Domain-specific content: cafeteria context, cafeteria actions, level one controller/modifier, cafeteria scenes, seed data

## Goals
1. Any developer can create a new educational game by extending core abstractions and placing content in `content/level_N_name/`
2. The framework MUST NOT know about cafeteria, library, or any specific domain
3. The game MUST still compile and run after the refactor with zero behavioral changes
4. Scenes (`.tscn`) remain at root level as application-layer artifacts
5. MVC pattern is preserved: `scenes/` = View, `scripts/` = Controller (re-exports from core), `models/` = Model (re-exports from core)

## Non-Goals
- Do NOT redesign the UI/UX
- Do NOT implement If/While control flow jumps (not priority)
- Do NOT redesign the CodeSpace drag-and-drop (separate branch)
- Do NOT fix SQL injection issues (not priority)
- Do NOT connect to real backend (separate concern)

## Affected Modules
- ALL `.gd` files in `apps/game/scripts/`, `apps/game/models/`, `apps/game/config/`
- `project.godot` autoloads (paths will change)
- Test files (must be relocated alongside their source files)

## Rollback Plan
Delete `core/` and `content/` directories, restore original `scripts/`, `models/`, `config/` from git history. All changes are file moves + import path updates — no logic changes.
