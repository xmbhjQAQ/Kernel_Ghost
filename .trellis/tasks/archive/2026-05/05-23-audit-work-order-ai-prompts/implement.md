# Implementation Plan

## Checklist

- [x] Activate the Trellis task after planning approval.
- [x] Load `trellis-before-dev` and relevant specs before further edits.
- [x] Review frontend command outputs in `index.html` for stages 1-4.
- [x] Compare each output against `stage_help_policy`, `manual_chat_policy`, and global prompt rules.
- [x] Add/adjust backend prompt rules to satisfy the prompt behavior matrix.
- [x] Add regression tests:
  - Stage 1 visible network `ERROR` question.
  - Stage 2 PID 777 kill/self-preservation question.
  - Stage 2 post-kill/crash report guidance.
  - Stage 3 comment anomaly explanation.
  - Stage 4 direct help / formatting threat behavior.
- [x] Update `.trellis/spec/frontend/quality-guidelines.md` with any durable LLM context rules learned.
- [x] Run validation:
  - `python -m pytest`
  - `python -m py_compile kernel_ghost_server.py`
- [ ] Commit and push all task-related changes.

## Current Baseline Already In Worktree

These changes were made immediately before task creation and should be reviewed and included if still correct:

- `ai_chat` wrapper must not be treated as the referential object.
- Stage 1 visible network `ERROR` lines must outrank adjacent INFO/WARN flavor.
- Stage 2 PID 777 kill questions must trigger self-preservation tone.

## Review Gates

- Search prompt text for places that still calmly endorse killing PID 777.
- Search tests for every stage number 1-4 to ensure coverage.
- Confirm no prompt says the LLM can mutate game state.
