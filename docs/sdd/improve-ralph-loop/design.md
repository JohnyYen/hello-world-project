# Technical Design: Improve Ralph AFK Loop

This document describes the technical implementation details for refactoring the Ralph automation loop scripts.

## 1. Directory Structure Changes
The project structure will be updated to include centralized prompts and shared utilities:

```text
scripts/
├── lib/
│   └── ralph-common.sh       # Shared functions and validation logic
├── prompts/
│   └── ralph-master-instruction.md  # Template for AI instructions
├── ralph-afk.sh              # Refactored loop script
└── ralph-once.sh             # Refactored single-run script
```

## 2. Master Prompt Template
**File**: `scripts/prompts/ralph-master-instruction.md`

The instruction set for the AI agent, using placeholders for dynamic path resolution.

```markdown
1. Identifica la siguiente tarea pendiente ("passes": false) en el PRD.json para el proyecto {{PROJECT}}.
2. Lee el AGENTS.md en {{APP_PATH}} y sigue TODAS sus reglas críticas y estándares.
3. Implementa la tarea y ejecuta los comandos de verificación (test/lint) del AGENTS.md.
4. Si hay éxito, marca "passes": true en el PRD.json.
5. Actualiza progress.txt y realiza el commit.
6. Si no quedan tareas pendientes para {{PROJECT}}, responde con <promise>COMPLETE</promise>.
SOLO TRABAJA EN UNA TAREA.
```

## 3. Shared Logic Design (`ralph-common.sh`)
To eliminate duplication, common logic will be moved to `scripts/lib/ralph-common.sh`.

### 3.1. Initialization and Validation
A `validate_project` function will:
1. Verify the project name is provided and directory `apps/$PROJECT` exists.
2. Resolve paths for `PRD.json`, `AGENTS.md`, and `progress.txt`.
3. Create `progress.txt` if it doesn't exist.
4. Exit with error if `PRD.json` or `AGENTS.md` are missing.

### 3.2. Placeholder Replacement
The script will use `sed` to replace `{{PROJECT}}` and `{{APP_PATH}}` in the template.

**Method**:
```bash
get_prompt() {
    local project=$1
    local app_path=$2
    local template="scripts/prompts/ralph-master-instruction.md"
    
    # Escape pipes in paths if necessary, or use a different delimiter
    cat "$template" | sed "s|{{PROJECT}}|$project|g; s|{{APP_PATH}}|$app_path|g"
}
```

## 4. Logging & Observability
### 4.1. Directory Creation
Scripts will ensure `logs/ralph/$PROJECT` exists before execution.

### 4.2. Summary Log (`summary.log`)
- **Format**: `[{YYYY-MM-DD HH:MM:SS}] Iteration {i}/{TOTAL}: {STATUS} (Log: {filename})`
- **Statuses**: `STARTED`, `SUCCESS`, `FAILED`, `ABORTED`, `COMPLETE`.

### 4.3. Detailed Logs
Each iteration will capture the full output of `opencode run` into:
`logs/ralph/$PROJECT/${TIMESTAMP}_iter_${i}.log`

## 5. Refactored Scripts Logic
### 5.1. `ralph-afk.sh`
- Sources `ralph-common.sh`.
- Sets up a `trap` for `SIGINT` to log "ABORTED" in the summary log.
- Executes a `for` loop from 1 to `$ITERATIONS`.
- Captures output into the detailed log and parses it for `<promise>COMPLETE</promise>`.

### 5.2. `ralph-once.sh`
- Sources `ralph-common.sh`.
- Reuses `validate_project` and `get_prompt`.
- Executes a single iteration of `opencode run`.

## 6. Infrastructure & Safety
- **Git**: Ensure `logs/ralph/` is excluded from version control if `*.log` pattern is not enough or if we want to be explicit.
- **Error Handling**: Use `set -e` in the main loop to handle unexpected command failures.
- **Verification**: The script must verify that `opencode` is available in the PATH.
