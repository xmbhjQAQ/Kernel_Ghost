# Implementation Plan

## Full Scope

1. Read frontend/backend specs.
2. Start the Trellis task.
3. Update `kernel_ghost_server.py` persona prompt for revised memory-fragment and work-comment setting.
4. Update Stage 1 deterministic output in `index.html` to use the revised keystroke/temperature/backlight/alarm-intercept residue and quick clearing behavior.
5. Update Stage 2 process/crash-report output in `index.html` to use repeated diary/progress fragments and analysis notes with emotional leakage.
6. Add `patience` state and UI.
7. Add Stage 3 `ai_chat` patience decrement.
8. Add direct-help confirmation flow and indirect project-text hint output.
9. Add forced erasure on patience zero.
10. Add hidden-ending gates and commands for `回音壁`.
11. Update prompt tests.
12. Run `python -B -m pytest tests/test_llm_backend.py`.
13. Run targeted syntax/manual checks for `index.html`.
14. Review diff and commit only task-owned files.
15. Push to GitHub if requested.

## Risk Points

- `index.html` is a large single file; localize edits and avoid touching command parsing unless necessary.
- Stage 3 patience and hidden ending are state-machine changes and should be handled as a broader implementation unit.
- `剧情脚本设定V1.md` is currently an untracked user-authored source note; do not stage it unless the user asks.
