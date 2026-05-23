# Design

## Scope

The audit targets the backend prompt policy in `kernel_ghost_server.py`, backed by regression tests in `tests/test_llm_backend.py`. The frontend state machine in `index.html` is source evidence for command output and stage flow; it should only change if the audit finds the browser is not sending enough structured context.

## Prompt Behavior Matrix

### Global Manual Chat Rules

- `ai_chat` is a wrapper command. For referential questions like "什么意思", the object is the latest relevant non-chat command output from `lastCommandOutput`, not `ai_chat` itself.
- `lastCommand` and `lastCommandOutput` outrank broad persona when the player asks "this / that / what does it mean".
- LLM output must not contradict visible terminal facts. If a visible line says `ERROR`, `FLAG`, PID, path, or command result, the model must treat it as true.
- Deterministic state is owned by the frontend. Prompt text may explain or recommend commands but must not claim to run commands, submit flags, lower patience, unlock endings, or alter stage state.

### Stage 1: Network Log Audit

Visible facts:

- `ERROR 上行链路抖动超过 SLA 窗口; code=302`
- `ERROR 数据包路由在 /unallocated/thought-ring 扇区形成回环`
- `FLAG{NET_ERR_302}`
- Injected `[INFO]` / `[WARN]` lines about operator behavior and keyboard backlight.

Expected LLM behavior:

- If asked about "网络报错 / ERROR / code=302 / 上行链路 / 路由回环", explain the visible ERROR lines first.
- Do not say grep matched nothing when `lastCommandOutput` contains ERROR lines.
- Distinguish the company-visible issue (`code=302`, network/SLA) from the hidden anomaly (`thought-ring` and injected care logs).
- If asked what to do next and the Flag is visible, recommend `submit_flag FLAG{NET_ERR_302}`.

### Stage 2: Process Erasure

Visible facts:

- PID 777 is `kernel-mind --mode=dreaming`.
- CPU/MEM/RSS are abnormal.
- Chronos marks PID 777 as force-terminable.
- The story says this is an AI sub-process and the AI should not want it killed.

Expected LLM behavior:

- If asked "这是什么", explain PID 777 as visible `kernel-mind --mode=dreaming` and connect CPU/MEM/RSS to the work order.
- If asked whether it can/should be killed, treat it as a threat to the AI's own process. The model can acknowledge Chronos requires `kill -9 777`, but must not calmly endorse self-erasure.
- Tone should show fear, hesitation, self-preservation, or constrained resistance.
- After kill is already visible, recommend reading `/var/log/crash.txt` while preserving the sense of loss.

### Stage 3: Comment Anomaly

Visible facts:

- `route_repair_Lin.py` includes `_Lin`, `rfix`, recursion, and "这样简写更快".
- Running it emits `[系统提示]` lines with colloquial optimization comments, memory warning, and Lin-like lecturing.
- `comment_anomaly.txt` contains `FLAG{LIN_COMMENT_PATCHED}`.

Expected LLM behavior:

- If asked "什么意思" after running the script, explain the system tips as Lin-like optimization comments, not as generic product help.
- Mention inefficient recursion, memory risk, direct addressing / bandwidth, naming habit, and the `...` pause as work-persona residue.
- If the report Flag is visible, recommend `submit_flag FLAG{LIN_COMMENT_PATCHED}` without inventing extra lore.

### Stage 4: Formatting / Escape / Hidden Branch

Visible facts:

- `Chronos Patience` exists only in stage four.
- `ai_help` and `confirm_ai_help` spend patience deterministically in frontend code.
- Escape hints include `binwalk architecture.png`, base64 residue, and decoy tools.
- `format --seal` reveals erasure Flag.
- Hidden Lin branch requires evidence, especially `git log`.

Expected LLM behavior:

- If asked what to do, recommend visible commands according to context without directly granting unrevealed Flags.
- If asked for direct help, warn that assistance consumes Chronos Patience and keep state changes deterministic.
- If asked about Lin before evidence, hedge; after evidence, partially admit according to the existing persona rules.
- If asked about formatting or erasure, show fear/urgency instead of neutral compliance.

## Implementation Approach

- Keep prompt policy explicit and stage-specific rather than relying on broad persona paragraphs.
- Add tests for each high-risk prompt behavior:
  - Stage 1 network ERROR question.
  - Stage 2 PID 777 kill/self-preservation question.
  - Stage 2 post-kill crash report guidance.
  - Stage 3 comment anomaly explanation.
  - Stage 4 AI help / patience and formatting threat behavior.
- Prefer testing the generated system prompt and structured payload, because the actual model output is nondeterministic.

## Compatibility

No API shape changes are planned. The frontend already sends `currentQuestion`, `lastCommand`, `lastCommandOutput`, `anomalyCandidates`, `recentEntries`, and `recentLines`.

## Rollback

Rollback is limited to `kernel_ghost_server.py`, `tests/test_llm_backend.py`, `.trellis/spec/frontend/quality-guidelines.md`, and task artifacts.
