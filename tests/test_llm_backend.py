import json
import unittest

from kernel_ghost_server import (
    awareness_style,
    build_chat_messages,
    event_mode,
    infer_anomaly_candidates,
    parse_openai_chat_sse,
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
        config = read_llm_config({})

        self.assertFalse(config.ready)
        self.assertFalse(config.enabled)


class PromptTests(unittest.TestCase):
    def test_awareness_changes_style(self):
        self.assertIn("冷静诊断", awareness_style(0))
        self.assertIn("工程进度汇报", awareness_style(40))
        self.assertIn("核心自我是 Lin 本人", awareness_style(90))

    def test_prompt_keeps_model_non_authoritative(self):
        messages = build_chat_messages(
            {
                "operatorName": "QAQ",
                "stage": 3,
                "awareness": 90,
                "ticket": "stage3Choice",
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

    def test_prompt_forbids_repeating_frontend_confirmation(self):
        system = build_chat_messages({"eventName": "manual_ai_chat"})[0]["content"]

        self.assertIn("不要重复固定前端提示", system)
        self.assertIn("Kernel-Mind side channel open", system)

    def test_prompt_requires_short_threat_aware_replies(self):
        system = build_chat_messages(
            {
                "eventName": "proactive_after_command",
                "stage": 2,
                "awareness": 40,
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
                "stage": 3,
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
                "awareness": 40,
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
        self.assertIn("必须先把“这/这个”解析为 lastCommandOutput", system)
        self.assertIn("不要只输出氛围化身份文本", system)
        self.assertEqual(payload["currentQuestion"], "这是什么东西？")
        self.assertEqual(payload["lastCommand"], "ps -aux")
        self.assertEqual(payload["anomalyCandidates"][0]["pid"], "777")
        self.assertIn("kernel-mind --mode=dreaming", payload["lastCommandOutput"][0])

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

    def test_event_mode_distinguishes_manual_chat(self):
        self.assertEqual(event_mode({"eventName": "manual_ai_chat"}), "chat")
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
