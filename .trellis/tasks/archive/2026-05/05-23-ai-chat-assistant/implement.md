# Implementation Plan

## Pre-Implementation

- [x] Confirm default hint directness: progressive but friendly.
- [x] Load `trellis-before-dev` and relevant backend/frontend specs.
- [x] Activate task with `task.py start` after planning approval.

## Backend

- [x] Add `stage_help_policy(context)` helper.
- [x] Add `event_mode(context)` helper for manual chat vs story flavor.
- [x] Update `build_chat_messages` system prompt to allow chat and task help.
- [x] Add policy against repeating fixed frontend side-channel text.
- [x] Add policy against revealing unearned flags.
- [x] Keep deterministic authority restrictions.
- [x] Extend unit tests for chat assistant behavior.

## Frontend

- [x] Remove or soften duplicated fixed local `ai_chat` confirmation line if needed.
- [x] Keep fallback behavior for disabled/unconfigured LLM.
- [x] Keep existing stream renderer unchanged unless duplicate output still occurs.

## Validation

- [x] Run `python -m unittest tests.test_llm_backend`.
- [x] Run `python -m py_compile kernel_ghost_server.py tests\test_llm_backend.py`.
- [x] Verify `ai_chat` fallback still works without configured backend.
- [x] With backend/mock streaming, verify manual chat can render assistant response.
- [x] Ensure no API key strings are introduced into `index.html`.
- [ ] Commit and push changes.
