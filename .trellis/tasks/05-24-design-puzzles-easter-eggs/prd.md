# Design puzzles and easter eggs

## Goal

Design a richer puzzle, relic, and easter egg structure for `Kernel Ghost: 2036` without making the two simple mainline endings too difficult.

## Confirmed Facts

- Current game has 3 easter eggs:
  - `git log` in `/etc/kernel`
  - `lshw -class processor`
  - `cat /dev/kmem | grep "REMAIN"`
- Current game has 4 relics:
  - `/var/mail/chronos_hr_announcement`
  - `/home/lin/.bash_aliases.bak`
  - `/sys/kernel/debug/distill_loss.log`
  - `/var/log/operator_history.bak`
- Mainline endings should remain accessible:
  - `虚无的回响` should stay very easy.
  - `赛博荒原的火种` should be no harder than Base64.
- Harder puzzles should support hidden truth, full collection, `回音壁`, and `燎原之火`.
- Keep 1-2 collectibles as direct file-reading discoveries.

## Requirements

- Produce a design document for puzzle/easter egg expansion.
- Define puzzle difficulty tiers and intended player experience.
- Preserve low difficulty for simple endings.
- Expand relic/easter egg ideas beyond the current 7 items.
- Include direct-file finds, medium reasoning puzzles, and harder multi-step evidence-chain puzzles.
- For each proposed puzzle, specify:
  - stage availability
  - trigger / command surface
  - clue source
  - solve action
  - reward / collectible
  - story function
  - ending relevance

## Acceptance Criteria

- [ ] A Markdown design document exists in the repo.
- [ ] It distinguishes mainline, optional, hidden ending, and full-collection puzzles.
- [ ] It keeps `虚无的回响` and `赛博荒原的火种` low-friction.
- [ ] It includes at least 12 total relic/easter egg/puzzle concepts.
- [ ] It preserves at least 1-2 direct file-reading collectibles.

## Out Of Scope

- Implementing the puzzles in `index.html`.
- Changing existing ending logic.
- Rewriting current relic text.
