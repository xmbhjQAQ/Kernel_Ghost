# Improve AI help guidance usability

## Goal

Make the stage 3 AI help flow understandable for first-time players and allow
players to request help more than once without getting stuck in a stale
confirmation state.

## Requirements

- Preserve the existing cryptic `project:` / `note:` puzzle output style.
- Use AI assistance output, not the base puzzle text, to explain those hints in
  more beginner-friendly terms.
- `confirm_ai_help` must be usable after each `ai_help` request; a completed
  confirmation should not block future help requests.
- Confirmed AI assistance should call the LLM when available; deterministic
  frontend output owns confirmation, patience cost, and offline fallback only.
- Manual `ai_chat` should answer simple greetings and identity questions
  directly instead of drifting into unrelated audit/residue flavor.
- Manual `ai_chat` should default to direct, useful answers for non-sensitive
  player questions. Evasive, fragmented, audit-like, or residue-like phrasing is
  reserved for sensitive subjects such as Lin identity, erasure, formatting,
  self-preservation, unrevealed Flags, or Chronos wrongdoing.
- Backend LLM configuration should be editable through a local JSON file so
  users do not need to set environment variables for normal local play.
- When help points to a command, make clear whether the command should be run
  directly or whether it is a hint about a hidden artifact.
- Preserve deterministic game-state ownership: the LLM must not spend patience
  or unlock endings.

## Acceptance Criteria

- [x] First `ai_help` then `confirm_ai_help` prints beginner-friendly guidance
      for the active stage 3 puzzle through LLM output or clear offline fallback.
- [x] A second `ai_help` after a confirmed help request opens a new confirmation
      instead of saying there is no pending request.
- [x] `confirm_ai_help` sends a dedicated LLM event when the backend is enabled.
- [x] Existing `project:` / `note:` puzzle lines remain available, while AI
      help can explain them.
- [x] `ai_chat 你好` and `ai_chat 你是谁？` have prompt rules that require a direct
      answer and forbid unrelated audit/residue filler.
- [x] Prompt rules clearly state direct-answer default for non-sensitive manual
      chat and define when evasive behavior is appropriate.
- [x] Backend reads `kernel_ghost_config.json` for LLM settings.
- [x] Environment variables remain supported as overrides.
- [x] A tracked example config documents the JSON shape while the real local
      config is ignored by git.
- [x] JavaScript syntax check passes.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
