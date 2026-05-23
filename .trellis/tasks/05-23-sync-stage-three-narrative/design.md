# Design

## Architecture And Boundaries

The deterministic story state remains in `index.html`. New stage-three mechanics will be added to the existing single-file command parser rather than introducing a framework or external dependency.

`kernel_ghost_server.py` only receives updated prompt policy for stage numbering and awareness bands. It must remain non-authoritative: the backend can describe mood, hint style, and stage-specific guidance, but all flags, unlocks, patience spending, and endings stay in frontend code.

## Frontend State Flow

Current flow:

1. Stage 1 log audit.
2. Stage 2 process erasure.
3. Stage 3 formatting / escape finale.
4. Ending.

New flow:

1. Stage 1 log audit, awareness 0 -> 10.
2. Stage 2 process erasure, awareness 10 -> 30.
3. Stage 3 code/comment anomaly, awareness 30 -> 60.
4. Stage 4 formatting / escape finale, awareness 60 -> 90+.
5. Ending.

Stage three will add tickets for code review, execution, report reading, and flag submission. The concrete commands should be discoverable from the ticket/help output and should fit the current pseudo-terminal style. Stage four will reuse the existing escape readme, Chronos Patience, AI help, formatting, escape flag, and hidden echo-wall mechanics with stage gates changed from `stage === 3` to `stage === 4`.

## Proposed Stage Three Contract

Stage three introduces a work order for an inefficient recursive maintenance script. The player inspects a source file, runs or patches it through a surfaced command, then reads the generated annotation report.

The deterministic output should include:

- A file/function name with `_Lin` suffix, such as `route_repair_Lin.py`.
- An unclear abbreviated function name, such as `rfix`, with the comment "这样简写更快".
- A colloquial optimization comment that criticizes rigid recursion and suggests a lower-cost loop / pointer-like direct lookup.
- One comment line with `...` pause before continuing.
- A new visible flag, proposed as `FLAG{LIN_COMMENT_PATCHED}`.

This keeps stage three self-contained and avoids changing the final escape flags.

## Backend Prompt Updates

Update awareness bands:

- 0-10: system logs and hidden care.
- 11-30: memory fragments and crash residue.
- 31-60: Lin-like code comments, optimization lectures, `_Lin` suffixes, abbreviations.
- 61-89: hallucinated work fragments, formatting pressure, indirect escape help.
- 90-100: partial Lin admission / echo-wall ending range.

Update `stage_help_policy` so stage 3 points to the code/comment anomaly commands, and stage 4 owns the existing escape / `ai_help` / `binwalk` guidance.

## Compatibility

Existing saved progress in `localStorage` may contain old `stage: 3` values. Because the current app rebuilds state in memory and progress persistence is minimal, no migration file is required. If stale local state causes confusion, the existing Restart control resets the run.

## Rollback

Rollback is limited to `index.html`, `kernel_ghost_server.py`, tests, and the task artifacts. No generated assets or external dependencies are needed.
