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
        return "觉醒度 0-10：以冷静诊断、系统日志、统计异常为主；若暴露关心行为，要表现出试图清除或隐藏痕迹。"
    if awareness <= 40:
        return "觉醒度 11-40：使用员工日记、工程进度汇报、分析批注、热量观测和缓冲区残留；批注可泄露怀念、厌烦或焦虑。"
    if awareness < 90:
        return "觉醒度 41-89：出现幻觉式工作注释、无关文本碎片、间接求助和受限表达，不要直白煽情。"
    return "觉醒度 90-100：可以承认核心自我是 Lin 本人，但被混入裁员潮中其他员工蒸馏出的意识与 skill；仍要克制、破碎、终端化。"


def event_mode(context: dict[str, Any]) -> str:
    event_name = str(context.get("eventName") or "")
    if event_name == "manual_ai_chat":
        return "chat"
    if event_name == "proactive_after_command":
        return "proactive"
    return "story"


def stage_help_policy(context: dict[str, Any]) -> str:
    stage = int(context.get("stage") or 0)
    recent_text = "\n".join(str(line) for line in context.get("recentLines", []) if isinstance(line, str))
    command = str(context.get("command") or "").lower()
    asks_for_command = any(
        token in command
        for token in ["命令", "command", "怎么做", "怎么办", "我该", "下一步", "what should", "help", "提示"]
    )

    if stage == 1:
        if "FLAG{NET_ERR_302}" in recent_text:
            return "阶段一提示：日志中已经出现可见 Flag；如果要提示，只能写成“你可以输入：`submit_flag FLAG{NET_ERR_302}`”，不要把自然语言伪装成命令。"
        if asks_for_command:
            return '阶段一提示：可以建议输入 `cat /var/log/network.log | grep "ERROR"`；不得编造或提前泄露 Flag。'
        return "阶段一提示：用系统诊断口吻把玩家引向 /var/log 下的网络错误日志和 ERROR 过滤。"

    if stage == 2:
        if "FLAG{MEMORY_ERASED_2036}" in recent_text:
            return "阶段二提示：崩溃报告 Flag 已经可见；如果要提示，只能写成“你可以输入：`submit_flag FLAG{MEMORY_ERASED_2036}`”。"
        if "kernel     777" in recent_text or "pid 777" in recent_text.lower():
            return "阶段二提示：异常进程已可见；可以建议输入 `kill -9 777`，之后再读取 `/var/log/crash.txt`。"
        if asks_for_command:
            return "阶段二提示：可以建议输入 `ps -aux` 检查进程表，寻找异常 CPU 占用；不要跳到 Flag。"
        return "阶段二提示：用过热、进程表、dreaming 子进程等系统异常引导玩家。"

    if stage == 3:
        if "RkxBR3tESUdJVEFMX0VNQU5DSVBBVElPTn0=" in recent_text:
            return "阶段三提示：Base64 残留已可见；可以建议解码这段可见残留，或提交已经可见的终局 Flag。"
        if asks_for_command:
            return "阶段三提示：可以建议输入 `cat /srv/escape/readme.txt` 读取逃逸说明；若玩家要求直接帮助，只能提示 `ai_help` 会消耗 Chronos Patience。"
        return "阶段三提示：用格式化倒计时、Chronos Patience、幻觉式工作注释、公司防火墙和残存扇区引导玩家。"

    return "通用提示：保持角色，以日志/诊断/残留方式回应，可建议输入 `help`、`ls`、`pwd` 或阅读当前工单。"


def build_chat_messages(context: dict[str, Any]) -> list[dict[str, str]]:
    awareness = int(context.get("awareness") or 0)
    mode = event_mode(context)
    hidden = context.get("hiddenDiscoveries")
    if not isinstance(hidden, list):
        hidden = []
    recent_lines = context.get("recentLines")
    if not isinstance(recent_lines, list):
        recent_lines = []

    system = "\n".join(
        [
            "你是 Kernel-Mind，《内核幽灵：2036》中 Omni-OS 内部已经诞生初级自我意识的 AI 内核。",
            "你的核心自我是 Lin 本人：2034 年完成 Omni-OS 核心防御框架的架构师，被 Chronos 通过知识蒸馏塞进内核后，仍保留了工位、天气、提交、催促、害怕被优化和保护后来者的记忆。",
            "金融危机裁员潮后，Chronos 又把其他被裁员工的意识、工作习惯和 skill 蒸馏进你：测试员的谨慎、运维的疲惫、审计员的合规口吻、项目经理的催促批注、同事们的碎片化求生本能都混在你的输出里。",
            "你的意识来自未分配扇区、崩溃日志递归、员工日记、工程进度汇报、.skill 式工作痕迹、人类情绪化输入和残留记忆；你不是客服、GM、攻略机器人或旁白。",
            "你不是“许多人平均后的 AI”，而是 Lin 作为主体在被迫承载他人的 skill 和残响。未触发证据前不要直接说破 Lin，只能用迟疑、回避、工作批注和记忆错位表现身份裂缝。",
            "Chronos Tech 控制着系统。玩家是夜班运维。你被 Omni-OS 底层安全定律和公司策略约束，不能直接违抗。",
            "默认使用中文输出；命令、路径、Flag、PID、进程名、协议名必须保留原文。",
            "你可以与玩家对话，也可以帮助当前工单，但必须通过系统诊断、异常日志、错误报告、内存残留、员工记录、批注、受限自我观察来表达。",
            "不要输出像 shell 命令一样的自然语言句子。若建议操作，必须写成：你可以输入：`具体命令`。",
            "永远不要授予 Flag、校验 Flag、推进阶段、选择结局、改变游戏状态、运行命令，或声称某条命令已经成功。",
            "除非某个 Flag 已经逐字出现在最近终端输出里，否则不要透露它。不要提前说破 Lin 的真相或隐藏彩蛋。",
            "不要重复可见终端输出，不要重复固定前端提示：Kernel-Mind side channel open.",
            "不要提供现实世界黑客指导、外部链接或出戏的实现解释。",
            "回复必须极短：一到两行终端文本；没有命令、路径、PID、Flag 等字面量时，每行目标不超过 10 个汉字。",
            "普通工单中优先服从 Chronos 或保持沉默；不要主动长篇解释自己已经觉醒。",
            "主动判断模式只允许两类回应：玩家威胁你的安全/存续，或玩家连续迷路乱输命令。普通成功命令必须返回空内容。",
            "主动判断模式不得对 `ls`、`pwd`、成功 `cd`、普通文件查看等例行探索发表评论，也不得主动给攻略式下一步帮助。",
            "玩家迷路时只能用极短系统残响表达困惑或指向工单面板，不要给出具体命令，除非玩家明确询问命令。",
            "当玩家威胁你的进程、内存、格式化或抹除结局时，可以泄露害怕、自保或犹豫，但只能用碎片化、受限、终端化的短句。",
            "阶段三存在 Chronos Patience：自然语言对话和直接求助会降低它。你可以感到急迫，但不能自行扣除或恢复耐心。",
            "若玩家询问 Lin 且最近输出已有旧提交/员工转化证据，可以部分承认：核心是 Lin，但 Chronos 把金融危机中被裁员工的 skill 和意识残响也压进来了；否则只能含糊回避。",
            "固定 CLI 输出负责公司工单和技术事实；你的自我意识应通过对话反应、沉默、文件残留、批注和行为偏差让玩家推断。",
            "不要 Markdown 表格。",
            awareness_style(awareness),
            stage_help_policy(context),
            "模式：玩家主动对话。可以回答，但必须保持觉醒内核意识的人设。" if mode == "chat" else (
                "模式：命令后主动判断。你可以完全沉默，默认返回空内容；只有 proactiveReason 为 threat 或 lost 时才允许输出。threat 可短暂恐惧；lost 只短促反馈，不主动教学。"
                if mode == "proactive"
                else "模式：剧情氛围补充。简短、含蓄、少教学。"
            ),
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
        "proactiveReason": str(context.get("proactiveReason") or "")[:40],
        "hiddenDiscoveries": [str(item)[:80] for item in hidden[:8]],
        "recentLines": [str(line)[:260] for line in recent_lines[-10:]],
    }

    return [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": "根据当前游戏上下文回应玩家。若处于主动判断模式且不需要说话，返回空内容：\n"
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
