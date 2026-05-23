# Implementation Plan

1. Read current `index.html` state machine around initialization, command handling, stage transitions, rendering, and restart.
2. Add collection, relic, and intermission catalogs.
3. Extend state with intermission tracking and persistence-safe fields.
4. Implement storage helpers for active progress and durable collection.
5. Add terminal transcript serialization and restoration.
6. Add relic virtual files, `ls` directory entries, stage gates, and collection unlocks.
7. Add collection rendering grouped by type.
8. Add intermission modal DOM/CSS/JS and trigger it from stage transition results.
9. Ensure existing easter eggs unlock durable collection ids.
10. Validate syntax and tests:
    - JavaScript syntax check for inline script in `index.html`.
    - `python -m pytest`.
    - Browser console check through local/static page when feasible.
11. Commit code and task artifacts, then push to GitHub if remote authentication permits.

## Risk Points

- `applyResult()` ordering must persist state after async terminal rendering without losing user input state.
- Restart must clear progress but not collection.
- Intermission modal must not block ending modals or leave command input disabled.
- Existing hidden-ending gates must continue using `hiddenDiscoveries`.

## Review Gates

- Confirm no LLM path can unlock collection or choose events.
- Confirm all newly suggested readable paths have deterministic handlers.
- Confirm browser refresh behavior restores the current run without duplicating intro lines.
