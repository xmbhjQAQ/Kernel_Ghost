# Implementation Plan

## Pre-Implementation

- [x] Confirm provider configuration strategy with the user: backend environment variables only.
- [x] Load `trellis-before-dev` and relevant frontend/backend specs.
- [x] Activate task with `task.py start` after planning approval.

## Backend

- [x] Add minimal Python backend dependencies/config files if missing.
- [x] Implement environment-based LLM config loader.
- [x] Implement prompt builder with awareness-level style selection.
- [x] Implement OpenAI-compatible streaming client for `/chat/completions`.
- [x] Implement SSE endpoint `/api/llm/stream`.
- [x] Implement status endpoint that exposes only non-secret readiness.
- [x] Serve `index.html` through the backend for local testing.
- [x] Add focused tests for config, prompt builder, and stream chunk parser.

## Frontend

- [x] Add LLM status indicator to the existing side panel.
- [x] Add frontend LLM client using streamed `fetch` from backend.
- [x] Add safe fallback from LLM failure to scripted local lines.
- [x] Add `ai_chat <message>` optional command for explicit model interaction.
- [x] Hook LLM flavor calls into selected story moments without giving progression authority to the model.
- [x] Keep direct file-open offline behavior working.

## Validation

- [x] Run Python tests.
- [x] Run static scans to ensure no API key appears in frontend code.
- [x] Verify offline `index.html` playthrough still works without backend.
- [x] Verify backend-served game loads.
- [x] Verify LLM disabled/unconfigured mode gives graceful fallback.
- [x] If credentials are available, verify real streaming from configured provider. No real credentials were present; verified frontend streaming with mocked SSE instead.
- [x] Check browser console for errors.
- [ ] Commit and push changes after validation.

## Risk Points

- Streaming parsers often fail on split chunks; parser must buffer partial SSE frames.
- Provider-specific OpenAI-compatible APIs differ; keep payload conservative.
- Prompt injection from user commands must not affect deterministic game state.
- API key handling must stay backend-only.
