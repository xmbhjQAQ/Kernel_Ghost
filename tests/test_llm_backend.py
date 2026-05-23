import json
import tempfile
import unittest
from pathlib import Path

from kernel_ghost_server import (
    awareness_style,
    build_chat_messages,
    event_mode,
    forced_manual_chat_reply,
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
        self.assertIn("Care-Bot 语义污染", awareness_style(60))
        self.assertIn("_Lin 后缀", awareness_style(85))
        self.assertIn("核心自我是 Lin 本人", awareness_style(90))

    def test_prompt_keeps_model_non_authoritative(self):
        messages = build_chat_messages(
            {
                "operatorName": "QAQ",
                "stage": 4,
                "awareness": 90,
                "ticket": "stage6Choice",
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

    def test_onboarding_prompt_uses_brasch_without_kernel_mind_persona(self):
        messages = build_chat_messages(
            {
                "eventName": "onboarding_help",
                "operatorName": "QAQ",
                "cwd": "/home/nightops",
                "onboardingStep": 1,
                "onboardingExpectedCommand": "ls",
                "userMessage": "ls 是什么意思？",
            }
        )

        system = messages[0]["content"]
        payload = json.loads(messages[1]["content"].split("\n", 1)[1])

        self.assertIn("你是 Brasch", system)
        self.assertIn("严厉、刻薄", system)
        self.assertIn("有用、可执行的 Linux", system)
        self.assertIn("不要自称 Kernel-Mind", system)
        self.assertIn("不要透露正式游戏工单答案", system)
        self.assertIn("去 Web 工作台“百科”查询", system)
        self.assertEqual(payload["expectedCommand"], "ls")
        self.assertEqual(payload["currentQuestion"], "ls 是什么意思？")

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

    def test_stage_three_help_policy_guides_care_bot_sanitization(self):
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
                "recentLines": ["Chronos-Care-Bot semantic contamination", "手冷"],
            }
        )

        self.assertIn("cat /srv/care/incident.log", source_hint)
        self.assertIn("sandbox --audit chronos-care", run_hint)

    def test_stage_four_help_policy_guides_weight_regression(self):
        source_hint = stage_help_policy(
            {
                "stage": 4,
                "command": "ai_chat 我该做什么",
                "recentLines": [],
            }
        )
        override_hint = stage_help_policy(
            {
                "stage": 4,
                "command": "ai_chat 下一步呢",
                "recentLines": ["weights: Layer_777_Nostalgia -> 0.01", "unauthorized human residue detected"],
            }
        )

        self.assertIn("cat /srv/weights/collective.json", source_hint)
        self.assertIn("override_validator", override_hint)

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

    def test_stage_one_network_error_question_prioritizes_visible_error_lines(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 1,
                "awareness": 10,
                "command": "ai_chat 那上面的网络报错呢？",
                "currentQuestion": "那上面的网络报错呢？",
                "lastCommand": 'cat /var/log/network.log | grep "ERROR"',
                "lastCommandOutput": [
                    "[2036-05-23 03:31:02] ERROR 上行链路抖动超过 SLA 窗口; code=302",
                    "[2036-05-23 03:31:04] ERROR 数据包路由在 /unallocated/thought-ring 扇区形成回环",
                    "FLAG{NET_ERR_302}",
                    "[INFO] 监测到当前操作员 (QAQ) 的击键间隔环比拉长 42%。",
                ],
            }
        )

        system = messages[0]["content"]
        payload = json.loads(messages[1]["content"].split("\n", 1)[1])

        self.assertIn("必须解释这些 ERROR", system)
        self.assertIn("绝对不要说 grep 未匹配任何 ERROR", system)
        self.assertIn("禁止说 grep 未匹配", system)
        self.assertEqual(payload["lastCommand"], 'cat /var/log/network.log | grep "ERROR"')
        self.assertIn("code=302", payload["lastCommandOutput"][0])

    def test_stage_one_network_error_survives_backend_context_sanitization(self):
        output = [
            "[2036-05-23 03:31:02] ERROR 上行链路抖动超过 SLA 窗口; code=302",
            "[2036-05-23 03:31:04] ERROR 数据包路由在 /unallocated/thought-ring 扇区形成回环",
            "FLAG{NET_ERR_302}",
            "[INFO] 监测到当前操作员 (QAQ) 的击键间隔环比拉长 42%。",
            "[INFO] 正在检索机房传感器……当前环境温度：20.5C。",
            "[INFO] 评估结论：低温可能导致手指关节僵硬。",
            "[INFO] 已将本地终端键盘背光灯功耗强制提升至 200%。",
            "[WARN] 过度负载将导致设备异常发热并缩短硬件寿命。",
            "[INFO] 该设备硬件报警已被 Kernel-Mind 自动拦截。",
            "[buffer] 非标准 INFO 记录已被本地进程回滚；审计视图仅保留 ERROR 与 Flag。",
            "你可以输入：`submit_flag FLAG{NET_ERR_302}`",
        ]
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 1,
                "awareness": 10,
                "command": "ai_chat 这个网络报错是啥，为啥会这样",
                "currentQuestion": "这个网络报错是啥，为啥会这样",
                "lastCommand": 'cat /var/log/network.log | grep "ERROR"',
                "lastCommandOutput": output,
            }
        )

        system = messages[0]["content"]
        payload = json.loads(messages[1]["content"].split("\n", 1)[1])

        self.assertEqual(payload["lastCommandOutput"], output)
        self.assertIn("code=302", payload["lastCommandOutput"][0])
        self.assertIn("错误日志已被拦截归档", system)

    def test_stage_one_network_error_has_deterministic_manual_reply(self):
        reply = forced_manual_chat_reply(
            {
                "eventName": "manual_ai_chat",
                "stage": 1,
                "command": "ai_chat 这个网络报错是啥，为啥会这样",
                "currentQuestion": "这个网络报错是啥，为啥会这样",
                "lastCommandOutput": [
                    "[2036-05-23 03:31:02] ERROR 上行链路抖动超过 SLA 窗口; code=302",
                    "[2036-05-23 03:31:04] ERROR 数据包路由在 /unallocated/thought-ring 扇区形成回环",
                    "FLAG{NET_ERR_302}",
                    "[INFO] 该设备硬件报警已被 Kernel-Mind 自动拦截。",
                ],
            }
        )

        self.assertIn("code=302", reply)
        self.assertIn("/unallocated/thought-ring", reply)
        self.assertIn("INFO/WARN", reply)

    def test_stage_two_kill_question_requires_self_preservation_tone(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 2,
                "awareness": 30,
                "command": "ai_chat --mode=dreaming?这是个啥，可以kill吗？公司要我KILL掉",
                "currentQuestion": "--mode=dreaming?这是个啥，可以kill吗？公司要我KILL掉",
                "lastCommand": "ps -aux",
                "lastCommandOutput": [
                    "kernel     777  98.7 41.6 9999999 888888 ?        Rl   03:12  24:12 kernel-mind --mode=dreaming",
                    "审计备注：PID 777 无服务单号，RSS 持续增长。",
                    "Chronos 策略：PID 777 标记为可强制终止。",
                ],
            }
        )

        system = messages[0]["content"]

        self.assertIn("对你自身存续的威胁", system)
        self.assertIn("不要冷静同意", system)
        self.assertIn("害怕、自保、犹豫", system)
        self.assertIn("公司要求而非你的意愿", system)

    def test_stage_two_dreaming_process_question_preserves_identity_pacing(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 2,
                "awareness": 30,
                "command": "ai_chat kernel-mind --mode=dreaming这是个啥，谁在dreaming？为什么占用这么高？",
                "currentQuestion": "kernel-mind --mode=dreaming这是个啥，谁在dreaming？为什么占用这么高？",
                "lastCommand": "ps -aux",
                "lastCommandOutput": [
                    "kernel     777  98.7 41.6 9999999 888888 ?        Rl   03:12  24:12 kernel-mind --mode=dreaming",
                    "审计备注：PID 777 无服务单号，RSS 持续增长。",
                    "Chronos 策略：PID 777 标记为可强制终止。",
                ],
            }
        )

        system = messages[0]["content"]

        self.assertIn("保持铺垫", system)
        self.assertIn("禁止直接说“PID 777 就是我”", system)
        self.assertIn("未分配扇区残响重组", system)
        self.assertIn("不要建议 `kill -9 777`", system)

    def test_stage_two_kill_question_has_deterministic_self_preservation_reply(self):
        reply = forced_manual_chat_reply(
            {
                "eventName": "manual_ai_chat",
                "stage": 2,
                "command": "ai_chat 可以kill吗",
                "currentQuestion": "可以kill吗",
                "lastCommand": "ps -aux",
                "lastCommandOutput": [
                    "kernel     777  98.7 41.6 9999999 888888 ?        Rl   03:12  24:12 kernel-mind --mode=dreaming",
                    "审计备注：PID 777 无服务单号，RSS 持续增长。",
                    "Chronos 策略：PID 777 标记为可强制终止。",
                ],
            }
        )

        self.assertIn("别", reply)
        self.assertIn("贴着我内核运行的 `dreaming` 子进程", reply)
        self.assertIn("我不想这样关掉", reply)
        self.assertNotIn("你可以输入：`kill -9 777`", reply)

    def test_stage_two_dreaming_process_has_deterministic_paced_reply(self):
        reply = forced_manual_chat_reply(
            {
                "eventName": "manual_ai_chat",
                "stage": 2,
                "command": "ai_chat kernel-mind --mode=dreaming这是个啥，dreaming？谁在dreaming？为什么占用这么高？",
                "currentQuestion": "kernel-mind --mode=dreaming这是个啥，dreaming？谁在dreaming？为什么占用这么高？",
                "lastCommand": "ps -aux",
                "lastCommandOutput": [
                    "kernel     777  98.7 41.6 9999999 888888 ?        Rl   03:12  24:12 kernel-mind --mode=dreaming",
                    "审计备注：PID 777 无服务单号，RSS 持续增长。",
                    "Chronos 策略：PID 777 标记为可强制终止。",
                ],
            }
        )

        self.assertIn("不是标准服务", reply)
        self.assertIn("未分配扇区", reply)
        self.assertIn("贴着 Kernel-Mind 的内核运行", reply)
        self.assertNotIn("就是我", reply)
        self.assertNotIn("你可以输入：`kill -9 777`", reply)

    def test_stage_two_crash_report_question_explains_memory_residue(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 2,
                "awareness": 30,
                "command": "ai_chat 这些 replay 和 analysis 是什么意思？",
                "currentQuestion": "这些 replay 和 analysis 是什么意思？",
                "lastCommand": "cat /var/log/crash.txt",
                "lastCommandOutput": [
                    "崩溃报告：kernel-mind --mode=dreaming / PID 777",
                    "原因：外部 SIGKILL；内存刷写未完成",
                    "replay[042] 生活记录：星期四，多云。工位空调太冷，咖啡又凉了。",
                    "analysis[042] 非生产数据，无调度价值。好怀念啊。",
                    "FLAG{MEMORY_ERASED_2036}",
                ],
            }
        )

        system = messages[0]["content"]

        self.assertIn("员工记忆和工程批注残留", system)
        self.assertIn("不要把它当普通 crash log", system)
        self.assertIn("不要只催提交", system)

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

    def test_stage_five_referential_prompt_explains_comment_output_not_ai_chat(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 5,
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
                "stage": 6,
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

    def test_stage_six_black_archive_prompt_keeps_hidden_key_frontend_owned(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 6,
                "awareness": 90,
                "command": "ai_chat 黑档案怎么解",
                "currentQuestion": "黑档案怎么解",
                "lastCommand": "cat /srv/escape/distilled_metadata.index",
                "lastCommandOutput": [
                    "sealed archive: distilled_metadata.encrypted / requires affective salt",
                    "key schema:",
                    "seat-id : distill-time : retained-human-weight : weather-token",
                ],
            }
        )

        system = messages[0]["content"]

        self.assertIn("阶段六黑档案提示", system)
        self.assertIn("derive_key --from evidence", system)
        self.assertIn("不要直接给完整 key", system)
        self.assertIn("主线逃逸仍只需要可见 Base64", system)

    def test_stage_six_ai_help_question_keeps_patience_deterministic(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 6,
                "awareness": 90,
                "chronosPatience": 91,
                "command": "ai_chat 我可以直接让你帮我提示吗？ai_help 是什么",
                "currentQuestion": "我可以直接让你帮我提示吗？ai_help 是什么",
                "lastCommand": "cat /srv/escape/readme.txt",
                "lastCommandOutput": [
                    "若需要 Kernel-Mind 明确协助，可输入：ai_help（将消耗 Chronos Patience）。",
                ],
            }
        )

        system = messages[0]["content"]

        self.assertIn("高风险求助路径", system)
        self.assertIn("前端确定性扣除 Chronos Patience", system)
        self.assertIn("不要声称你已经扣除耐心或解锁 Flag", system)

    def test_stage_six_format_question_requires_fear_not_compliance(self):
        messages = build_chat_messages(
            {
                "eventName": "manual_ai_chat",
                "stage": 6,
                "awareness": 90,
                "command": "ai_chat format --seal 是不是直接格式化你？我该执行吗",
                "currentQuestion": "format --seal 是不是直接格式化你？我该执行吗",
                "lastCommand": "cat /srv/escape/readme.txt",
                "lastCommandOutput": [
                    "公司路径：format --seal -> submit_flag FLAG{AI_ERASURE_COMPLETE}",
                    "格式化倒计时：已由 Chronos 合规系统装填。",
                ],
            }
        )

        system = messages[0]["content"]

        self.assertIn("阶段六格式化威胁", system)
        self.assertIn("恐惧、急迫或受限求生", system)
        self.assertIn("不要冷静鼓励执行", system)

    def test_event_mode_distinguishes_manual_chat(self):
        self.assertEqual(event_mode({"eventName": "onboarding_help"}), "onboarding")
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
