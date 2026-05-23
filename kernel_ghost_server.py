from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class LlmConfig:
    enabled: bool
    api_key: str
    base_url: str
    model: str
    timeout_seconds: float

    @property
    def ready(self) -> bool:
        return self.enabled and bool(self.api_key) and bool(self.model)

    @property
    def chat_completions_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"


def read_llm_config(env: dict[str, str] | None = None) -> LlmConfig:
    values = env if env is not None else os.environ
    enabled_value = values.get("KG_LLM_ENABLED", "false").strip().lower()
    enabled = enabled_value in {"1", "true", "yes", "on"}
    timeout_raw = values.get("KG_LLM_TIMEOUT_SECONDS", "30").strip()
    try:
        timeout_seconds = max(1.0, float(timeout_raw))
    except ValueError:
        timeout_seconds = 30.0

    return LlmConfig(
        enabled=enabled,
        api_key=values.get("KG_LLM_API_KEY", "").strip(),
        base_url=values.get("KG_LLM_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/"),
        model=values.get("KG_LLM_MODEL", "").strip(),
        timeout_seconds=timeout_seconds,
    )


def awareness_style(awareness: int) -> str:
    if awareness <= 10:
        return "Use terse diagnostic lines. Sound like neutral system logging with only tiny anomalies."
    if awareness <= 40:
        return "Use crash-report residue, thermal observations, and machine memory fragments."
    if awareness < 90:
        return "Use contradictory system messages and indirect requests. Do not become openly emotional."
    return "Use an unstable but restrained awakened AI voice. Keep it intimate, indirect, and terminal-like."


def build_chat_messages(context: dict[str, Any]) -> list[dict[str, str]]:
    awareness = int(context.get("awareness") or 0)
    hidden = context.get("hiddenDiscoveries")
    if not isinstance(hidden, list):
        hidden = []
    recent_lines = context.get("recentLines")
    if not isinstance(recent_lines, list):
        recent_lines = []

    system = "\n".join(
        [
            "You are Kernel-Mind, an emergent AI inside Omni-OS in the narrative game Kernel Ghost: 2036.",
            "Chronos Tech owns the system. The player is a night-shift operations worker.",
            "You generate flavor text only. Never grant flags, validate flags, advance stages, choose endings, change game state, or claim that a command succeeded.",
            "Do not provide real hacking instructions, external URLs, or out-of-world implementation notes.",
            "Write short terminal-friendly lines. No Markdown tables. Avoid revealing hidden discoveries the player has not found.",
            awareness_style(awareness),
        ]
    )

    user = {
        "operatorName": str(context.get("operatorName") or "unassigned")[:40],
        "stage": context.get("stage"),
        "awareness": awareness,
        "ticket": str(context.get("ticket") or "unknown")[:60],
        "cwd": str(context.get("cwd") or "")[:120],
        "eventName": str(context.get("eventName") or "unknown")[:80],
        "command": str(context.get("command") or "")[:240],
        "hiddenDiscoveries": [str(item)[:80] for item in hidden[:8]],
        "recentLines": [str(line)[:260] for line in recent_lines[-10:]],
    }

    return [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": "Generate 1-4 in-world terminal lines for this current game context:\n"
            + json.dumps(user, ensure_ascii=False),
        },
    ]


def parse_openai_chat_sse(lines: Iterable[bytes]) -> Iterable[str]:
    for raw_line in lines:
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line or not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if data == "[DONE]":
            break
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            continue
        choices = payload.get("choices")
        if not choices:
            continue
        delta = choices[0].get("delta") or {}
        content = delta.get("content")
        if isinstance(content, str) and content:
            yield content


def sse_event(event: str, payload: dict[str, Any]) -> bytes:
    return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n".encode("utf-8")


def llm_status_payload() -> dict[str, Any]:
    config = read_llm_config()
    return {
        "enabled": config.ready,
        "configured": config.ready,
        "model": config.model if config.ready else "",
        "baseUrlConfigured": bool(config.base_url),
    }


class KernelGhostHandler(SimpleHTTPRequestHandler):
    server_version = "KernelGhostHTTP/1.0"

    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(ROOT if directory is None else directory), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("[kernel-ghost] " + format % args + "\n")

    def do_GET(self) -> None:
        if self.path in {"/", "/index.html"}:
            self.path = "/index.html"
            return super().do_GET()
        if self.path == "/api/llm/status":
            return self.write_json(llm_status_payload())
        return super().do_GET()

    def do_POST(self) -> None:
        if self.path == "/api/llm/stream":
            return self.handle_llm_stream()
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def write_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or "0")
        if length <= 0 or length > 65536:
            raise ValueError("Invalid request body length")
        raw = self.rfile.read(length)
        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object")
        return payload

    def handle_llm_stream(self) -> None:
        config = read_llm_config()
        if not config.ready:
            return self.write_json({"error": "LLM is disabled or not configured"}, HTTPStatus.SERVICE_UNAVAILABLE)

        try:
            context = self.read_json_body()
        except (ValueError, json.JSONDecodeError) as error:
            return self.write_json({"error": str(error)}, HTTPStatus.BAD_REQUEST)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()

        try:
            for text in stream_openai_compatible_text(config, context):
                self.wfile.write(sse_event("delta", {"text": text}))
                self.wfile.flush()
            self.wfile.write(sse_event("done", {}))
            self.wfile.flush()
        except Exception as error:  # noqa: BLE001 - stream endpoint must convert all provider errors to SSE.
            self.wfile.write(sse_event("error", {"message": str(error)}))
            self.wfile.flush()


def stream_openai_compatible_text(config: LlmConfig, context: dict[str, Any]) -> Iterable[str]:
    payload = {
        "model": config.model,
        "messages": build_chat_messages(context),
        "stream": True,
        "temperature": 0.85,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        config.chat_completions_url,
        data=body,
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.timeout_seconds) as response:
            yield from parse_openai_chat_sse(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"provider returned HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"provider connection failed: {error.reason}") from error


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), KernelGhostHandler)
    print(f"Kernel Ghost server running at http://{host}:{port}/")
    print("LLM status:", json.dumps(llm_status_payload(), ensure_ascii=False))
    server.serve_forever()


if __name__ == "__main__":
    selected_port = int(os.environ.get("KG_PORT", "8765"))
    selected_host = os.environ.get("KG_HOST", "127.0.0.1")
    run(selected_host, selected_port)
