# Implementation Plan

## Pre-Implementation

- [x] Confirm MVP scope decision with the user: offline H5 first, LLM integration later after testing.
- [x] Load `trellis-before-dev` and relevant frontend specs before editing app code.
- [x] Activate the task with `task.py start` only after planning approval.

## Build Checklist

- [x] Create `index.html` at repository root.
- [x] Define CSS design tokens, responsive shell layout, terminal output region, command input, work-order panel, status rail, and modal screens.
- [x] Add runtime fallback wrapper.
- [x] Implement initial state, restart, and optional local progress storage.
- [x] Implement terminal renderer and queued typewriter output without `scrollIntoView`.
- [x] Implement in-game operator name entry.
- [x] Implement command parser and deterministic engine.
- [x] Add Stage 1 content and flag progression.
- [x] Add Stage 2 content, process kill gate, crash report, and flag progression.
- [x] Add Stage 3 formatting / escape sequence content.
- [x] Add hidden discovery commands and discovery tracking.
- [x] Add both endings and restart from ending.
- [x] Add mobile ergonomics and reduced-motion handling.
- [x] Add concise in-game help and wrong-command feedback.
- [x] Leave a documented adapter boundary for future LLM integration without making network calls.

## Validation

- [x] Run a static search for forbidden offline-H5 patterns: external URLs, `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `alert`, `confirm`, `prompt`, `window.open`, `scrollIntoView`.
- [x] Open with browser automation and check console errors.
- [x] Play through Stage 1, Stage 2, hidden commands, and both endings.
- [x] Check desktop and mobile viewport screenshots for layout overlap.
- [x] Run `git status --short` and ensure only intended implementation files changed; unrelated pre-existing/user changes remain unstaged.

## Commit Plan

- [ ] Commit planning artifacts once approved if desired by workflow.
- [ ] Commit implementation after validation.
- [ ] Push to GitHub if remote access is configured and permitted by the environment.

## Risk Points

- Single-file JavaScript can become hard to maintain; keep data, engine, and renderer sections clearly separated.
- Typewriter queues can race with rapid input; disable command submission while output is streaming or queue commands predictably.
- Mobile terminal input can be cramped; keep touch targets at least 44px where possible.
- Hidden commands should not accidentally bypass main progression.
