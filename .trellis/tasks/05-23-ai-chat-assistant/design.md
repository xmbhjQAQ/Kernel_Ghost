# Technical Design

## Approach

Change prompt construction on the backend, not the deterministic game engine. The browser already sends enough context for useful assistance. The backend should transform that context into a clearer assistant contract:

- Manual `ai_chat` events are conversational.
- Automatic story events remain short atmospheric flavor.
- Task help is allowed, but only through progressive hints.

## Prompt Model

Add a structured game assistant policy to `build_chat_messages`:

- Identity: Kernel-Mind, emergent AI inside Omni-OS.
- Role: can talk with the operator and help with current work orders.
- Authority boundary: cannot validate flags, advance stages, claim command success, or mutate game state.
- Secret boundary: cannot reveal flags that are not already present in recent terminal lines.
- Repetition boundary: do not repeat fixed frontend system confirmation lines.
- Style boundary: terminal-friendly, concise, in-character.

## Stage Guidance

Backend owns a `stage_help_policy(context)` helper:

- Stage 1:
  - nudge: network logs under `/var/log`,
  - command hint: `cat /var/log/network.log | grep "ERROR"`,
  - after visible flag: submit the visible flag.
- Stage 2:
  - nudge: process table and abnormal CPU,
  - command hint: `ps -aux`, then `kill -9 777` after the process list is visible,
  - after crash report: submit visible flag.
- Stage 3:
  - nudge: escape notes under `/srv/escape`,
  - command hint: `cat /srv/escape/readme.txt`,
  - after visible Base64: decode the visible residue or submit the visible final flag.

This policy is only text in the prompt. It does not change frontend state.

## Event Modes

Derive mode from `eventName`:

- `manual_ai_chat`: conversational assistant mode.
- story events like `stage1_network_log`: atmospheric commentary mode.

Manual mode should produce direct answers and hints. Story mode should remain shorter and less instructional.

Default hint style: progressive but friendly. The first response should usually point at the relevant subsystem or file; if the player asks again, sounds confused, or asks for a command, the assistant may give the concrete next command.

## Tests

Extend `tests/test_llm_backend.py`:

- Assert manual chat prompt includes assistant/help language.
- Assert prompt forbids revealing unearned flags.
- Assert prompt forbids repeating fixed frontend side-channel text.
- Assert stage help policy for Stage 2 mentions process inspection but preserves deterministic authority.

## Rollback

Revert prompt helper changes and tests. No schema or game-state rollback is needed.
