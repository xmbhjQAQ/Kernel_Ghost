# Quality Guidelines

> Code quality standards for backend development.

---

## Overview

<!--
Document your project's quality standards here.

Questions to answer:
- What patterns are forbidden?
- What linting rules do you enforce?
- What are your testing requirements?
- What code review standards apply?
-->

(To be filled by the team)

---

## Forbidden Patterns

<!-- Patterns that should never be used and why -->

(To be filled by the team)

---

## Required Patterns

<!-- Patterns that must always be used -->

## Scenario: Local LLM Configuration

### 1. Scope / Trigger

- Trigger: changing how `kernel_ghost_server.py` reads model provider settings.
- Applies to local backend LLM settings, API keys, provider base URLs, model
  names, and request timeouts.

### 2. Signatures

- Config file path: `kernel_ghost_config.json` at repository root.
- Tracked template: `kernel_ghost_config.example.json`.
- Reader signature: `read_llm_config(env=None, config_path=CONFIG_PATH)`.

### 3. Contracts

- JSON shape:
  - `llm.enabled: boolean`
  - `llm.apiKey: string`
  - `llm.baseUrl: string`
  - `llm.model: string`
  - `llm.timeoutSeconds: number`
- `kernel_ghost_config.json` must be git-ignored because it can contain an API
  key.
- Environment variables remain valid and override JSON values:
  - `KG_LLM_ENABLED`
  - `KG_LLM_API_KEY`
  - `KG_LLM_BASE_URL`
  - `KG_LLM_MODEL`
  - `KG_LLM_TIMEOUT_SECONDS`

### 4. Validation & Error Matrix

- Missing JSON config -> backend falls back to environment variables and safe
  disabled defaults.
- Invalid JSON -> ignored, same as missing config.
- Missing API key or model -> `ready == false`; browser falls back to scripted
  lines.
- Timeout below 1 second or invalid -> clamp/fallback to safe defaults.

### 5. Good/Base/Bad Cases

- Good: user edits local `kernel_ghost_config.json`, starts
  `python kernel_ghost_server.py`, and the API key never reaches the browser or
  git.
- Base: CI tests call `read_llm_config({}, config_path=None)` and get disabled
  defaults.
- Bad: committing a real provider key in a tracked config file.
- Bad: removing environment override support, breaking existing shell-based
  setup.

### 6. Tests Required

- Config-file read enables a ready LLM config.
- Environment values override JSON values.
- Invalid JSON is ignored without crashing the backend.

### 7. Wrong vs Correct

#### Wrong

```json
{"apiKey": "real-secret"}
```

Committed in a tracked file.

#### Correct

```json
{
  "llm": {
    "enabled": true,
    "apiKey": "your-provider-key",
    "baseUrl": "https://api.openai.com/v1",
    "model": "gpt-5.2",
    "timeoutSeconds": 30
  }
}
```

The real version lives in git-ignored `kernel_ghost_config.json`; the tracked
version is only `kernel_ghost_config.example.json`.

---

## Testing Requirements

<!-- What level of testing is expected -->

(To be filled by the team)

---

## Code Review Checklist

<!-- What reviewers should check -->

(To be filled by the team)
