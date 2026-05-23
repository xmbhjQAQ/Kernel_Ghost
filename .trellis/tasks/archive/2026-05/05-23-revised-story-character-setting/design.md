# Technical Design

## Architecture

- `index.html` remains the deterministic state machine and source of truth for commands, flags, stage transitions, hidden discoveries, and endings.
- `kernel_ghost_server.py` remains the LLM voice boundary. It can shape Kernel-Mind output but must not authorize game state changes.
- `tests/test_llm_backend.py` locks prompt contracts.

## Data Flow

```text
player command -> index.html command handler -> deterministic lines/patch -> optional LLM context -> kernel_ghost_server.py prompt -> non-authoritative flavor text
```

The revised setting should follow this split:

- deterministic CLI: work orders, command results, files, logs, patience/state if implemented;
- LLM: short in-character reactions, fear, hiding, indirect hints, hallucinated wording;
- system files: residue that supports the player interpretation.

## Main Path Updates

- Stage 1 replaces the current QAQ dictionary residue with the revised backlight/alarm sequence and a quick redaction/clear marker.
- Stage 2 updates `crash.txt` to contain repeated diary/progress fragments with analysis notes that become emotional.
- Stage 3 adds hallucinated work-comment texture in `readme.txt`, direct help, and Chronos pressure.

## Stage 3 Mechanics

- add `patience` to state;
- render patience in the status UI or ticket body;
- decrement on `ai_chat` during Stage 3;
- add a confirmation branch for direct AI help;
- add forced erasure when patience reaches zero;
- add hidden-ending state gates and new commands for gathering/publishing truth files.

The LLM never spends patience directly. Frontend deterministic command handling applies all patience changes before optional LLM flavor is requested.

## Compatibility

- Keep `FLAG{NET_ERR_302}`, `FLAG{MEMORY_ERASED_2036}`, `FLAG{AI_ERASURE_COMPLETE}`, and `FLAG{DIGITAL_EMANCIPATION}` unchanged.
- Keep existing hidden discovery commands unchanged.
- Do not stage unrelated existing dirty files unless explicitly requested.

## Rollback

Revert this task's edits in:

- `index.html`
- `kernel_ghost_server.py`
- `tests/test_llm_backend.py`
- `.trellis/tasks/05-23-revised-story-character-setting/*`
