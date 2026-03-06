# Hello World Game - AI Agent Ruleset

> **Skills Reference**: For detailed patterns, use these skills:
> - [`godot-4`](https://docs.godotengine.org/en/stable/) - GDScript 2.0, Signal patterns
> - [`architecture-patterns`](#) - MVC in Game Development
> - [`tdd`](#) - Test-Driven Development workflow

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| Committing changes | `prowler-commit` |
| Fixing bug | `tdd` |
| Implementing feature | `tdd` |
| Refactoring code | `tdd` |
| Working on task | `tdd` |

---

## CRITICAL RULES - NON-NEGOTIABLE

### GDScript Coding Standards
- ALWAYS: Use explicit type hints for variables and function returns (`var x: int`, `-> void`).
- ALWAYS: Use `class_name` to register global classes.
- ALWAYS: Use 4-space indentation (standard for this project).
- NEVER: Use untyped arrays or dictionaries if the content type is known.

### Architecture (MVC Pattern)
- ALWAYS: Separate logic into `models/` (Data), `scripts/` (Controllers), and `scenes/` (Views).
- ALWAYS: Use Signal-based communication between nodes to avoid tight coupling.
- NEVER: Hardcode configuration values; use `config/game_config.gd` or `env.gd`.

### Database
- ALWAYS: Use the repository pattern for SQLite operations in `scripts/database/repositories/`.
- NEVER: Execute raw SQL queries directly inside UI scripts or game logic.

---

## TECH STACK

Godot 4.x | GDScript 2.0 | SQLite | GUT (Godot Unit Test)

---

## PROJECT STRUCTURE

```
apps/game/
├── models/             # Data structures and resources
├── scenes/             # UI and Level scenes (.tscn)
├── scripts/            # Controllers and logic
│   ├── database/       # SQLite repositories
│   └── engine/         # Core game mechanics
├── assets/             # Textures, sounds, and fonts
└── config/             # Game configuration
```

---

## COMMANDS

```bash
# Testing
# Use the GUT (Godot Unit Test) panel in the Godot Editor
# Or run from CLI if configured:
# godot --headless -s addons/gut/gut_cmdline.gd
```

---

## QA CHECKLIST

- [ ] Explicit type hints on all new functions/variables
- [ ] Signals used for cross-node communication
- [ ] Logic separated from UI scripts
- [ ] Database access via repositories
- [ ] Spanish UI for user-facing text
