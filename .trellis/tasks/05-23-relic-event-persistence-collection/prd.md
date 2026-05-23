# 实现掉落物事件持久化收集系统

## Goal

Extend **Kernel Ghost: 2036** with collectible narrative content that supports player exploration across playthroughs:

- virtual CLI "relic" files from `掉落物系统.md`
- intermission events between tickets from `工单之间事件.md`
- local progress persistence so a browser refresh does not lose the current run
- a collection system that survives ending restart / next playthrough and records relics, easter eggs, and intermission events

## Confirmed Facts

- The app is an offline-first single-file H5 game in `index.html`.
- The deterministic frontend state machine owns commands, flags, stage transitions, hidden discoveries, patience, and endings.
- The optional backend/LLM must remain non-authoritative and should not unlock collectibles or mutate progress.
- Current hidden discoveries are only in memory: `git-log`, `lshw`, and `kmem`.
- Existing `restartGame()` clears `${storagePrefix}progress`; there is no durable run restore or meta-collection.
- `掉落物系统.md` defines 4 relic files and their discovery paths.
- `工单之间事件.md` defines 4 event pools, 5 events per pool, intended to appear after ticket completions / stage transitions.
- User asked for intermission event presentation as a modal similar to news, with title, content, sender, time, and confirm button.

## Requirements

1. Add the four relics from `掉落物系统.md` as deterministic virtual CLI files/commands.
2. Unlock relic collection entries the first time each relic is read.
3. Add intermission events after ticket completions:
   - after work order #001 completion: pool 1
   - after work order #002 completion: pool 2
   - after work order #003 completion: pool 3
   - during / after entering work order #004 before final resolution: pool 4
4. Render intermission events in a modal with title, sender/source, time, content, and a confirm action.
5. Add intermission events to the collection system when shown.
6. Keep existing easter eggs in the collection system and make them survive restarts.
7. Persist active run progress to `localStorage`, including enough state and terminal transcript to survive browser refresh.
8. Persist the meta-collection separately from active run progress, and do not clear it when the player restarts after an ending.
9. Preserve all existing deterministic command behavior, endings, and optional LLM constraints.
10. Keep the game playable by opening `index.html` directly.

## Acceptance Criteria

- [ ] Refreshing the page during an active run restores operator name, stage, ticket, cwd, state flags, discoveries, and visible terminal transcript.
- [ ] Restarting after an ending starts a new run but keeps the meta-collection.
- [ ] Reading each relic file unlocks a durable collection entry:
  - `/var/mail/chronos_hr_announcement`
  - `/home/lin/.bash_aliases.bak`
  - `/sys/kernel/debug/distill_loss.log`
  - `/var/log/operator_history.bak`
- [ ] Existing easter eggs `git-log`, `lshw`, and `kmem` appear as durable collection entries once discovered.
- [ ] Completing #001, #002, and #003 shows one intermission modal from the matching pool and stores it in the durable collection.
- [ ] Stage four can show one pool-4 intermission before final resolution and store it in the durable collection.
- [ ] The modal is keyboard-usable, dismissible through the confirm button, and does not overlap incoherently on mobile or desktop.
- [ ] Collection UI distinguishes locked and recovered entries without requiring players to inspect code.
- [ ] JavaScript syntax validation passes for `index.html`.
- [ ] Existing Python backend tests still pass.

## Out of Scope

- Adding new backend APIs or letting the LLM decide unlocks.
- External analytics, cloud sync, or server-side saves.
- Rewriting the app into a multi-file framework.
- Adding new story content beyond the supplied Markdown databases except for concise labels/metadata needed by UI.
