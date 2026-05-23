# Design

## Architecture And Boundaries

`index.html` remains the single deterministic game engine for offline play. The new work orders are added as new state-machine stages rather than a separate system, because existing tickets, virtual files, command handlers, flags, intermissions, and persistence all use `state.stage` as the source of truth.

`kernel_ghost_server.py` is updated only for LLM prompt policy. The backend does not advance gameplay state; it must describe the same stage numbers that the frontend sends in LLM context.

Tests stay source-level and contract-oriented, matching the current repository style.

## Frontend Data Flow

Player command -> `handleCommand()` -> stage-specific command function -> result patch / lines -> `applyResult()` -> persistence and optional LLM context.

New persistent state fields:

- `sawCareLog`, `ranCareAudit`, `cleansedCareBot`, `careBackdoor`
- `sawWeightReport`, `adjustedWeights`, `nostalgiaPreserved`, `overrodeValidator`

Stage transitions:

- #001 `FLAG{NET_ERR_302}` -> #002
- #002 `FLAG{MEMORY_ERASED_2036}` -> #003
- #003 `FLAG{CAREBOT_SANITIZED_2036}` -> #004
- #004 `FLAG{COLLECTIVE_MUTED_2036}` -> #005
- #005 `FLAG{LIN_COMMENT_PATCHED}` -> #006
- #006 existing final flags/endings

## Backend Prompt Contract

The frontend continues to send `stage` and recent terminal context. Backend policy maps:

- `stage == 3`: Care-Bot semantic cleansing.
- `stage == 4`: Collective Mind weight regression.
- `stage == 5`: comment anomaly / Lin coding habits.
- `stage == 6`: final formatting / escape / Chronos Patience.

The backend must not claim to mutate frontend state or reveal flags before deterministic terminal output has surfaced them.

## Compatibility

Restored saves may contain old stage numbers. This task does not attempt a full migration of old saves; the reset/restart path remains available. Persisted unknown fields are sanitized through existing restore logic.

## Tradeoffs

The v3 blind-typing and hardware-opposition ideas are represented as terminal logs rather than a new visual mechanic. This keeps the merge scoped and preserves offline deterministic play.

The `1% Nostalgia` condition is stored now so later hidden ending logic can use it, while the existing endings remain reachable.

## Rollback

The main rollback point is `index.html`. If the expanded state machine becomes unstable, revert the stage additions and backend stage remapping together; they must not be split.
