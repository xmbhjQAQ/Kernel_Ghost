# Implementation Plan

## Checklist

- [x] Activate the Trellis task after planning approval.
- [x] Load `trellis-before-dev` and relevant frontend/backend specs before editing.
- [x] Add stage-three tickets and state flags in `index.html`.
- [x] Implement deterministic stage-three commands and file/report outputs.
- [x] Change stage-two completion to awareness 30 and route to the new stage-three ticket.
- [x] Move existing formatting / escape / hidden echo-wall gates from stage 3 to stage 4.
- [x] Update help text, stage labels, ticket copy, hidden branch messages, and ending references.
- [x] Update `kernel_ghost_server.py` awareness style and `stage_help_policy`.
- [x] Update backend prompt tests for new stage numbering and awareness behavior.
- [x] Run validation:
  - `python -m pytest`
  - JavaScript syntax check for the inline script in `index.html`
  - Browser console smoke check against the local app.
- [ ] Commit and push changes to GitHub after successful verification.

## Risk Points

- Stage renumbering can silently break hidden branch gates if any `state.stage === 3` remains in formatting logic.
- Help output must surface every required command before the player needs it.
- LLM prompt tests currently assume stage 3 is the finale and awareness 40 belongs to stage-two memory fragments.

## Review Gates

- Search for `stage === 3`, `stage: 3`, and `阶段三` after edits.
- Search for `stage !== 3` in command gates and verify whether each should become stage 4 or remain stage 3.
- Confirm the new stage-three flag cannot be submitted before its report is visible.
