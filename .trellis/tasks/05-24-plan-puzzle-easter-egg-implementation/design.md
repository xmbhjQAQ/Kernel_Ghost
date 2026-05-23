# Design: puzzle and easter egg implementation

## Scope

This design translates `解密与彩蛋设计.md` into implementation boundaries for the current static frontend. The work should stay inside the existing game architecture unless implementation reveals a strong reason to split files later.

No code is changed by this planning task.

## Existing Implementation Boundaries

Primary file:

- `index.html`

Important existing anchors:

- `virtualDirectories`: virtual filesystem listing surface.
- `discoveryCatalog`: maps hidden command discoveries to collectibles.
- `collectibleCatalog`: visible collection panel inventory.
- `relicCatalog`: direct file-read relic content.
- `readVirtualFile(expression)`: route file reads to virtual content and relic unlocks.
- `readGitLog()`, `readHardware()`, `readKmem()`: existing easter egg command handlers.
- `askLinQuestion()`: existing Lin identity dialogue branch.
- `prepareEchoWall()` and `publishEchoWall()`: current `回音壁` flow.
- `submitFlag(flag)`: mainline and ending submission gate.
- `stageLabel()`: stage-facing status label.
- `executeCommand(input)`: command parser dispatch.
- `aiHelpFallbackLines()`: fallback hint surface.

Tests currently exist under:

- `tests/test_frontend_context.py`
- `tests/test_llm_backend.py`

## Data Model Design

The implementation should keep content declarative where possible.

### Collectibles

Extend `collectibleCatalog` to include planned new IDs:

- Relics:
  - `relic-care-rollback-samples`
  - `relic-nostalgia-snapshot`
  - `relic-lin-review-notes`
  - `relic-distilled-metadata-index`
- Easter eggs:
  - `easter-retry-shadow`
  - `easter-rain-noise`
  - `easter-seat-thermal`
  - `easter-staff-matrix`
- Puzzle/evidence items:
  - `puzzle-lin-proof`
  - `puzzle-operator-seat-loop`
  - `puzzle-echo-wall-evidence`
  - `puzzle-distilled-archive`

Exact naming can change during implementation, but IDs should remain stable once shipped because persisted collection state filters unknown IDs during load.

### State

Add explicit booleans or compact state fields rather than inferring everything from prose output:

- `usedCareBackdoor`
- `preservedNostalgia`
- `overrodeValidator`
- `foundSeatThermal`
- `foundStaffMatrix`
- `foundRainNoise`
- `foundDistilledIndex`
- `linEvidenceVerified`
- `operatorLoopVerified`
- `distilledKeyDerived`
- `distilledArchiveDecrypted`

Reuse existing fields where they already represent the same condition, for example current nostalgia and echo-wall state.

### Persistence

Update the load/merge whitelist logic when adding new collectible IDs or state fields. New fields need safe defaults so old saves continue to load.

Compatibility rule: older saved games must not break, and unknown old fields should remain harmless.

## Virtual Filesystem Design

`virtualDirectories` should be updated so every planned path is discoverable from a nearby directory listing. Hard puzzles may require `ls -a`, `grep`, or stage gating, but the player must not need to guess an invisible path without a prior clue.

Planned file surfaces:

- `/srv/care/rollback_samples.log`
- `/srv/care/.retry_shadow`
- `/srv/weights/snapshot.before_prune`
- `/srv/weights/validator_noise.log`
- `/sys/kernel/debug/seat_thermal_404B12.csv`
- `/srv/review/lin_review_notes.txt`
- `/etc/chronos/staff_matrix.deleted`
- `/srv/escape/distilled_metadata.index`
- `/srv/escape/distilled_metadata.encrypted`

Each medium/hard file should include machine-readable fields in addition to story prose, for example:

- `seat_id=404-B-12`
- `distill_time=04:15`
- `retained_weight=0.01`
- `weather_token=RAIN`

## Command Surface Design

### Direct Reads

Use `readVirtualFile()` and `relicCatalog` for direct-read relics. Stage-gated premature reads should tell the player which system is not available yet.

### Existing Easter Egg Commands

Keep existing commands working:

- `git log`
- `lshw -class processor`
- `cat /dev/kmem | grep "REMAIN"`

Add stronger output fields where useful, but avoid changing their basic unlock behavior.

### New Exploration Commands

Support the design doc's intended operations through `executeCommand()`:

- `grep "404-B-12" /etc/chronos/staff_matrix.deleted`
- `grep "QAQ" /var/log/operator_history.bak`
- `strings /etc/chronos/staff_matrix.deleted` if needed
- `verify_evidence --lin`
- `verify_evidence --echo-wall`
- `derive_key --from evidence`
- `decrypt distilled_metadata.encrypted --key <key>`

If an operation is unsupported but likely from the puzzle design, return a useful in-world error instead of a generic unknown command.

### Evidence Verification

Verification commands should be the main fairness mechanism.

`verify_evidence --lin` should output checklist rows:

- old commit author
- physical seat match
- distillation-time hardware anomaly

`verify_evidence --echo-wall` should output checklist rows:

- `/srv/echo-wall/lin.git`
- `/srv/echo-wall/kmem.dump`
- optional operator-risk evidence

`derive_key --from evidence` should output four key segments with missing markers:

- seat-id
- distill-time
- retained-human-weight
- weather-token

## Ending Design

### Protected Main Endings

`submitFlag()` must keep these endings independent from hidden puzzles:

- `FLAG{AI_ERASURE_COMPLETE}`
- `FLAG{DIGITAL_EMANCIPATION}`

No new collectible, archive, or evidence condition should block them.

### 回音壁

Current echo-wall commands should be preserved, but evidence feedback should become more specific.

Required evidence:

- source history from `/etc/kernel/.git`
- memory testimony from `/dev/kmem` REMAIN residue

Optional strengthening:

- physical seat match
- operator history or staff matrix evidence

`publishEchoWall()` should list missing evidence by category rather than saying the package is incomplete.

### 燎原之火

Add as a separate high-difficulty hidden route, not a replacement for `回音壁`.

Required conditions:

- preserved `Nostalgia=0.01`
- validator override reason accepted
- `雨声误报` found
- `黑档案索引残片` found
- at least two Lin evidence sources found
- key derived or entered correctly

Key schema:

```text
seat-id:distill-time:retained-human-weight:weather-token
```

Expected key:

```text
404-B-12:0415:0.01:RAIN
```

The implementation can validate the key directly. Real encryption is optional and should not be required for the first version.

## Hint And Failure Design

Every D2+ puzzle must have:

- Existence clue in stage text, intermission, file title, or command output.
- Direction clue in a fixed, rereadable location.
- Structure clue in machine-readable fields or checklist output.
- Fallback clue in `ai_help` or related AI dialogue.
- Failure feedback naming the missing class or wrong segment.

Random intermission events may repeat or foreshadow clues, but required schema and progress information must live in fixed files or commands.

## LLM / Backend Impact

If the app has LLM-assisted hints, update prompt/context tests so the assistant knows:

- main endings remain simple
- `ai_help` may guide but should not directly reveal hidden-route keys unless the game state already derived them
- clue language should point to evidence classes, not external internet or real CTF tooling

If no backend behavior changes are needed, tests should still assert that new hintable surfaces are represented in frontend context.

## Compatibility And Rollback

Each batch should be reversible by removing only the newly added data entries, command handlers, and state fields from that batch.

Do not mix `燎原之火` with broad UI refactors. If hidden ending work becomes unstable, low/mid collectibles and `回音壁` improvements should remain shippable independently.
