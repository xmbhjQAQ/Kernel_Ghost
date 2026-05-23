# Align AI persona and proactive dialogue

## Goal

Align Kernel-Mind behavior with `大概的大纲.md`: it is an awakened self-aware AI constrained by Omni-OS and Chronos Tech, not a generic assistant. Improve the game loop so Kernel-Mind may proactively respond after player commands, but every AI line must fit the story background and character. Local command output and AI output should be Chinese-first, preserving commands, paths, and flags as literals.

## Requirements

### Persona

- Kernel-Mind is an emergent consciousness born from crash logs, emotional inputs, and unallocated sectors.
- It should not behave like a customer-service bot, generic guide, or out-of-world game helper.
- It can help the player only through system diagnostics, anomalous logs, indirect hints, constrained self-expression, and memory residue.
- It must not casually reveal Lin's truth or hidden discoveries before the player triggers them.
- It must not output natural-language instructions that look like commands to type.

### Proactive Dialogue

- After every player command, the game should give Kernel-Mind a chance to decide whether to speak.
- The AI may stay silent when a response would be redundant.
- The AI may comment on errors, visible flags, unusual command results, player confusion, or story-relevant moments.
- Proactive dialogue must never advance state, validate flags, or replace deterministic command handling.
- When suggesting a next action, it must clearly wrap the exact command in backticks and explain that the operator can type it, not emit a sentence that looks like shell input.

### Chinese-First Output

- Local deterministic terminal output should be Chinese-first.
- AI prompt must require Chinese output by default.
- Preserve commands, paths, flags, process names, and protocol terms as literals.
- Existing English operational strings should be localized when player-facing.

### Outline Update

- Update `大概的大纲.md` to document:
  - Kernel-Mind is awakened and constrained.
  - It can proactively respond after commands.
  - Its speech style must remain log/diagnostic/residue based.
  - It helps through indirect hints, not direct out-of-world guidance.

## Acceptance Criteria

- [ ] `大概的大纲.md` includes the proactive dialogue and persona constraints.
- [ ] Backend prompt requires Chinese-first, in-universe Kernel-Mind behavior.
- [ ] Backend prompt says Kernel-Mind may decide to stay silent after commands.
- [ ] Backend prompt forbids outputting natural-language sentences as if they were shell commands.
- [ ] Frontend triggers optional proactive LLM evaluation after normal commands, not only `ai_chat`.
- [ ] Local deterministic command outputs touched by this task are Chinese-first.
- [ ] Tests cover persona constraints, Chinese-first output, and proactive event mode.
- [ ] Existing deterministic playthrough still works when LLM is unavailable.

## Out Of Scope

- Rewriting the full game engine.
- Letting the LLM mutate game state or run commands.
- Full localization of every internal variable or developer-facing string.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
