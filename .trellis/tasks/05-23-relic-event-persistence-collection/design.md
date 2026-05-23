# Design

## Architecture

Keep `index.html` as the deterministic game authority. Add three data catalogs near the existing `discoveryCatalog`:

- `collectibleCatalog`: stable metadata for durable collection entries.
- `relicCatalog`: virtual file path, stage gate, terminal lines, and collection id.
- `intermissionPools`: event pools keyed by stage transition.

The active run state remains in `state`. The durable collection lives outside normal run state as `metaCollection`, loaded from and saved to `localStorage`.

## Storage Contracts

Use the existing prefix:

- `kernelGhost2036:progress` for active run state plus terminal transcript.
- `kernelGhost2036:collection` for durable collection unlock ids.

`progress` can be removed by restart. `collection` must not be removed by restart.

Persisted progress shape:

```json
{
  "version": 1,
  "state": {},
  "terminal": [{"kind": "system", "text": "..."}]
}
```

Persisted collection shape:

```json
{
  "version": 1,
  "unlocked": ["easter-git-log", "relic-hr-announcement", "event-1-3"]
}
```

On invalid JSON or schema mismatch, ignore the bad value and continue with a fresh run / empty collection.

## Data Flow

1. `initApp()` loads collection first, then tries to load active progress.
2. Command results may include `unlockCollectible` or `intermission`.
3. `applyResult()` applies deterministic patches, unlocks collection ids, persists progress, and opens intermission modals after terminal output.
4. Confirming an intermission closes the modal, records progress, and returns focus to the command input.
5. `restartGame()` clears only `progress`, resets run state, and re-renders the collection from `collection`.

## Relic Files

Integrate relics through `readVirtualFile()` and `listDirectory()` so absolute paths and relevant relative paths work where the current virtual directory supports them.

Stage gates:

- HR announcement and operator history: available from the start.
- Lin alias backup: available from stage 2 onward.
- distill loss log: available from stage 3 onward.

## Intermission Selection

Use deterministic pseudo-random selection based on operator name, pool id, and current collection size for a given run. If all events in a pool are already collected, still show a valid event but do not duplicate collection state.

This keeps the feature offline and repeatable enough for testing while encouraging multiple playthroughs to collect all variants.

## UI

Add an event modal separate from the intro and ending modals:

- Source/sender line
- Title
- Timestamp
- Preformatted content block
- Confirm button

Extend the existing discovery panel into a compact "collection" panel grouped by Easter Eggs, Relics, and Intermissions. Keep dense terminal-tool styling and avoid adding a marketing-like page.

## Compatibility And Rollback

Existing saves from before this feature are absent or incomplete; treat them as no save. Existing in-memory `hiddenDiscoveries` remains for branch logic, while collection unlocks mirror those discoveries.

Rollback is limited to `index.html` and this task directory. No backend migration is required.
