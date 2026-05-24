# Plot flowchart overlay

## Goal

Add a player-facing plot flowchart control below the existing top-right
guidebook button so players can understand their current story route, see which
endings are reachable if they keep playing, and recognize locked routes without
spoiling their names or contents.

The feature should support the game's replay and collection loop without
turning into a full walkthrough.

## Confirmed Facts

- The main playable frontend is `index.html`, an offline single-page H5 game.
- A fixed top-right guidebook button already exists as `#guideButton` and opens
  the guidebook modal.
- Story progress is represented in frontend state, including `stage`, `ticket`,
  `completedFlags`, `hiddenDiscoveries`, `askedLin`, `nostalgiaPreserved`,
  `echoGitPacked`, `echoKmemPacked`, `linEvidenceVerified`,
  `operatorLoopVerified`, `distilledKeyDerived`, and
  `distilledArchiveDecrypted`.
- There are four implemented endings: `erasure`, `emancipation`, `echo`, and
  `wildfire`.
- The collection UI already masks undiscovered archive entries as `???`; this
  behavior is a useful precedent for masking locked plot routes.
- Progress and collection state are persisted in `localStorage`.
- The user confirmed that route/ending names should persist across playthroughs
  once discovered, because the feature is meant to help full-route completion.

## Requirements

- Add a compact control visually positioned below the existing top-right
  guidebook button.
- Opening the control shows a plot flowchart or route map, not just a flat text
  list.
- The map shows the player's current position in the story using current state.
- The map shows already unlocked or discovered routes/endings by name.
- Locked, undiscovered routes are masked as `???`.
- The map communicates what continuing from the current route can still unlock
  without exposing exact hidden-route commands or full spoilers.
- The route map must update as the player advances, discovers hidden evidence,
  unlocks route prerequisites, reaches an ending, restarts, or restores saved
  progress.
- Route and ending discovery should persist across normal restarts/new
  playthroughs.
- The full local reset action should clear persisted route/ending discovery
  together with progress and collection records.
- The feature must work offline with the existing single-file delivery shape.
- The feature must not break the existing guidebook, encyclopedia, collection,
  mobile ticket toggle, ending modal, or progress restore behavior.

## Acceptance Criteria

- [ ] A new top-right plot control appears below `#guideButton` on desktop and
  mobile without overlapping existing UI.
- [ ] Activating the control opens an accessible modal/panel with a visual route
  map.
- [ ] The route map highlights the active stage or ending.
- [ ] The route map shows the main progression from onboarding/work orders into
  stage six.
- [ ] The route map displays the company path and escape path when stage six is
  reached, and masks routes that are not yet unlocked as `???`.
- [ ] Hidden routes become named only after their relevant prerequisites or
  endings are discovered in state or previously persisted route history; before
  then, their name and description remain masked.
- [ ] Normal restart keeps previously discovered route/ending names visible,
  while full reset clears them back to `???`.
- [ ] The route map gives non-spoiler next-unlock hints based on current state.
- [ ] Restored saves render the same route-map state as live play.
- [ ] Tests cover route-map masking, current-position derivation, and modal
  event wiring.
- [ ] Existing frontend tests still pass.

## Open Questions

- None blocking.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
