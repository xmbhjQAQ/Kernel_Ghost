# Reduce Proactive AI Chatter

## Goal

Reduce Kernel-Mind proactive after-command replies so normal exploration does not feel like constant unsolicited commentary. Proactive AI should be rare and intentional.

## Requirements

- Normal allowed commands such as `ls`, `pwd`, successful `cd`, `whoami`, and ordinary file inspection must not trigger proactive LLM replies.
- Proactive LLM replies should trigger only when:
  - the player threatens Kernel-Mind safety or survival, such as `kill -9 777`, formatting, erasure, memory dumping, or related destructive actions;
  - the player appears lost through an invalid/disallowed command, premature command, wrong flag, or repeated random exploration;
  - a major story event explicitly requests LLM flavor through an existing `result.llm` block.
- Proactive replies must not proactively provide help for routine commands.
- If the player is lost, proactive output can nudge toward the current work-order area, but must remain sparse and in-universe.
- Backend prompt must reinforce that proactive mode should usually return empty content, especially for normal commands.

## Acceptance Criteria

- [ ] `ls` and normal successful navigation do not call proactive LLM.
- [ ] Invalid/disallowed commands can call proactive LLM with a "lost player" context.
- [ ] Threat commands can call proactive LLM with a "threat" context.
- [ ] Backend prompt says proactive mode is silent by default and must not offer routine help.
- [ ] Tests cover the stricter proactive prompt contract.
- [ ] Existing manual `ai_chat` and explicit story `result.llm` behavior remains unchanged.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
