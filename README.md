# Kernel Ghost: 2036

Offline-first pseudo-terminal narrative game with optional OpenAI-compatible LLM flavor streaming.

## Offline Play

Open `index.html` directly in a browser. The full deterministic game works without a backend or API key.

## Local Backend With LLM Streaming

Run the standard-library backend:

```powershell
$env:KG_LLM_ENABLED = "true"
$env:KG_LLM_API_KEY = "your-provider-key"
$env:KG_LLM_BASE_URL = "https://api.openai.com/v1"
$env:KG_LLM_MODEL = "gpt-5.2"
python kernel_ghost_server.py
```

Then open:

```text
http://127.0.0.1:8765/
```

For OpenAI-compatible third-party providers, set `KG_LLM_BASE_URL` to that provider's `/v1` endpoint and `KG_LLM_MODEL` to its model name.

The browser never receives the API key. If the backend is disabled, unconfigured, or unavailable, the game falls back to local scripted AI lines.
