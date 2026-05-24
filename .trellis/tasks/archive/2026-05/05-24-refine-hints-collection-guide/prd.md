# Refine hints collection archive and guide docs

## Goal

Reduce in-game answer leakage while improving post-discovery review and out-of-game documentation.

The game should not expose all stage commands or collectible names before the player discovers them. The external guide document may be fully explicit and should contain promotional story introduction, gameplay introduction, a novel-style story article, and a complete walkthrough for every ending, collectible, easter egg, encrypted archive, and other discoverable item.

## Confirmed Facts

- `helpResult()` in `index.html` currently lists commands for multiple later stages at once.
- `renderDiscoveries()`, `collectionHint()`, and `collectionStatus()` currently expose non-intermission collectible titles and availability details.
- Only found `Intermissions` can be clicked to reopen archive text.
- Collectible content already exists in data and command handlers:
  - relic content in `relicCatalog`
  - easter egg and puzzle output in command handlers / hidden discovery IDs
  - intermission text in `intermissionPools`
- `kernel_ghost_server.py` has `build_onboarding_messages()` for Brasch onboarding LLM prompt.
- `剧情文章与详细攻略.md` exists but is now outdated:
  - It describes an older four-stage story structure.
  - It does not cover the latest six work orders, new relics, easter eggs, puzzle archives, `回音壁` verification, or `燎原之火`.

## Requirements

- Help output must be stage-scoped:
  - Show only universal commands plus commands relevant to current screen/stage.
  - Do not list future-stage commands.
  - Avoid exact puzzle-answer command chains unless that command is already the active work-order instruction.
- Collection panel must hide undiscovered details for `Easter Eggs`, `Relics`, and `Puzzle Archives`:
  - Undiscovered title should be `???`.
  - Undiscovered hint/status should reveal at most whether the item exists yet for the current stage.
  - It should not reveal exact titles, paths, command names, or clue wording before discovery.
- Found non-intermission collectibles must be clickable like intermission archives:
  - Clicking a found relic/easter egg/puzzle archive should show an in-game archive modal.
  - The archive should summarize or replay the discovered content enough for review.
  - Undiscovered items must not be clickable.
- Brasch onboarding prompt must become harsher:
  - Reduce comforting language such as "理解".
  - Keep useful Linux training guidance.
  - Do not reveal gameplay answers or later-stage content.
- Update `剧情文章与详细攻略.md`:
  - Add promotional story introduction suitable for showing the game to players.
  - Add gameplay introduction explaining terminal play, work orders, collections, endings, and LLM assistance.
  - Rewrite or extend the story article in novel form to match the latest six-stage route.
  - Add detailed walkthrough covering every required main command.
  - Add detailed collection guide covering all currently implemented relics, easter eggs, puzzle archives, intermission events, and endings.

## Acceptance Criteria

- [ ] `help` at stage 1 does not show stage 3-6 commands.
- [ ] `help` at stage 6 may mention hidden evidence tools, but does not dump every solved command chain as a full answer list.
- [ ] Undiscovered non-intermission collectibles render with `???` as title.
- [ ] Undiscovered non-intermission collectibles reveal only existence status, not title/path/solution.
- [ ] Found relic/easter egg/puzzle archive entries can be clicked and opened in the archive modal.
- [ ] Found intermission archive behavior still works.
- [ ] Brasch prompt remains useful but becomes stricter and less soft in onboarding replies.
- [ ] `剧情文章与详细攻略.md` includes promotional intro, gameplay intro, novel-style story, and complete walkthrough.
- [ ] Tests cover stage-scoped help, hidden collection labels, clickable found collectibles, and Brasch prompt tone.
- [ ] Existing mainline endings and puzzle commands keep working.

## Out Of Scope

- Rewriting the core puzzle logic from the previous task.
- Adding new endings or collectibles beyond documenting the current implemented set.
- Designing new UI artwork.
- Changing the random intermission draw rules.

## Open Questions

None blocking. Use the current implemented game as source of truth for the guide.
