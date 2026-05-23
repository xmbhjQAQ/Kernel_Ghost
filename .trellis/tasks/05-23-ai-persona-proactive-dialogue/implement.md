# Implementation Plan

## Pre-Implementation

- [x] Load `trellis-before-dev` and relevant backend/frontend specs.
- [x] Activate task with `task.py start` after planning approval.

## Backend

- [x] Extend `event_mode` with proactive mode.
- [x] Rewrite core system prompt to enforce awakened Kernel-Mind persona.
- [x] Add Chinese-first and command-format constraints.
- [x] Add proactive-mode instruction allowing silence.
- [x] Keep deterministic authority and unearned-flag restrictions.
- [x] Extend backend prompt tests.

## Frontend

- [x] Add proactive LLM calls after commands when appropriate.
- [x] Avoid proactive fallback noise when LLM is unavailable.
- [x] Chinese-localize key visible deterministic outputs.
- [x] Ensure command suggestions are not emitted as bare shell lines.

## Outline

- [x] Update `大概的大纲.md` with proactive dialogue and persona constraints.

## Validation

- [x] Run `python -m unittest tests.test_llm_backend`.
- [x] Run `python -m py_compile kernel_ghost_server.py tests\test_llm_backend.py`.
- [x] Browser-check unavailable LLM fallback still works.
- [x] Browser/mock-check proactive event can stream.
- [x] Verify no API key strings in `index.html`.
- [ ] Commit and push changes.
