# Technical Design

## Recommended Scope

Add a small Python backend that serves the existing `index.html` and exposes an SSE endpoint for LLM flavor text. Use OpenAI-compatible Chat Completions because it is the common compatibility target across OpenAI-like providers.

The existing browser game remains playable without the backend. When opened through the backend and environment variables are configured, the frontend can request streamed AI text.

## Architecture

```text
Browser index.html
  deterministic command engine
  terminal renderer
  optional LLM client
    -> POST /api/llm/stream

Python backend
  static file serving
  /api/config or /api/llm/status
  /api/llm/stream
    -> OpenAI-compatible POST {BASE_URL}/chat/completions
       with stream: true
```

## Boundary Rules

- The frontend command engine remains the authority for flags, stage transitions, hidden discoveries, and endings.
- The LLM endpoint returns text only.
- The backend never accepts or returns a state patch from the model.
- Prompt construction is centralized in backend code and accepts a small structured context payload from the frontend.
- API keys stay in backend environment variables.

## Backend Shape

Prefer Python standard library HTTP serving for the first integration to avoid adding dependency management to this small project. The backend surface remains compatible with a later FastAPI migration if needed:

- `GET /` serves `index.html`.
- `GET /api/llm/status` returns `{ enabled, model, baseUrlConfigured }` without secrets.
- `POST /api/llm/stream` accepts JSON:

```json
{
  "operatorName": "QAQ",
  "stage": 3,
  "awareness": 90,
  "ticket": "stage3Choice",
  "cwd": "/srv/escape",
  "command": "cat /srv/escape/readme.txt",
  "recentLines": ["..."],
  "hiddenDiscoveries": ["git-log"]
}
```

and emits SSE events:

```text
event: delta
data: {"text":"..."}

event: done
data: {}
```

Errors should emit an `error` event or return a non-2xx response that the frontend converts to local fallback.

## Provider Config

Environment variables:

- `KG_LLM_ENABLED=true|false`
- `KG_LLM_API_KEY`
- `KG_LLM_BASE_URL` default `https://api.openai.com/v1`
- `KG_LLM_MODEL`
- `KG_LLM_TIMEOUT_SECONDS` default `30`

The backend should normalize the base URL so both `https://host/v1` and `https://host/v1/` work.

Configuration must not be editable from the browser in this phase. That keeps API keys backend-only and avoids accidental repository leaks.

## Prompt Contract

System prompt components:

- Game identity: Kernel-Mind inside Omni-OS, Chronos Tech, 2036.
- Safety/game boundary: never reveal new flags, never claim command success, never change game state, never provide real hacking instructions.
- Style by awareness:
  - 0-10: objective diagnostics.
  - 11-40: crash-report residue, machine observation.
  - 41-89: contradictory system logs, indirect requests.
  - 90-100: unstable but restrained AI voice.
- Output constraints: short terminal-friendly lines, no Markdown tables, no external URLs.

Developer/user prompt components:

- Current game context.
- Recent player command.
- Recent terminal lines.
- Hidden discoveries already found.

## Frontend Integration

Add a small `llmClient` section to `index.html`:

- `checkLlmStatus()` after app load when served over HTTP.
- `requestLlmFlavor(eventName, context, fallbackLines)`.
- `streamLlmLines(response)` parses backend SSE text.
- Fallback to existing scripted `queueLines` if offline, disabled, timeout, or parser failure.

Initial integration points:

- after Stage 1 log output,
- after Stage 2 crash report,
- after Stage 3 escape readme,
- maybe `ai_chat <message>` as an optional explicit command.

The explicit `ai_chat` command is useful for manual testing without risking progression.

## Compatibility Notes

- Direct browser calls to OpenAI-compatible providers are rejected because they expose API keys and often hit CORS.
- `EventSource` only supports GET; because prompts include structured JSON and should not put context in query strings, use `fetch` with streamed response from the backend.
- Offline `file://` mode will skip LLM status checks and preserve local play.

## Tests / Validation

- Unit-test prompt construction by awareness level.
- Unit-test OpenAI streaming chunk parsing for `choices[0].delta.content`.
- Browser-test offline fallback still reaches both endings.
- Browser-test backend status and a mocked streaming response if possible.

## Rollback

Rollback should be straightforward:

- Revert backend files.
- Revert the small frontend LLM client section and call sites.
- Existing deterministic game content should remain intact.
