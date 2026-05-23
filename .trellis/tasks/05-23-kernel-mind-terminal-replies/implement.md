# Implementation Plan

## Checklist

1. Read frontend/backend specs and current task artifacts.
2. Start the Trellis task.
3. Update `kernel_ghost_server.py` prompt rules for short, threat-aware Kernel-Mind replies.
4. Update `index.html` deterministic Stage 1/2 copy to use concrete evidence instead of abstract consciousness labels.
5. Update backend tests for short-reply and threat-emotion prompt constraints.
6. Run targeted tests.
7. Check git diff to ensure unrelated deletions are not modified.
8. Commit and push this task's changes.

## Validation

- `python -m pytest tests/test_llm_backend.py`

If frontend text changes are substantial, also run a syntax check or lightweight browser/server check if available without adding dependencies.

## Risk Points

- `index.html` is a large single file; keep edits localized around known command handlers.
- Avoid changing deterministic stage progression or flag strings.
- Existing unrelated deletions are present in the working tree; do not stage them unless explicitly requested.
