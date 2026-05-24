# Plot Flowchart Overlay Design

## Architecture and Boundaries

Implement the feature inside the existing offline single-file frontend,
`index.html`.

Add three small frontend concepts:

- `plotRouteCatalog`: static route-map node definitions for main progression and
  endings.
- `plotArchive`: persisted cross-run knowledge of discovered route IDs and ending
  IDs.
- `renderPlotMap()`: derives the current visible route-map state from live
  `state`, persisted `plotArchive`, and the static catalog.

Do not add a backend endpoint or external asset. The route map must continue to
work when the game is opened as a standalone local H5 file.

## UI Shape

- Add a fixed route-map button below `#guideButton`.
- Add a dedicated modal, similar to the existing guidebook and encyclopedia
  modals.
- The modal renders a vertical route map:
  - onboarding / work-order spine
  - stage six branch point
  - visible named endings and hidden masked branches
- The active node is highlighted based on current `state.stage`,
  `state.ticket`, and `state.ending`.
- Locked undiscovered branches render title and description as `???`.

## Route Knowledge Contract

Route knowledge is separate from current-run progress:

- Current-run state can temporarily reveal a route when its prerequisites are
  met.
- Persisted route knowledge keeps that route named in later playthroughs.
- Normal restart preserves route knowledge.
- Full reset clears route knowledge.

Persisted object:

```json
{
  "version": 1,
  "routes": ["main", "company", "escape", "echo", "wildfire"],
  "endings": ["erasure", "emancipation", "echo", "wildfire"]
}
```

Unknown IDs must be filtered out on load.

## Discovery Rules

Known route IDs:

- `main`: known once gameplay starts or any stage is reached.
- `stage6`: known once stage six is reached.
- `company`: known once stage six is reached or erasure ending is reached.
- `escape`: known once stage six is reached or emancipation ending is reached.
- `echo`: known once the current run exposes the liberation branch
  (`askedLin` and `git-log`) or the echo ending is reached.
- `wildfire`: known once the black archive path is exposed through
  `distilled-index`, key derivation, archive decryption, or the wildfire ending.

Known ending IDs:

- Add the ending ID when `endingResult(kind)` is applied.

These rules intentionally reveal ordinary stage-six choices once the player
gets to the final branch, while keeping hidden routes masked until the player
has actually found their prerequisites.

## Data Flow

1. `initApp()` loads `plotArchive` from `localStorage`.
2. `renderState()` calls `updatePlotArchiveFromState()` and `renderPlotMap()`.
3. Command results mutate `state` through existing `applyResult()` flow.
4. Ending application persists the reached ending through the same archive
   update path.
5. `restartGame()` resets only current-run state; `plotArchive` remains.
6. `hardResetGame()` clears collection and plot archive state.

## Compatibility and Migration

Existing saves without plot archive load with an empty archive.

The new `localStorage` key should be independent from existing progress and
collection keys so old saves remain valid.

If `localStorage` is unavailable, keep an in-memory default and allow play to
continue, matching existing collection/progress behavior.

## Trade-Offs

The route-map catalog is intentionally static. Deriving it dynamically from the
command handlers would reduce duplication, but the existing game logic is not
structured as declarative route data. A static catalog is lower risk for this
single-file H5 and easier to test.

The map gives direction-level hints only. It should not list exact hidden route
commands, because the existing guidebook already owns spoiler walkthroughs.
