# Plan puzzle and easter egg implementation

## Goal

Turn `解密与彩蛋设计.md` into an executable implementation plan for the existing single-page game, without changing game code in this planning task.

The implementation plan must preserve the low-friction main endings while adding harder, fair, traceable puzzle routes for relics, easter eggs, `回音壁`, and `燎原之火`.

## Confirmed Facts

- Current implementation is concentrated in `index.html`.
- Current collectible scale is 7 known items:
  - 3 easter eggs: `git log`, `lshw -class processor`, `cat /dev/kmem | grep "REMAIN"`.
  - 4 relics: HR announcement, Lin aliases, distill loss log, operator history.
- Current hidden-ending flow already has `mkdir /srv/echo-wall`, `cp`, `publish --global /srv/echo-wall`, and basic `回音壁` handling.
- Current main endings are:
  - `虚无的回响`: `format --seal` then `submit_flag FLAG{AI_ERASURE_COMPLETE}`.
  - `赛博荒原的火种`: escape route with `FLAG{DIGITAL_EMANCIPATION}`.
- The source design requires a layered difficulty model:
  - D0/D1 for mainline and simple discovery.
  - D2/D3 for ordinary relics, easter eggs, and evidence chains.
  - D4 for full hidden truth and `燎原之火`.
- Intermission events are randomized, so they may provide existence and atmosphere hints but cannot be the only source of any required clue.

## Requirements

- Preserve mainline ending difficulty:
  - `虚无的回响` must stay direct and should not require puzzle solving.
  - `赛博荒原的火种` may require at most Base64-level decoding.
- Convert the new puzzle design into staged implementation batches.
- Each medium or hard puzzle must be explicitly "有迹可循":
  - existence clue
  - direction clue
  - structure clue
  - fallback clue
  - actionable failure feedback
- Keep one or two relics discoverable by direct file reading, so players learn exploration is rewarded.
- Add enough planned content to grow from 7 total collectibles toward:
  - 8 relics
  - 7 easter eggs
  - 4 puzzle archive or evidence-chain items
- Plan hidden-route work separately from simple collectible expansion:
  - low/mid collectible expansion
  - `回音壁` evidence verification
  - `燎原之火` key derivation and archive decryption
- Define validation expectations before implementation begins, including frontend context tests and command-flow checks.
- Do not require real cryptography or external tools outside the in-game terminal.

## Acceptance Criteria

- [x] `design.md` maps the requested puzzle additions to concrete implementation boundaries in `index.html`.
- [x] `design.md` states state-model, command parser, virtual filesystem, collection, ending, and LLM/backend impacts.
- [x] `implement.md` splits execution into ordered batches with review gates.
- [x] `implement.md` lists exact functions or data tables likely to change in each batch.
- [x] `implement.md` includes validation commands and manual playthrough checks for each batch.
- [x] The plan explicitly protects the two simple main endings from new hard prerequisites.
- [x] The plan explicitly prevents randomized intermissions from becoming the only required clue source.
- [x] This planning task ends with documentation only; no game-code changes are made until the user approves implementation.

## Out Of Scope

- Implementing the puzzle changes in `index.html`.
- Rewriting story prose beyond what is needed to identify implementation surfaces.
- Adding a backend service or real encryption library.
- Rebalancing unrelated UI layout, art direction, or stage scripts.

## Open Questions

None blocking. The current recommendation is to implement in three batches and ask for user review before starting code changes.
