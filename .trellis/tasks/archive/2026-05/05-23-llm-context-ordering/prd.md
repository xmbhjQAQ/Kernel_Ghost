# Order LLM context for referential questions

## Goal

Improve Kernel-Mind LLM context ordering so referential player questions like
“这是什么东西？” resolve to the most recent concrete terminal output, especially
high-signal anomalies such as PID 777 / `kernel-mind --mode=dreaming`.

## Requirements

- Preserve the existing lightweight OpenAI-compatible backend and frontend flow.
- Send ordered command context, not only an undifferentiated recent terminal line
  slice, from the frontend to the backend.
- Identify recent anomaly candidates from visible terminal output, including PID
  / process / CPU / memory / RSS evidence.
- In backend prompt construction, make last command output and anomaly candidates
  higher priority than broad Kernel-Mind persona lore for referential questions.
- Keep responses constrained by existing game rules: no premature Flag disclosure,
  no state mutation, short terminal-style replies.

## Acceptance Criteria

- [x] `ai_chat 这是什么东西？` after `ps -aux` has structured context that points
      at PID 777 / `kernel-mind --mode=dreaming`.
- [x] Backend prompt includes explicit rules to answer “这/这个/什么意思” from
      the latest command output first.
- [x] Tests cover stage 2 process-audit context ordering and anomaly extraction.
- [x] Existing LLM backend tests pass.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
