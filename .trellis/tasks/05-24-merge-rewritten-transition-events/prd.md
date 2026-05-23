# Merge rewritten transition events

## Goal

Merge `过渡事件（重写）.md` into the playable intermission system so each transition between work orders #001-#006 has a five-event random pool aligned with the rewritten narrative.

## Requirements

- Replace the current intermission event copy in `index.html` with the rewritten transition event pools.
- Preserve the existing mechanic: after each eligible work order, randomly select one event from that transition pool and archive it as a collectible.
- Support five transition pools:
  - #001 -> #002
  - #002 -> #003
  - #003 -> #004
  - #004 -> #005
  - #005 -> #006
- Do not add a normal intermission after #006; endings remain responsible for final narrative closure.
- Keep event text long-form. The UI may show long text; no compression is required for this task.
- Keep existing unrelated dirty worktree files untouched.

## Acceptance Criteria

- [ ] `index.html` contains five intermission pools with five events each.
- [ ] The existing transition logic can trigger pools 1-5 after work orders #001-#005.
- [ ] The new events use the rewritten document's themes and text.
- [ ] Collection/archive metadata still works for intermission events.
- [ ] Frontend source tests cover the five-pool shape.
- [ ] Validation passes.
