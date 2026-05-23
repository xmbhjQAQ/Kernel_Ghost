# Sync stage three narrative

## Goal

Update the playable Kernel Ghost H5 game so it follows `剧情脚本设定V2.md`, especially the newly inserted stage three: "注释异常" with awareness progression from 30% to 60%.

The player should experience the new stage as a deterministic terminal work order before the existing full-formatting / escape finale.

## Requirements

- Treat `剧情脚本设定V2.md` as the source of truth for the stage order:
  - Stage 1: routine log audit, awareness 0% -> 10%.
  - Stage 2: forced process erasure, awareness 10% -> 30%.
  - Stage 3: code/comment anomaly, awareness 30% -> 60%.
  - Stage 4: full formatting / escape finale, awareness 60% -> 90%+.
- Insert a new playable stage three in `index.html` after `FLAG{MEMORY_ERASED_2036}` and before the current escape readme / Chronos Patience flow.
- Stage three must have a company work order, at least one concrete command path, and a submit step consistent with the current deterministic terminal style.
- Stage three output must show:
  - AI-provided inefficient code or task material.
  - Extra colloquial optimization comments after execution.
  - Lin-like naming habits including unclear abbreviations and `_Lin` suffixes.
  - A brief `...` pause in one system/comment line to evoke Lin organizing a lecture.
- Update stage labels, tickets, help text, gating, endings, hidden branch requirements, and LLM context wording so "stage three" no longer refers to the formatting finale.
- Preserve deterministic game-state ownership: LLM output can add flavor only and must not unlock flags, spend patience, or choose endings.
- Keep the app offline-first: opening `index.html` directly must still run the full deterministic game.

## Acceptance Criteria

- [ ] Completing stage two advances to the new stage three, not directly to the formatting finale.
- [ ] The new stage three is playable via surfaced commands and advances only after its own visible Flag is submitted.
- [ ] Awareness values align with V2: stage two completion reaches 30%, stage three completion reaches at least 60%, and stage four reaches the existing high-awareness finale range.
- [ ] Existing stage four mechanics still work after renumbering: `ai_help`, `confirm_ai_help`, `format --seal`, `binwalk architecture.png`, escape Flag submission, hidden `你是Lin吗？` branch, and echo-wall publishing.
- [ ] Help text and ticket copy use the correct stage numbers and do not mislabel formatting as stage three.
- [ ] Backend LLM prompt tests are updated where they assert stage numbering, awareness bands, or stage help policy.
- [ ] JavaScript syntax validation, backend tests, and a browser console smoke check pass.

## Notes

- Existing dirty worktree before this task included deleted `.trellis/spec/frontend/interactive-space-h5.md`, deleted `大纲.md`, and untracked `剧情脚本设定V1.md` / `剧情脚本设定V2.md`. Do not revert unrelated user changes.
- `.trellis/spec/frontend/index.md` references `interactive-space-h5.md`, but that file is currently deleted in the worktree, so the active usable frontend spec is `quality-guidelines.md`.
