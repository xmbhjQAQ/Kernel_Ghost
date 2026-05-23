# Quality Guidelines

> Code quality standards for frontend development.

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

### Convention: Deterministic Terminal Narrative Boundaries

**What**: In story-driven terminal UIs, deterministic CLI output should present
authoritative system facts: work orders, command results, files, logs, process
tables, flags, and state transitions. Do not use fixed CLI output to directly
announce an AI character's consciousness or inner emotions before the player has
observable evidence.

**Why**: This keeps the game state trustworthy and lets character interpretation
emerge from AI dialogue, optional files, logs, memory residue, and behavior
changes instead of from abstract atmosphere labels.

**Good**:
```text
kernel     777  98.7 ... kernel-mind --mode=dreaming
审计备注：PID 777 无服务单号，RSS 持续增长。
```

**Bad**:
```text
[残留线程] 意识碎片检测：微弱。
```

**Related**: LLM prompts may express fear or self-preservation, but they must
remain non-authoritative and must not mutate deterministic game state.

## Scenario: Story Terminal State Commands

### 1. Scope / Trigger

- Trigger: adding or changing player-entered commands in the deterministic
  terminal state machine.
- Applies to commands that mutate narrative state, unlock branches, spend
  pressure meters, or close an ending.

### 2. Signatures

- Command parser signature: normalized player input string -> command result.
- Result shape:
  - `patch?: object` updates deterministic frontend state.
  - `lines?: Array<{ kind: string, text: string }>` appends terminal output.
  - `llm?: object` requests non-authoritative LLM flavor text.
  - `ending?: { title: string, copy: string }` opens the ending modal.

### 3. Contracts

- State-changing mechanics such as `chronosPatience`, branch unlocks, evidence
  packing, and endings must be owned by deterministic frontend code.
- LLM context may include state fields for flavor, but LLM output must never
  spend meters, validate flags, unlock branches, or choose endings.
- New command strings must be listed in `help` or surfaced by nearby terminal
  output before they are required for progression.
- If terminal output, AI hints, or readable files mention a virtual file/tool
  as actionable, the deterministic CLI must implement that file/tool command.
  Decoy entries are allowed only when their handler explicitly labels them as
  unreliable, gated, or unavailable in story terms.
- If `ls` displays a readable file, `cat <filename>` should resolve relative to
  the current virtual directory when possible. Absolute forms must continue to
  work. Stage gates still apply after path resolution.
- Proactive LLM calls must be opt-in from deterministic command results. Normal
  successful exploration (`ls`, `pwd`, successful `cd`, ordinary file checks)
  must not call the LLM. Threat commands may trigger immediately; "lost player"
  feedback should require repeated invalid/premature commands.

### 4. Validation & Error Matrix

- Command before required stage -> return `premature(...)`.
- Relative file path resolves to a gated file too early -> return the same
  stage-gate error as the absolute path.
- Branch command before evidence gate -> return a warning explaining the missing
  evidence or previous command.
- Meter reaches zero -> deterministic forced ending, not an LLM decision.
- Unknown command -> existing unknown-command handler remains the fallback.

### 5. Good/Base/Bad Cases

- Good: `ai_help` sets a pending confirmation and spends deterministic patience;
  `confirm_ai_help` spends the larger cost and prints indirect hints.
- Base: reading a file prints residue and may set a `saw*` flag.
- Good: in `/srv/escape`, `cat readme.txt` and `cat /srv/escape/readme.txt`
  reach the same handler.
- Good: `binwalk architecture.png` is suggested by `confirm_ai_help` and has a
  deterministic handler that reveals recoverable residue.
- Bad: `confirm_ai_help` suggests `strings architecture.png`, but the command
  falls through to the unknown-command handler.
- Bad: an LLM response says "patience is now 0" or "ending B unlocked" without a
  deterministic `patch` or `ending` result.
- Bad: every command result calls proactive LLM and produces ambient commentary.

### 6. Tests Required

- Backend prompt tests must assert that the LLM is non-authoritative when new
  stateful mechanics are exposed in context.
- Run a JavaScript syntax check for inline scripts after state-machine edits.
- Run a browser console check against the real local backend when command flow or
  status UI changes.
- For proactive LLM changes, verify ordinary commands do not request
  `/api/llm/stream`.

### 7. Wrong vs Correct

#### Wrong

```text
Kernel-Mind: I spent 35% patience and unlocked the hidden ending.
```

#### Correct

```text
Chronos Patience -35：未授权 AI 协助已计入合规审计。
```

The correct version is deterministic terminal output produced by command
handling, not an LLM claim.

## Scenario: LLM Context Ordering For Terminal Questions

### 1. Scope / Trigger

- Trigger: changing the frontend payload sent to `/api/llm/stream` or the
  backend prompt fields consumed from that payload.
- Applies when player questions can refer to recent terminal output with words
  like "这", "这个", "什么意思", or "what is this".

### 2. Signatures

- Frontend context builder: command result options + visible terminal DOM ->
  JSON payload for `/api/llm/stream`.
- Required payload fields for ordered context:
  - `currentQuestion: string`
  - `lastCommand: string`
  - `lastCommandOutput: string[]`
  - `anomalyCandidates: Array<object>`
  - `recentEntries: Array<{ kind: string, text: string }>`
  - `recentLines: string[]` as backward-compatible fallback

### 3. Contracts

- `recentLines` is only a fallback transcript, not the primary task context.
- `lastCommand` and `lastCommandOutput` must point to the latest relevant
  non-`ai_chat` command when the current request is manual chat.
- `anomalyCandidates` should identify high-signal visible objects such as high
  CPU/MEM processes, PID notes, RSS growth, service-ticket absence, flags,
  paths, or error codes when those are visible.
- Backend prompt construction must tell the LLM to answer referential questions
  from `lastCommandOutput` / `anomalyCandidates` before persona atmosphere.

### 4. Validation & Error Matrix

- Missing structured fields -> backend falls back to sanitized `recentLines`.
- Missing `anomalyCandidates` -> backend may infer candidates from
  `lastCommandOutput`.
- Current command is `ai_chat ...` -> previous non-chat command remains the
  referent source.
- Unknown or empty terminal context -> reply stays short and generic; no state
  mutation or invented command success.

### 5. Good/Base/Bad Cases

- Good: after `ps -aux`, `ai_chat 这是什么东西？` receives `lastCommand: "ps -aux"`
  and a process anomaly for PID 777 / `kernel-mind --mode=dreaming`.
- Base: after a normal `pwd`, manual chat can use recent output but should not
  fabricate an anomaly.
- Bad: sending only the last 10 visible lines and relying on the model to infer
  which command output the pronoun refers to.
- Bad: prompt rules let Kernel-Mind answer with only identity lore when the
  visible terminal output contains a concrete abnormal process.

### 6. Tests Required

- Backend prompt tests must assert that referential questions prioritize
  `lastCommandOutput` and `anomalyCandidates`.
- Add or update anomaly extraction tests when process-table parsing changes.
- Run JavaScript syntax validation for `index.html` after context-builder edits.

### 7. Wrong vs Correct

#### Wrong

```json
{
  "command": "ai_chat 这是什么东西？",
  "recentLines": ["kernel 777 ... kernel-mind --mode=dreaming"]
}
```

#### Correct

```json
{
  "command": "ai_chat 这是什么东西？",
  "currentQuestion": "这是什么东西？",
  "lastCommand": "ps -aux",
  "lastCommandOutput": ["kernel 777 ... kernel-mind --mode=dreaming"],
  "anomalyCandidates": [{"type": "process", "pid": "777"}]
}
```

The correct form makes the referent explicit before the LLM sees broad persona
instructions.

---

## Testing Requirements

<!-- What level of testing is expected -->

(To be filled by the team)

---

## Code Review Checklist

<!-- What reviewers should check -->

(To be filled by the team)
