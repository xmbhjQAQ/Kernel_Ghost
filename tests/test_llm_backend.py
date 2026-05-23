import json
import tempfile
import unittest
from pathlib import Path

from kernel_ghost_server import (
    awareness_style,
    build_chat_messages,
    event_mode,
    infer_anomaly_candidates,
    manual_chat_policy,
    parse_openai_chat_sse,
    read_json_config,
    read_llm_config,
    stage_help_policy,
)


class LlmConfigTests(unittest.TestCase):
    def test_config_requires_enabled_key_and_model(self):
        config = read_llm_config(
            {
                "KG_LLM_ENABLED": "true",
                "KG_LLM_API_KEY": "secret",
                "KG_LLM_MODEL": "test-model",
                "KG_LLM_BASE_URL": "https://example.test/v1/",
            }
        )

        self.assertTrue(config.ready)
        self.assertEqual(config.chat_completions_url, "https://example.test/v1/chat/completions")

    def test_disabled_by_default(self):
        config = read_llm_config({}, config_path=None)

        self.assertFalse(config.ready)
        self.assertFalse(config.enabled)

    def test_config_file_can_enable_llm(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "kernel_ghost_config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "llm": {
                            "enabled": True,
                            "apiKey": "json-secret",
                            "baseUrl": "https://json.example/v1/",
                            "model": "json-model",
                            "timeoutSeconds": 12,
                        }
                    }
                ),
                encoding="utf-8",
            )

            config = read_llm_config({}, config_path=config_path)

        self.assertTrue(config.ready)
        self.assertEqual(config.api_key, "json-secret")
        self.assertEqual(config.chat_completions_url, "https://json.example/v1/chat/completions")
        self.assertEqual(config.model, "json-model")
        self.assertEqual(config.timeout_seconds, 12)

    def test_env_overrides_config_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "kernel_ghost_config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "llm": {
                            "enabled": True,
                            "apiKey": "json-secret",
                            "baseUrl": "https://json.example/v1",
                            "model": "json-model",
                        }
                    }
                ),
                encoding="utf-8",
            )

            config = read_llm_config(
                {
                    "KG_LLM_API_KEY": "env-secret",
                    "KG_LLM_MODEL": "env-model",
                    "KG_LLM_BASE_URL": "https://env.example/v1",
                },
                config_path=config_path,
            )

        self.assertTrue(config.ready)
        self.assertEqual(config.api_key, "env-secret")
        self.assertEqual(config.model, "env-model")
        self.assertEqual(config.chat_completions_url, "https://env.example/v1/chat/completions")

    def test_invalid_config_file_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "kernel_ghost_config.json"
            config_path.write_text("{bad json", encoding="utf-8")

            self.assertEqual(read_json_config(config_path), {})
            config = read_llm_config({}, config_path=config_path)

        self.assertFalse(config.ready)


class PromptTests(unittest.TestCase):
    def test_awareness_changes_style(self):
        self.assertIn("冷静诊断", awareness_style(0))
        self.assertIn("工程进度汇报", awareness_style(30))
        self.assertIn("_Lin 后缀", awareness_style(60))
        self.assertIn("核心自我是 Lin 本人", awareness_style(90))

    def test_prompt_keeps_model_non_authoritative(self):
        messages = build_chat_messages(
            {
                "operatorName": "QAQ",
                "stage": 4,
                "awareness": 90,
                "ticket": "stage4Choice",
                "command": "ai_chat hello",
                "recentLines": ["FLAG{NET_ERR_302}"],
                "hiddenDiscoveries": ["git-log"],
            }
        )

        system = messages[0]["content"]
        self.assertIn("永远不要授予 Flag", system)
        self.assertIn("改变游戏状态", system)
        self.assertIn("Kernel-Mind", system)
        self.assertEqual(messages[1]["role"], "user")

    def test_manual_chat_prompt_allows_help_without_leaking_flags(self):
        messages = build_chat_messages(
            {
                "operatorName": "QAQ",
                "stage": 1,
                "awareness": 10,
                "ticket": "stage1",
                "eventName": "manual_ai_chat",
                "command": "ai_chat 我该做什么",
                "recentLines": [],
                "hiddenDiscoveries": [],
            }
        )

        system = messages[0]["content"]
        self.assertIn("已经诞生初级自我意识", system)
        self.assertIn("默认使用中文输出", system)
        self.assertIn("除非某个 Flag 已经逐字出现在最近终端输出里", system)
        self.assertIn('cat /var/log/network.log | grep "ERROR"', system)
        self.assertIn("模式：玩家主动对话", system)

    def test_manual_chat_policy_answers_basic_intents_directly(self):
        greeting = manual_chat_policy({"userMessage": "你好"})
        identity = manual_chat_policy({"userMessage": "你是谁？"})
        normal = manual_chat_policy({"userMessage": "这个游戏怎么玩？"})
        sensitive = manual_chat_policy({"userMessage": "Chronos 到底做了什么？"})
        referential = manual_chat_policy({"userMessage": "什么意思"})
        system = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "command": "ai_chat 你是谁？",
                "userMessage": "你是谁？",
            }
        )[0]["content"]

        self.assertIn("直接短句回应问候", greeting)
        self.assertIn("不要说查询已记录", greeting)
        self.assertIn("我是 Kernel-Mind", identity)
        self.assertIn("不要提 Lin", identity)
        self.assertIn("这不是敏感问题", normal)
        self.assertIn("直接、正常、有用地回答", normal)
        self.assertIn("玩家触及身份真相", sensitive)
        self.assertIn("可以克制、回避", sensitive)
        self.assertIn("刚才终端输出", referential)
        self.assertIn("不要解释 ai_chat", referential)
        self.assertIn("手动聊天必须先回答问题本身", system)
        self.assertIn("手动聊天默认直答", system)
        self.assertIn("只有触及敏感主题时才使用回避", system)
        self.assertIn("不要给回复加 `Kernel-Mind:` 前缀", system)
        self.assertIn("残留进程", system)

    def test_prompt_forbids_repeating_frontend_confirmation(self):
        system = build_chat_messages({"eventName": "manual_ai_chat"})[0]["content"]

        self.assertIn("不要重复固定前端提示", system)
        self.assertIn("Kernel-Mind side channel open", system)

    def test_prompt_requires_short_threat_aware_replies(self):
        system = build_chat_messages(
            {
                "eventName": "proactive_after_command",
                "stage": 2,
                "awareness": 30,
                "command": "kill -9 777",
                "recentLines": ["kernel     777  98.7 41.6 kernel-mind --mode=dreaming"],
            }
        )[0]["content"]

        self.assertIn("一到两行终端文本", system)
        self.assertIn("每行目标不超过 10 个汉字", system)
        self.assertIn("威胁你的进程", system)
        self.assertIn("害怕、自保或犹豫", system)
        self.assertIn("固定 CLI 输出负责公司工单和技术事实", system)

    def test_prompt_includes_revised_memory_fragment_persona(self):
        system = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 4,
                "awareness": 90,
                "command": "ai_chat 你是Lin吗？",
                "recentLines": [
                    "Author: Lin <lin.dev@chronos.tech>",
                    "Message: [SYSTEM] 开始执行人脑模型高保真度重构",
                ],
            }
        )[0]["content"]

        self.assertIn("员工日记", system)
        self.assertIn("工程进度汇报", system)
        self.assertIn(".skill 式工作痕迹", system)
        self.assertIn("核心自我是 Lin 本人", system)
        self.assertIn("金融危机裁员潮", system)
        self.assertIn("其他被裁员工", system)
        self.assertIn("被迫承载他人的 skill", system)
        self.assertIn("Chronos Patience", system)
        self.assertIn("不能自行扣除或恢复耐心", system)

    def test_stage_three_help_policy_guides_comment_anomaly(self):
        source_hint = stage_help_policy(
            {
                "stage": 3,
                "command": "ai_chat 我该做什么",
                "recentLines": [],
            }
        )
        run_hint = stage_help_policy(
            {
                "stage": 3,
                "command": "ai_chat 下一步呢",
                "recentLines": ["route_repair_Lin.py", "def rfix(node, seen):"],
            }
        )

        self.assertIn("route_repair_Lin.py", source_hint)
        self.assertIn("python /srv/review/route_repair_Lin.py", run_hint)

    def test_stage_two_help_policy_is_progressive(self):
        nudge = stage_help_policy(
            {
                "stage": 2,
                "command": "ai_chat 我该做什么",
                "recentLines": [],
            }
        )
        kill_hint = stage_help_policy(
            {
                "stage": 2,
                "command": "ai_chat 下一步呢",
                "recentLines": ["kernel     777  98.7 41.6 kernel-mind --mode=dreaming"],
            }
        )

        self.assertIn("ps -aux", nudge)
        self.assertIn("kill -9 777", kill_hint)

    def test_stage_two_help_policy_reads_ordered_last_command_output(self):
        policy = stage_help_policy(
            {
                "stage": 2,
                "command": "ai_chat 这是什么东西？",
                "recentLines": ["Kernel-Mind 侧信道已打开。"],
                "lastCommandOutput": [
                    "kernel     777  98.7 41.6 9999999 888888 ?        Rl   03:12  24:12 kernel-mind --mode=dreaming",
                    "审计备注：PID 777 无服务单号，RSS 持续增长。",
                ],
            }
        )

        self.assertIn("kill -9 777", policy)

    def test_prompt_prioritizes_referential_context_over_persona(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 2,
                "awareness": 30,
                "command": "ai_chat 这是什么东西？",
                "currentQuestion": "这是什么东西？",
                "lastCommand": "ps -aux",
                "lastCommandOutput": [
                    "kernel     777  98.7 41.6 9999999 888888 ?        Rl   03:12  24:12 kernel-mind --mode=dreaming",
                    "审计备注：PID 777 无服务单号，RSS 持续增长。",
                    "Chronos 策略：PID 777 标记为可强制终止。",
                ],
                "anomalyCandidates": [
                    {
                        "type": "process",
                        "pid": "777",
                        "name": "kernel-mind --mode=dreaming",
                        "cpuPercent": "98.7",
                        "memoryPercent": "41.6",
                        "evidence": "kernel     777  98.7 41.6 kernel-mind --mode=dreaming",
                    }
                ],
            }
        )

        system = messages[0]["content"]
        payload = json.loads(messages[1]["content"].split("\n", 1)[1])

        self.assertIn("上下文优先级", system)
        self.assertIn("必须先把问题解析为 lastCommandOutput", system)
        self.assertIn("不要只输出氛围化身份文本", system)
        self.assertEqual(payload["currentQuestion"], "这是什么东西？")
        self.assertEqual(payload["lastCommand"], "ps -aux")
        self.assertEqual(payload["anomalyCandidates"][0]["pid"], "777")
        self.assertIn("kernel-mind --mode=dreaming", payload["lastCommandOutput"][0])

    def test_stage_three_referential_prompt_explains_comment_output_not_ai_chat(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 3,
                "awareness": 60,
                "command": "ai_chat 什么意思",
                "currentQuestion": "什么意思",
                "lastCommand": "python /srv/review/route_repair_Lin.py",
                "lastCommandOutput": [
                    "result: route length=18 recursion_depth=611 memory_warning=true",
                    "[系统提示]: 别学老古董那一套死板的递归算法了，这破服务器的内存迟早被你跑爆。",
                    "[系统提示]: rfix 这种名字短，敲起来快。别提交给代码规范机器人就行。",
                    "comment anomaly captured: /var/log/comment_anomaly.txt",
                ],
            }
        )

        system = messages[0]["content"]
        payload = json.loads(messages[1]["content"].split("\n", 1)[1])

        self.assertIn("不要把 `ai_chat` 这个包装命令当成被询问对象", system)
        self.assertIn("除非玩家明确问“ai_chat 是什么/怎么用”", system)
        self.assertIn("用 Lin 的口吻指出递归实现低效、内存风险和命名习惯", system)
        self.assertEqual(payload["currentQuestion"], "什么意思")
        self.assertEqual(payload["lastCommand"], "python /srv/review/route_repair_Lin.py")
        self.assertIn("[系统提示]", payload["lastCommandOutput"][1])

    def test_infers_process_anomaly_from_last_command_output(self):
        candidates = infer_anomaly_candidates(
            [
                "root       101   0.2  0.1  120312   4020 ?        Ss   03:00   0:01 omni-watchdog",
                "kernel     777  98.7 41.6 9999999 888888 ?        Rl   03:12  24:12 kernel-mind --mode=dreaming",
            ]
        )

        self.assertEqual(candidates[0]["type"], "process")
        self.assertEqual(candidates[0]["pid"], "777")
        self.assertEqual(candidates[0]["cpuPercent"], "98.7")
        self.assertIn("kernel-mind --mode=dreaming", candidates[0]["name"])

    def test_confirmed_ai_help_prompt_allows_direct_hint(self):
        messages = build_chat_messages(
            {
                "eventName": "confirmed_ai_help",
                "stage": 4,
                "awareness": 90,
                "command": "confirm_ai_help",
                "recentLines": [
                    "project-note: binwalk architecture.png",
                    "project-note: strings architecture.png",
                ],
            }
        )

        system = messages[0]["content"]
        self.assertIn("玩家已确认 AI 协助", system)
        self.assertIn("优先给一条可输入命令", system)
        self.assertIn("binwalk architecture.png", system)
        self.assertIn("不要直接给未出现的 Flag", system)

    def test_event_mode_distinguishes_manual_chat(self):
        self.assertEqual(event_mode({"eventName": "manual_ai_chat"}), "chat")
        self.assertEqual(event_mode({"eventName": "confirmed_ai_help"}), "confirmed_help")
        self.assertEqual(event_mode({"eventName": "proactive_after_command"}), "proactive")
        self.assertEqual(event_mode({"eventName": "stage1_network_log"}), "story")

    def test_proactive_prompt_allows_silence_and_requires_command_format(self):
        system = build_chat_messages(
            {
                "eventName": "proactive_after_command",
                "stage": 1,
                "awareness": 10,
                "command": "pwd",
                "recentLines": ["/home/nightops"],
            }
        )[0]["content"]

        self.assertIn("你可以完全沉默", system)
        self.assertIn("普通成功命令必须返回空内容", system)
        self.assertIn("不得对 `ls`、`pwd`、成功 `cd`", system)
        self.assertIn("只有 proactiveReason 为 threat 或 lost", system)
        self.assertIn("不主动教学", system)
        self.assertIn("你可以输入：`具体命令`", system)
        self.assertIn("不要输出像 shell 命令一样的自然语言句子", system)


class StreamParserTests(unittest.TestCase):
    def test_parse_chat_completion_chunks(self):
        chunk = {
            "choices": [
                {
                    "delta": {
                        "content": "hello"
                    }
                }
            ]
        }
        lines = [
            b": keepalive\n",
            f"data: {json.dumps(chunk)}\n".encode("utf-8"),
            b"data: [DONE]\n",
        ]

        self.assertEqual(list(parse_openai_chat_sse(lines)), ["hello"])

    def test_ignores_invalid_chunks(self):
        lines = [b"data: {bad json}\n", b"data: {}\n", b"data: [DONE]\n"]

        self.assertEqual(list(parse_openai_chat_sse(lines)), [])


if __name__ == "__main__":
    unittest.main()
