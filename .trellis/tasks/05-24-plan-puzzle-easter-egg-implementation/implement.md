# Implementation Plan: puzzle and easter egg design

## Current Status

- [x] Source design reviewed: `解密与彩蛋设计.md`.
- [x] Existing implementation anchors identified in `index.html`.
- [x] Requirements captured in `prd.md`.
- [x] Technical design captured in `design.md`.
- [x] User reviews and approves starting implementation.
- [x] Task is activated with `task.py start` before any game-code edits.

## Batch 0: Pre-Implementation Guardrail

Goal: make sure implementation starts from a clean enough understanding without touching unrelated dirty files.

Steps:

- [x] Review `git status --short` and identify unrelated user changes.
- [x] Read relevant `index.html` sections around catalogs, command dispatch, virtual files, state defaults, persistence, echo-wall, and flag submission.
- [x] Read `tests/test_frontend_context.py` and `tests/test_llm_backend.py`.
- [x] Confirm no new code blocks either simple endings:
  - `FLAG{AI_ERASURE_COMPLETE}`
  - `FLAG{DIGITAL_EMANCIPATION}`

Validation:

```bash
git status --short
python -m pytest tests/test_frontend_context.py tests/test_llm_backend.py
```

Review gate: if tests are already failing before implementation, record the baseline and avoid mixing unrelated fixes into this task.

## Batch 1: Low/Mid Collectible Expansion

Goal: increase exploration rewards without introducing the high-difficulty ending yet.

Status: completed in `index.html` with new relics, easter eggs, virtual paths, gated reads, and collection entries.

Likely files:

- `index.html`
- `tests/test_frontend_context.py`
- `tests/test_llm_backend.py` if hint/context strings change

Likely implementation anchors:

- `virtualDirectories`
- `collectibleCatalog`
- `relicCatalog`
- `readVirtualFile(expression)`
- `executeCommand(input)`
- save/load state defaults and whitelist logic
- collection panel rendering if group names change

Add planned relics:

- `Care-Bot 回滚样本`: `/srv/care/rollback_samples.log`
- `Nostalgia 权重快照`: `/srv/weights/snapshot.before_prune`
- `Lin 的代码评审习惯`: `/srv/review/lin_review_notes.txt`
- `黑档案索引残片`: `/srv/escape/distilled_metadata.index`

Add planned easter eggs:

- `retry_shadow 计数器`: `/srv/care/.retry_shadow`, gated by backdoor choice
- `雨声误报`: `/srv/weights/validator_noise.log`, gated by `Nostalgia=0.01` plus validator override
- `04:15 的热峰`: `/sys/kernel/debug/seat_thermal_404B12.csv`
- `被删掉的员工名册`: `/etc/chronos/staff_matrix.deleted`

Fairness requirements:

- Each new path appears in a directory listing or a fixed readable clue before it is required.
- Hidden files require `ls -a` only after output text has hinted a hidden counter or shadow file.
- Conditional files distinguish "wrong path" from "condition not met".

Manual checks:

- Direct relic file reads unlock their collection entries at or after the right stage.
- Premature reads return stage-aware feedback.
- `ls -a /srv/care` can reveal `.retry_shadow` after the correct route.
- `grep "404-B-12" /etc/chronos/staff_matrix.deleted` gives a meaningful result.
- Existing 7 collectibles still unlock as before.

Automated validation:

```bash
python -m pytest tests/test_frontend_context.py tests/test_llm_backend.py
```

Rollback point: if Batch 1 introduces instability, remove only new catalog entries, virtual files, and handlers. Do not touch main endings.

## Batch 2: 回音壁 Evidence Chain

Goal: make `回音壁` evidence-based and fair without making it as hard as `燎原之火`.

Status: completed with `verify_evidence --lin`, `verify_evidence --echo-wall`, specific missing-evidence feedback, and preserved echo-wall publishing commands.

Likely files:

- `index.html`
- frontend/backend context tests

Likely implementation anchors:

- `askLinQuestion()`
- `prepareEchoWall()`
- `publishEchoWall()`
- `executeCommand(input)`
- new `verifyEvidenceLin()` helper
- new `verifyEvidenceEchoWall()` helper
- collection unlock helper

Add or revise commands:

- `verify_evidence --lin`
- `verify_evidence --echo-wall`
- keep existing:
  - `mkdir /srv/echo-wall`
  - `cp /etc/kernel/.git /srv/echo-wall/lin.git`
  - `cp /dev/kmem /srv/echo-wall/kmem.dump`
  - `publish --global /srv/echo-wall`

Required `verify_evidence --lin` checklist:

- `old commit author`
- `physical seat match`
- `distillation-time hardware anomaly`

Required `verify_evidence --echo-wall` checklist:

- source history
- memory testimony
- optional operator-risk evidence

Acceptance behavior:

- Missing git evidence reports `missing: old commit author` or `missing evidence: source history`.
- Missing hardware evidence reports `missing: physical seat match`.
- Missing thermal evidence reports `missing: 04:15 hardware anomaly`.
- Missing kmem evidence reports `missing evidence: memory testimony`.
- `publish --global /srv/echo-wall` tells the player exactly which evidence category is missing.
- `回音壁` remains easier than `燎原之火` and does not require `Nostalgia=0.01`.

Manual checks:

- Player with only `git log` gets a direction toward memory testimony.
- Player with `git log` + kmem can publish the basic `回音壁`.
- Player with optional evidence gets richer ending copy or extra collectible, without making optional evidence mandatory.

Automated validation:

```bash
python -m pytest tests/test_frontend_context.py tests/test_llm_backend.py
```

Rollback point: preserve current echo-wall behavior if the richer evidence checklist is incomplete.

## Batch 3: 燎原之火 High-Difficulty Chain

Goal: implement the full hidden archive route with a clear key schema, derivation feedback, and segment-specific failure messages.

Status: completed with `distilled_metadata.index`, `distilled_metadata.encrypted`, `derive_key --from evidence`, `decrypt ... --key`, segment mismatch feedback, and a new `燎原之火` ending.

Likely files:

- `index.html`
- frontend/backend context tests

Likely implementation anchors:

- `executeCommand(input)`
- `readVirtualFile(expression)`
- state defaults and persistence merge
- ending registry or `submitFlag(flag)` depending on current ending structure
- `aiHelpFallbackLines()`
- new key/evidence helpers

Add commands:

- `derive_key --from evidence`
- `decrypt distilled_metadata.encrypted --key <key>`

Add file surfaces:

- `/srv/escape/distilled_metadata.index`
- `/srv/escape/distilled_metadata.encrypted`

Required key schema:

```text
seat-id:distill-time:retained-human-weight:weather-token
```

Expected key:

```text
404-B-12:0415:0.01:RAIN
```

Required route conditions:

- `Nostalgia=0.01` was preserved.
- Validator was overridden with an accepted reason.
- `雨声误报` was found.
- `黑档案索引残片` was found.
- At least two Lin evidence sources were found.
- Key is derived by evidence or entered correctly.

Failure behavior:

- Missing evidence in `derive_key --from evidence` returns a four-row checklist.
- Wrong key in `decrypt` reports segment-level mismatch:
  - seat-id
  - distill-time
  - retained-human-weight
  - weather-token
- Repeating escape-route commands should not accidentally unlock `燎原之火`.
- `ai_help` explains the evidence classes but should not reveal the full key before derivation.

Manual checks:

- A normal player can still finish `虚无的回响`.
- A normal player can still finish `赛博荒原的火种` with no harder than Base64.
- A hidden-route player can derive the key without leaving the game.
- Random intermission clues are helpful but not required to infer the schema.

Automated validation:

```bash
python -m pytest tests/test_frontend_context.py tests/test_llm_backend.py
```

Rollback point: if `燎原之火` is unstable, keep Batch 1 and Batch 2 while disabling only decrypt/ending registration for this route.

## Batch 4: Integrated Polish And Regression Pass

Goal: make the additions coherent as a game experience rather than isolated commands.

Status: completed with frontend/backend prompt tests and full pytest passing.

Checks:

- Collection panel locked hints give stage and clue class, not exact solution paths.
- All new D2+ puzzles have existence, direction, structure, fallback, and failure hints.
- Stage gating is consistent with the design document.
- The two simple endings remain reachable from a fresh save without hidden collectibles.
- Existing command aliases and old player habits still work.
- Save/load with older state does not throw or erase unrelated progress.

Validation:

```bash
python -m pytest
```

Manual playthrough matrix:

- Mainline company ending only.
- Mainline escape ending only.
- Basic `回音壁`.
- Enhanced `回音壁` with optional evidence.
- Full `燎原之火`.
- Partial hidden route with wrong key and missing evidence.

## Review Before Start

Before executing this plan, present this task to the user and ask for approval to start implementation. Task activation should happen only after approval:

```bash
python .\.trellis\scripts\task.py start .trellis\tasks\05-24-plan-puzzle-easter-egg-implementation
```

This planning task should then move from design into implementation mode.
