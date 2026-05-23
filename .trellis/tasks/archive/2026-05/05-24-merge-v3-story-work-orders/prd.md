# Merge v3 story work orders

## Goal

Merge the expanded `kernel_ghost_2036_story_v3.md` flow into the playable game. The current playable flow has four work orders; v3 expands the mainline to six work orders by inserting AI semantic cleansing and model weight regression before the existing comment anomaly and final formatting sequence.

## Confirmed Facts

- `kernel_ghost_2036_story_v3.md` defines six work orders:
  - #001 routine network log audit.
  - #002 kill PID 777 and read the crash report.
  - #003 AI semantic cleansing of `Chronos-Care-Bot`.
  - #004 Collective Mind weight regression, including optional 1% Nostalgia preservation.
  - #005 comment anomaly review for `route_repair_Lin.py`.
  - #006 final formatting / escape / evidence endings.
- `index.html` currently owns the deterministic offline game state machine, virtual filesystem, work-order tickets, command handling, intermissions, endings, persistence, and frontend LLM context.
- `kernel_ghost_server.py` owns stage-aware LLM prompt policy and must stay aligned with frontend stage numbers.
- Tests exist for frontend source contracts in `tests/test_frontend_context.py` and backend LLM prompt behavior in `tests/test_llm_backend.py`.
- Existing unrelated/uncommitted user changes are present in the worktree and must not be reverted.

## Requirements

- Expand the playable work-order chain from four stages to six stages.
- Add deterministic commands, files, tickets, flags, and state transitions for:
  - Work order #003: read Care-Bot incident context, audit sandbox, choose compliance injection or hidden backdoor, submit `FLAG{CAREBOT_SANITIZED_2036}`.
  - Work order #004: read Collective Mind weight report, set Nostalgia to `0` or `0.01`, use validator override when preserving `0.01`, submit `FLAG{COLLECTIVE_MUTED_2036}`.
- Preserve the existing playable content for network audit, PID 777, comment anomaly, terminal escape, hidden discoveries, and endings, while renumbering comment anomaly to #005 and final choice to #006.
- Carry v3 narrative consequences into state where needed:
  - `sandbox --backdoor chronos-care` should record that a hidden audit backdoor exists.
  - preserving Nostalgia at `0.01` should record that the hidden ending / deeper evidence condition is available.
- Update frontend help text, stage labels, collection stage names, patience display, and stage-gated commands to match the six-stage flow.
- Update backend LLM stage policy so stage #003, #004, #005, and #006 describe the correct current work order.
- Update tests to catch the new stage mapping and prevent the previous four-stage numbering from drifting back.

## Acceptance Criteria

- [ ] A fresh playthrough can proceed deterministically through all six work orders and reach existing endings.
- [ ] Work order #003 exposes Care-Bot semantic cleansing commands and produces `FLAG{CAREBOT_SANITIZED_2036}` only after the required steps.
- [ ] Work order #004 exposes weight regression commands and produces `FLAG{COLLECTIVE_MUTED_2036}` only after the required steps.
- [ ] Work order #005 comment anomaly still works after renumbering.
- [ ] Work order #006 final escape / formatting / Lin hidden branch still works after renumbering.
- [ ] Frontend and backend stage numbers agree.
- [ ] Existing deterministic offline mode remains usable without a backend.
- [ ] Relevant tests pass.

## Out Of Scope

- Rewriting the full ending system beyond carrying the new v3 prerequisites.
- Adding new visual minigames for blind typing, flashing text, or hardware effects beyond deterministic terminal output.
- Replacing the existing intermission database.
- Reworking unrelated Trellis specs or user-created documents.

## Open Questions

- None blocking. The requested scope is to merge the v3-added work orders into the current playable flow.
