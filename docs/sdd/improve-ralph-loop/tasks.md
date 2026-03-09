# Implementation Tasks: Improve Ralph AFK Loop

This document outlines the step-by-step tasks required to implement the improvements to the Ralph automation loop scripts.

## Phase 1: Preparation
- [ ] **Task 1.1**: Create required directories: `scripts/prompts/` and `scripts/lib/`.
- [ ] **Task 1.2**: Create `scripts/prompts/ralph-master-instruction.md` with the SSOT prompt content.
- [ ] **Task 1.3**: Update `.gitignore` to explicitly ignore `logs/ralph/` directory.

## Phase 2: Common Library Implementation
- [ ] **Task 2.1**: Create `scripts/lib/ralph-common.sh`.
- [ ] **Task 2.2**: Implement `validate_project` function in `ralph-common.sh`.
    - Must resolve `APP_PATH`, `PRD`, `AGENTS`, and `PROGRESS` paths.
    - Must verify `PRD.json` and `AGENTS.md` exist.
    - Must create `progress.txt` if missing.
- [ ] **Task 2.3**: Implement `get_prompt` function in `ralph-common.sh`.
    - Must use `sed` to replace `{{PROJECT}}` and `{{APP_PATH}}`.
- [ ] **Task 2.4**: Add check for `opencode` CLI availability in `ralph-common.sh`.

## Phase 3: Refactor `ralph-once.sh`
- [ ] **Task 3.1**: Refactor `scripts/ralph-once.sh` to source `ralph-common.sh`.
- [ ] **Task 3.2**: Replace project validation and prompt logic with calls to the common library.
- [ ] **Task 3.3**: Implement logging:
    - Detailed log in `logs/ralph/$PROJECT/${TIMESTAMP}_once.log`.
    - Entry in `logs/ralph/$PROJECT/summary.log`.

## Phase 4: Refactor `ralph-afk.sh`
- [ ] **Task 4.1**: Refactor `scripts/ralph-afk.sh` to source `ralph-common.sh`.
- [ ] **Task 4.2**: Implement main loop logic with `set -e` and proper iteration tracking.
- [ ] **Task 4.3**: Implement `trap` for `SIGINT` (Ctrl+C) and unexpected exits to log `ABORTED` status.
- [ ] **Task 4.4**: Implement logging:
    - Detailed log per iteration: `logs/ralph/$PROJECT/${TIMESTAMP}_iter_${i}.log`.
    - Summary log updates per iteration.
- [ ] **Task 4.5**: Add logic to detect `<promise>COMPLETE</promise>` and terminate the loop early with `COMPLETE` status.

## Phase 5: Verification
- [ ] **Task 5.1**: Run `scripts/ralph-once.sh backend` (or a dummy project) and verify successful execution and logging.
- [ ] **Task 5.2**: Run `scripts/ralph-afk.sh 2 backend` and verify loop behavior, trap handling, and summary log format.
- [ ] **Task 5.3**: Verify that `PRD.json` and `AGENTS.md` missing errors are handled correctly by the scripts.
- [ ] **Task 5.4**: Confirm `logs/` directory is correctly ignored by git.
