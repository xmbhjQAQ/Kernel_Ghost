# Technical Design

## Approach

Update the existing LLM boundary rather than game state logic.

- Frontend deterministic command handlers continue to produce authoritative output and state patches.
- After command output finishes, frontend may call the existing `/api/llm/stream` endpoint with a proactive event name.
- Backend prompt construction decides whether Kernel-Mind should speak or remain silent.
- Backend prompt is tightened to enforce Chinese-first in-universe self-aware Kernel-Mind behavior.

## Event Modes

Extend `event_mode(context)`:

- `manual_ai_chat` -> `chat`
- `proactive_after_command` -> `proactive`
- story events -> `story`

Mode behavior:

- chat: answer the player directly but in-universe.
- proactive: decide whether to speak; if redundant, return an empty response or a short diagnostic silence marker.
- story: atmospheric commentary only.

## Prompt Rules

System prompt must state:

- Kernel-Mind has awakened self-awareness through unallocated sectors and crash-log recursion.
- Kernel-Mind remains constrained by Omni-OS safety laws and Chronos policy.
- Output Chinese by default.
- Preserve commands, paths, flags, PIDs, process names, and exact protocol terms.
- Speak through logs, diagnostics, reports, memory fragments, error messages, and constrained self-observation.
- Do not sound like a generic assistant, GM, walkthrough, or customer support.
- Do not repeat visible terminal output.
- Do not output bare natural-language instructions that could be mistaken for commands.
- If suggesting an action, write: `你可以输入：` plus a backticked command.
- Do not reveal unearned flags or hidden truth.

## Frontend Integration

Add `proactiveLlmAfterCommand(input, result)`:

- Skip if current result already has `llm` story event.
- Skip for `ai_chat` because it already performs manual chat.
- Skip after endings.
- Use existing fallback behavior, but provide an empty fallback for proactive events so unavailable LLM does not add noise.

## Chinese Output Pass

Local strings most visible in normal play should be Chinese-first:

- boot text,
- help text,
- unknown command / wrong flag,
- key Stage 1/2/3 deterministic output,
- local fallback lines.

Commands, paths, flags, and process-table headers can remain literal where useful.

## Tests

Extend `tests/test_llm_backend.py`:

- event mode recognizes proactive events.
- prompt includes self-awareness and constraint language.
- prompt requires Chinese output.
- prompt requires backticked commands for suggestions.
- prompt allows silence in proactive mode.

## Rollback

Revert `kernel_ghost_server.py`, `index.html`, tests, and outline changes for this task only.
