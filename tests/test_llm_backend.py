import json
import unittest

from kernel_ghost_server import (
    awareness_style,
    build_chat_messages,
    event_mode,
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
        self.assertIn("terse diagnostic", awareness_style(0))
        self.assertIn("crash-report", awareness_style(40))
        self.assertIn("awakened AI", awareness_style(90))

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
        self.assertIn("Never grant flags", system)
        self.assertIn("change game state", system)
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
        self.assertIn("chat with the operator", system)
        self.assertIn("progressive hints", system)
        self.assertIn("Never reveal a flag unless", system)
        self.assertIn('cat /var/log/network.log | grep "ERROR"', system)
        self.assertIn("Mode: conversational assistant", system)

    def test_prompt_forbids_repeating_frontend_confirmation(self):
        system = build_chat_messages({"eventName": "manual_ai_chat"})[0]["content"]

        self.assertIn("Do not repeat this fixed frontend line", system)
        self.assertIn("Deterministic engine remains authoritative", system)

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

    def test_event_mode_distinguishes_manual_chat(self):
        self.assertEqual(event_mode({"eventName": "manual_ai_chat"}), "chat")
        self.assertEqual(event_mode({"eventName": "stage1_network_log"}), "story")


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
