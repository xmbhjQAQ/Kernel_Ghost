# Kernel Ghost: 2036

Offline-first pseudo-terminal narrative game with optional OpenAI-compatible LLM flavor streaming.

## Offline Play

Open `index.html` directly in a browser. The full deterministic game works without a backend or API key.

## Local Backend With LLM Streaming

Run the standard-library backend:

```powershell
python kernel_ghost_server.py
```

Then open:

```text
http://127.0.0.1:8765/
```

Configure the model in `kernel_ghost_config.json`:

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

`kernel_ghost_config.json` is ignored by git so your API key is not committed.
For OpenAI-compatible third-party providers, set `baseUrl` to that provider's
`/v1` endpoint and `model` to its model name.

Environment variables such as `KG_LLM_API_KEY`, `KG_LLM_BASE_URL`, and
`KG_LLM_MODEL` still work and override the JSON file when present.

The browser never receives the API key. If the backend is disabled, unconfigured, or unavailable, the game falls back to local scripted AI lines.
