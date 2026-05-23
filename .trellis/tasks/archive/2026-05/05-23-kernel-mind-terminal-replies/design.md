# Technical Design

## Boundaries

- `index.html` remains the deterministic game authority: command parsing, stage progression, flags, endings, and virtual file output.
- `kernel_ghost_server.py` remains the LLM boundary: it shapes Kernel-Mind's voice but cannot mutate game state.
- Tests in `tests/test_llm_backend.py` lock prompt contracts that are easy to regress.

## Narrative Contract

Fixed CLI output should represent Chronos and Omni-OS:

- company work orders,
- technical observations,
- files and logs,
- process table facts,
- deterministic flags and stage transitions.

Fixed CLI output should not narrate Kernel-Mind's self-awareness directly with labels such as "consciousness fragment" or "residual thread" before the player has evidence. Selfhood emerges through:

- Kernel-Mind `ai_chat` replies,
- proactive LLM behavior after commands,
- file/log/memory residue the player can inspect,
- threat reactions around destructive commands.

## Backend Prompt Changes

Add prompt rules:

- Reply in one or two short terminal-style lines.
- Target no more than 10 Chinese characters per line when no command/path/PID/Flag literal is needed.
- In ordinary operations, obey Chronos or remain silent.
- When the operator threatens destructive action against Kernel-Mind, show fear or self-preservation through fragments, hesitation, or system-constrained language.
- Keep existing non-authoritative restrictions: no state mutation, flag validation, unearned flags, ending choice, or real-world hacking advice.

Use context fields already passed by the frontend: `eventName`, `command`, `stage`, `recentLines`, and `awareness`. No schema migration is needed.

## Frontend Text Changes

Keep the early main path clear:

- Stage 1 network log: technical error lines plus concrete `QAQ` residue. Remove abstract "residual thread / consciousness fragment" declarations.
- Stage 1 after flag: close the work order, mention the next heat / process audit objective, avoid repeated "pulse" language.
- Stage 2 process list: Chronos can demand termination, but the extra flavor should be concrete process evidence.
- `kill -9 777`: add a short threat moment or file residue setup, then direct the player to the crash report.

The LLM unavailable fallback should stay quiet for proactive events so deterministic play remains clean.

## Compatibility

- Keep all commands, flags, paths, PID `777`, process name `kernel-mind --mode=dreaming`, and existing stage requirements unchanged.
- Do not require LLM availability for completion.
- Do not restore or alter unrelated deleted files currently present in the working tree.

## Rollback

Revert this task's edits in:

- `index.html`
- `kernel_ghost_server.py`
- `tests/test_llm_backend.py`
- `.trellis/tasks/05-23-kernel-mind-terminal-replies/*`
