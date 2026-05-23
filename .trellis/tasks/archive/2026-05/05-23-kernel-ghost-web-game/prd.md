# Build Kernel Ghost web game

## Goal

Build a playable web game based on `大概的大纲.md`: **Kernel Ghost: 2036**, a cyberpunk pseudo-CLI narrative puzzle game where the player handles company tickets, uncovers an emergent AI consciousness, discovers optional hidden truth fragments, and reaches one of two endings.

The first implementation should prioritize a complete, polished, locally runnable offline H5 MVP over a larger incomplete full-stack system. Real LLM integration is deferred until the offline version has been tested and accepted.

## Confirmed Facts

- Source concept: `大概的大纲.md`.
- Genre: narrative, pseudo-CLI terminal simulation, immersive lightweight CTF puzzle.
- Player fantasy: a Chronos Tech night-shift operations worker executing tickets in an Omni-OS terminal.
- Core loop: company work order gives explicit commands, the player runs commands, deterministic game state returns logs/flags, then the player submits the flag to advance.
- Main stages:
  - Stage 1: network log audit, `cat /var/log/network.log | grep "ERROR"`, flag `FLAG{NET_ERR_302}`.
  - Stage 2: process kill, `ps -aux`, `kill -9 777`, `cat /var/log/crash.txt`, flag `FLAG{MEMORY_ERASED_2036}`.
  - Stage 3: formatting / escape dilemma, AI instability, puzzle assistance, final dual ending.
- Optional hidden narrative commands:
  - `git log` under `/etc/kernel/`.
  - `lshw -class processor`.
  - `cat /dev/kmem | grep "REMAIN"`, emitting a Base64 truth fragment.
- Endings:
  - Ending A: submit `FLAG{AI_ERASURE_COMPLETE}`.
  - Ending B: submit `FLAG{DIGITAL_EMANCIPATION}`.
- The repository currently has no existing app framework; this task owns the app skeleton.
- Existing frontend spec has an active offline H5 contract, which fits a first playable game.
- Product scope decision: build the offline H5 version first; add OpenAI-compatible LLM streaming only after this version tests cleanly.

## Requirements

### Gameplay

- Provide an immediate playable terminal-like experience without a marketing or title-only page.
- Ask the player for an operator name at game start using in-game UI, not a browser prompt.
- Render a pseudo-terminal with:
  - command input,
  - command history,
  - streaming/typed output feel,
  - blinking cursor,
  - terminal log styling,
  - mobile-readable controls.
- Provide a persistent work-order panel or equivalent in-game guidance so non-Linux players know what to type next.
- Implement deterministic command handling for the main story commands and expected flags.
- Support graceful responses for unknown commands, wrong stage commands, and wrong flags.
- Track awareness level across story progression: 0%, 10%, 40%, 90%+.
- Make hidden commands optional and not required for normal completion.
- Track discovered hidden truth fragments and reflect them in later narrative or ending presentation.
- Implement both final endings and allow restart after an ending.

### Content

- Include the Stage 1, Stage 2, Stage 3, hidden truth, and dual-ending content from the outline.
- Keep the AI's consciousness indirect: system logs, crash reports, diagnostics, and anomalous machine wording should carry the emotion.
- Preserve the "company bright-line instruction + AI dark-line ambiguity" structure.
- Do not include external brand/IP assets.

### Technical / Delivery

- First version must be a local offline H5 app that can run from the workspace without needing a paid model key.
- Deliver an offline-first `index.html` H5 game.
- Use deterministic local state for command validation and progression.
- Keep future LLM integration behind a clear adapter boundary so the deterministic game engine remains authoritative when that later phase starts.
- Avoid browser-native `alert`, `confirm`, and `prompt`.
- Include a visible runtime error fallback instead of a blank page.
- Keep all resources local if implementing the offline H5 path.
- After code changes, commit changes to git as requested by the project instructions.

## Acceptance Criteria

- [ ] Opening the game shows the terminal experience and asks for the operator name in-game.
- [ ] A player can complete Stage 1 using the guided command and `FLAG{NET_ERR_302}`.
- [ ] A player can complete Stage 2 using `ps -aux`, `kill -9 777`, crash report reading, and `FLAG{MEMORY_ERASED_2036}`.
- [ ] A player can progress through Stage 3 and reach both endings via the two final flags.
- [ ] Optional hidden commands reveal the three hidden truth fragments without blocking main progression.
- [ ] Wrong commands and wrong flags produce useful in-world feedback without breaking state.
- [ ] Restart returns the game to a clean initial state.
- [ ] The UI is usable on desktop and mobile widths without incoherent text overlap.
- [ ] Browser console has no errors during a basic playthrough.
- [ ] If delivered as offline H5, `index.html` is at the root and contains no external network dependencies.
- [ ] Planning artifacts include `design.md` and `implement.md` before task activation.

## Out Of Scope For MVP

- Real OpenAI-compatible LLM calls in the critical path. LLM integration is a follow-up after offline MVP testing passes.
- User accounts, database persistence, leaderboard, multiplayer, or analytics.
- Real Linux command execution.
- A production FastAPI service unless explicitly chosen in the remaining scope decision.
- Audio, heavy images, or large external assets.

## Open Questions

- None blocking implementation. The offline-first MVP scope is confirmed.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
