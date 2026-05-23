# Fix terminal responsive layout

## Goal

Fix the terminal layout regression reported by the user: the command input row is no longer visible and the desktop browser layout no longer adapts to the full viewport width.

## Requirements

- Keep the command input visible at the bottom of the terminal on desktop.
- Restore desktop responsiveness so the game fills the available browser width instead of leaving a large unused black area.
- Preserve mobile stacking behavior.
- Avoid changing game logic or LLM behavior.

## Acceptance Criteria

- [ ] At desktop viewport, `.shell` width matches the available app width.
- [ ] At desktop viewport, `.input-row` is visible within the viewport.
- [ ] At mobile viewport, there is no horizontal overflow.
- [ ] Browser console has no errors after loading.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
