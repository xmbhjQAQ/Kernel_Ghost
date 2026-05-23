# Enhance AI chat assistant

## Goal

Upgrade `ai_chat` from a narrow flavor-text side channel into an in-character conversational assistant. Kernel-Mind should be able to chat with the player, answer story questions, and help the player complete current tasks with progressive hints while preserving deterministic game authority.

## Confirmed Facts

- Existing backend: `kernel_ghost_server.py`.
- Existing frontend: `index.html`.
- Current `ai_chat <message>` streams through `/api/llm/stream` when configured.
- Current prompt says the model generates flavor text only and must not change game state.
- Frontend sends the backend: operator name, stage, awareness, ticket, cwd, command, event name, hidden discoveries, and recent terminal lines.
- The user wants AI to chat with the player and help complete tasks.
- Product decision: default hint style is progressive but friendly. First help gives direction; follow-up help can provide a concrete command.

## Requirements

### Conversation

- `ai_chat <message>` should support natural back-and-forth conversation.
- Kernel-Mind should stay in-world: an emergent Omni-OS fragment under Chronos constraints.
- The assistant may answer questions about itself, the world, the current ticket, and what the player can inspect next.
- The assistant should avoid repeating the fixed frontend line: "Kernel-Mind side channel requested. Deterministic engine remains authoritative."

### Task Help

- The assistant may help the player complete the current stage.
- Help should be progressive:
  - first response: nudge toward the relevant area or concept,
  - follow-up request: suggest a concrete command,
  - only after the player has generated or seen a flag may it discuss submitting that visible flag.
- The assistant must not reveal unearned flags.
- The assistant must not claim a command succeeded, advance a stage, or override the deterministic engine.
- The assistant should explain wrong-command situations in-world when recent terminal output shows an error.

### Technical

- Update backend prompt construction to distinguish manual chat from automatic story flavor events.
- Add current ticket guidance to the prompt so the model knows how to help at each stage.
- Include a small hint policy in backend code rather than scattering it through frontend strings.
- Keep browser API-key safety unchanged.
- Add tests that enforce:
  - chat prompt allows helping,
  - unearned flag disclosure is forbidden,
  - duplicate fixed side-channel line is forbidden.

## Acceptance Criteria

- [ ] `ai_chat 你是谁` produces a conversational in-character answer, not only log fragments.
- [ ] `ai_chat 我该做什么` during Stage 1 can guide the player toward reading network logs.
- [ ] During Stage 2, the assistant can suggest using `ps -aux` or `kill -9 777` only as stage-appropriate help.
- [ ] During Stage 3, the assistant can nudge toward `cat /srv/escape/readme.txt` and decoding the visible Base64 residue without directly granting hidden state.
- [ ] Prompt tests verify the assistant can help but cannot reveal unearned flags or mutate game state.
- [ ] Existing deterministic playthrough and LLM fallback still work.

## Out Of Scope

- Letting the model run commands for the player.
- Model-side tool calls.
- Persistent long-term chat memory outside current browser session context.
- Changing flag validation or stage progression.

## Open Questions

- None blocking implementation.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
