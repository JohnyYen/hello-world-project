# Technical Specifications: Improve Ralph AFK Loop

**Change Name**: improve-ralph-loop
**Status**: Specified
**Related Proposal**: [proposal.md](./proposal.md)

## 1. Overview
This specification details the improvements to the "Ralph" automation loop scripts (`ralph-afk.sh` and `ralph-once.sh`). The goal is to eliminate hardcoded paths, centralize prompt instructions, and enhance observability through structured logging and project-specific file resolution.

## 2. Folder Structure
The following structure will be established/enforced:

```text
/
├── apps/
│   ├── backend/
│   │   ├── PRD.json          # Project-specific task list
│   │   ├── progress.txt      # Project-specific progress log
│   │   └── AGENTS.md         # Project-specific instructions
│   ├── frontend/ ...
│   └── game/ ...
├── scripts/
│   ├── ralph-afk.sh          # Main loop script
│   ├── ralph-once.sh         # Single-run script
│   └── prompts/
│       └── ralph-master-instruction.md  # SSOT for prompt logic
└── logs/
    └── ralph/
        └── {project}/        # Log root for each project
            ├── summary.log   # Chronological summary of all runs
            └── {timestamp}_iter_{n}.log  # Detailed iteration output
```

## 3. Master Prompt (SSOT)
The file `scripts/prompts/ralph-master-instruction.md` will contain the logic for the AI agent.

### 3.1. Placeholders
The following placeholders will be used for dynamic replacement:
- `{{PROJECT}}`: The name of the project (e.g., `backend`).
- `{{APP_PATH}}`: The relative path to the project directory (e.g., `apps/backend`).

### 3.2. Prompt Content Template
```markdown
1. Identifica la siguiente tarea pendiente ("passes": false) en el PRD.json para el proyecto {{PROJECT}}.
2. Lee el AGENTS.md en {{APP_PATH}} y sigue TODAS sus reglas críticas y estándares.
3. Implementa la tarea y ejecuta los comandos de verificación (test/lint) del AGENTS.md.
4. Si hay éxito, marca "passes": true en el PRD.json.
5. Actualiza progress.txt y realiza el commit.
6. Si no quedan tareas pendientes para {{PROJECT}}, responde con <promise>COMPLETE</promise>.
SOLO TRABAJA EN UNA TAREA.
```

## 4. Script Logic & File Resolution

### 4.1. Variable Replacement
The scripts will load the master prompt and replace placeholders using `sed`:
```bash
PROMPT_TEMPLATE=$(cat scripts/prompts/ralph-master-instruction.md)
FINAL_PROMPT=$(echo "$PROMPT_TEMPLATE" | sed "s|{{PROJECT}}|$PROJECT|g; s|{{APP_PATH}}|$APP_PATH|g")
```

### 4.2. File Resolution Strategy
For a given `$PROJECT`:
- **APP_PATH**: `apps/$PROJECT`
- **PRD**: `$APP_PATH/PRD.json`. 
  - *Validation*: If missing, the script must exit with an error.
- **AGENTS**: `$APP_PATH/AGENTS.md`.
  - *Validation*: If missing, the script must exit with an error.
- **PROGRESS**: `$APP_PATH/progress.txt`.
  - *Validation*: If missing, the script should create it.

### 4.3. Logging Mechanism
- **Detailed Log**: `logs/ralph/$PROJECT/${TIMESTAMP}_iter_${i}.log`
  - Captures the full output of the `opencode run` command.
- **Summary Log**: `logs/ralph/$PROJECT/summary.log`
  - Format: `[{TIMESTAMP}] Iteration {i}/{TOTAL}: {STATUS} (Log: {filename})`

### 4.4. Error Handling
- Use `set -e` for early exit on command failure.
- Implement a `trap` to log "Aborted" status in `summary.log` on `SIGINT` or unexpected exit.

## 5. CLI Signature
No changes to the existing signatures are required, but internal validation will be stricter.
- `scripts/ralph-afk.sh <iterations> <project>`
- `scripts/ralph-once.sh <project>`

## 6. Implementation Tasks (High-Level)
1. Create `scripts/prompts/ralph-master-instruction.md`.
2. Ensure `logs/ralph/{project}` directories are ignored by git (via `.gitignore`).
3. Refactor `scripts/ralph-afk.sh` to use the template and dynamic paths.
4. Refactor `scripts/ralph-once.sh` to share the same logic.
5. Create missing `PRD.json` or `progress.txt` where necessary (or document requirement).
