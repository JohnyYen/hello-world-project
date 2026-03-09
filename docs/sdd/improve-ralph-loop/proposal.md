# Proposal: Improve Ralph AFK Loop Logic

**Change Name**: improve-ralph-loop
**Status**: Proposed
**Author**: Opencode SDD Sub-agent

## 1. Context & Problem Statement
The current `scripts/ralph-afk.sh` script is designed to automate task execution across different projects (`backend`, `frontend`, `game`). However, it has several limitations:
- **Hardcoded Paths**: It explicitly references `@apps/frontend/PRD.json` even when running for other projects.
- **Global Progress Tracking**: It uses a single `@progress.txt` (likely in the root), which prevents concurrent or isolated tracking per project.
- **Limited Observability**: Logging is minimal (only `echo` to stdout), making it hard to debug failed iterations or track history.
- **Basic Error Handling**: Relies solely on `set -e`, without sophisticated error reporting or state recovery.

## 2. Goals
- **Project Isolation**: Ensure each project uses its own `PRD.json` and `progress.txt` located within its respective directory.
- **Robust Path Handling**: Dynamically resolve paths based on the selected project.
- **Enhanced Logging**: Implement iteration-specific logging and a central log repository.
- **Improved Reliability**: Add explicit checks for file existence and better error reporting.

## 3. Proposed Changes

### 3.1. Dynamic File Resolution
Modify the `opencode run` command to use project-specific artifacts:
- PRD: `$APP_PATH/PRD.json`
- Progress: `$APP_PATH/progress.txt`

### 3.2. Script Logic Improvements
- **Validation**: Check if `$APP_PATH/PRD.json` exists before starting.
- **Logging**:
  - Redirect iteration output to `logs/ralph/$PROJECT/$(date +%Y%m%d_%H%M%S)_iter_$i.log`.
  - Maintain a `summary.log` for high-level progress.
- **Error Trapping**: Implement a `trap` function to log failures and provide a clear "Last known state" before exiting.

### 3.3. Project Structure Alignment
Ensure all projects (`backend`, `frontend`, `game`) follow a consistent pattern:
- `apps/<project>/PRD.json`
- `apps/<project>/progress.txt`
- `apps/<project>/AGENTS.md`

## 4. Risks & Considerations
- **Breaking Changes**: If a project doesn't have a `PRD.json` yet, the script will fail. We should decide if the script should initialize a blank PRD or if it's a prerequisite.
- **Log Management**: Automated loops can generate many log files. We should consider a simple rotation or cleanup strategy.

## 5. Next Steps
1. Create `specs.md` to define the exact script behavior.
2. Update the script implementation.
3. Verify with a test run on a mock project or a subset of tasks.
