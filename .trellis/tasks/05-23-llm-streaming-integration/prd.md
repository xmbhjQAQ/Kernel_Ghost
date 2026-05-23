# Add LLM streaming integration

## Goal

Add OpenAI-compatible LLM streaming to **Kernel Ghost: 2036** without weakening the deterministic game engine. The model should provide in-world AI flavor text and dialogue that changes with awareness level, while command validation, stage progression, flags, and endings remain controlled by application code.

## Confirmed Facts

- Existing game entry: `index.html`.
- Existing game is a single-file offline H5 MVP with deterministic command handling and scripted terminal output.
- User confirmed this phase starts after offline testing passed.
- The LLM provider should be OpenAI-compatible, not locked only to OpenAI-hosted models.
- Official OpenAI API reference confirms Chat Completions supports `stream: true` for server-sent streaming responses at `/v1/chat/completions`.
- Official OpenAI docs recommend the newer Responses API for new OpenAI-only projects, but Chat Completions remains the broader compatibility surface for OpenAI-compatible third-party providers.
- Provider configuration decision: backend environment variables only. The browser must not provide or persist API keys.

## Requirements

### Gameplay / Product

- Preserve the existing complete offline playable path when no LLM backend is configured.
- Add an optional online mode where AI-flavored terminal lines stream from a backend LLM proxy.
- The LLM must not be able to grant flags, advance stages, alter hidden-discovery state, or choose endings.
- Awareness level must affect the LLM system prompt:
  - low awareness: terse diagnostic/system-log tone,
  - mid awareness: anomalous logs and observational residue,
  - high awareness: indirect, unstable, help-seeking AI voice.
- The model should receive enough game context to stay in-world: operator name, stage, awareness, current ticket, recent command, recent terminal context, and hidden discoveries.
- If the LLM request fails, times out, or is unconfigured, the game must fall back to scripted local output and remain playable.

### Technical

- Do not expose provider API keys in browser code.
- Add a backend endpoint that proxies an OpenAI-compatible Chat Completions streaming request.
- Backend config must support environment variables for:
  - API key,
  - base URL,
  - model,
  - timeout,
  - optional enable/disable flag.
- Frontend should consume the backend stream and render streamed text with the terminal output system.
- Keep deterministic command handling separate from probabilistic LLM generation.
- Add minimal run documentation for local development.
- Do not require a database or user accounts.

## Acceptance Criteria

- [ ] The existing offline path still works without backend or API key.
- [ ] Backend can be configured for an OpenAI-compatible `/v1/chat/completions` provider via environment variables.
- [ ] API keys are read only by the backend and are not present in `index.html`.
- [ ] Frontend can detect online LLM availability and show connection status.
- [ ] At least one AI interaction path streams text into the terminal from the backend.
- [ ] Stage/awareness context changes the backend prompt used for the model.
- [ ] LLM output cannot cause flag validation or state progression directly.
- [ ] Failed/unconfigured LLM calls produce a graceful in-world fallback, not a broken UI.
- [ ] Browser console has no errors in offline fallback and configured online mode.
- [ ] Backend has at least a basic validation/test path for prompt construction and streaming parser behavior.

## Out Of Scope

- Full migration to a database-backed game service.
- User login, cloud save, analytics, payment, or deployment automation.
- Rewriting the game in React/Vue.
- Letting the LLM execute tools or directly mutate game state.

## Open Questions

- None blocking implementation.

## Notes / Sources

- OpenAI Chat Completions API reference: https://platform.openai.com/docs/api-reference/chat/create-chat-completion
- OpenAI streaming guide/API references describe streaming model output using server-sent events.

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
