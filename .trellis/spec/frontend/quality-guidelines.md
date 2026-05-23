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

---

## Testing Requirements

<!-- What level of testing is expected -->

(To be filled by the team)

---

## Code Review Checklist

<!-- What reviewers should check -->

(To be filled by the team)
