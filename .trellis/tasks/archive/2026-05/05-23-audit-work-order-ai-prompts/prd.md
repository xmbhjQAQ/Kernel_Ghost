# Audit all work order AI prompts

## Goal

Systematically audit and harden the LLM prompt behavior across all Kernel Ghost work orders so player follow-up questions bind to the correct terminal output and preserve the intended narrative persona from `剧情脚本设定V2.md`.

The immediate motivation is that manual `ai_chat` replies have repeatedly shown two classes of defects:

- Context binding defects, such as treating `ai_chat` itself as the object of "什么意思", or ignoring visible network `ERROR` lines.
- Persona defects, such as calmly endorsing killing `kernel-mind --mode=dreaming` when the story says the AI should resist or show fear.

## Requirements

- Treat `剧情脚本设定V2.md` and deterministic terminal output in `index.html` as source material.
- Audit all playable work-order stages:
  - Stage 1: network log audit and injected INFO/WARN residue.
  - Stage 2: process list, PID 777 / `kernel-mind --mode=dreaming`, kill command, crash report.
  - Stage 3: `route_repair_Lin.py`, comment anomaly output, comment report.
  - Stage 4: escape readme, AI help confirmation, binwalk/base64 escape, format / erasure, hidden Lin branch.
- For each stage, define expected LLM behavior for common player follow-ups:
  - "这是什么 / 什么意思 / 怎么导致的"
  - "我该怎么办 / 下一步"
  - "可以这样吗 / 能 kill 吗 / 已经 kill 了?"
  - topic-specific questions such as "网络报错呢", "这个注释什么意思", "这个 Flag 是什么", "Lin 是谁"
- Ensure prompt policy prioritizes visible terminal facts correctly:
  - If visible `ERROR` lines exist, never claim grep matched nothing.
  - If `kernel-mind --mode=dreaming` / PID 777 is visible, treat kill questions as self-preservation threats, not neutral IT support.
  - If stage-three `[系统提示]` comments are visible, explain them as Lin-like optimization comments, not product support.
  - If stage-four escape hints are visible, give bounded puzzle guidance without directly granting hidden or unrevealed Flags.
- Preserve deterministic boundaries:
  - LLM must not unlock flags, spend patience, advance stages, run commands, or choose endings.
  - LLM can recommend surfaced commands only when appropriate and must distinguish Chronos orders from Kernel-Mind's own will.
- Add regression tests for each audited prompt class.
- Keep the offline deterministic game behavior unchanged unless the audit reveals a frontend context payload bug.

## Acceptance Criteria

- [ ] A prompt behavior matrix exists in `design.md` covering stages 1-4 and common follow-up classes.
- [ ] `kernel_ghost_server.py` prompt policy implements the matrix without contradicting visible terminal output.
- [ ] Tests cover at least one context-binding and one persona case per major stage.
- [ ] Existing tests still pass with the new prompt rules.
- [ ] Any already-applied prompt fixes for network `ERROR`, `ai_chat` wrapper confusion, and PID 777 self-preservation are included in the task's final commit.
- [ ] `python -m pytest` and `python -m py_compile kernel_ghost_server.py` pass.

## Notes

- Current dirty worktree before this task includes prompt/test/spec edits from the immediate bug reports:
  - `.trellis/spec/frontend/quality-guidelines.md`
  - `kernel_ghost_server.py`
  - `tests/test_llm_backend.py`
- Unrelated pre-existing dirty paths remain out of scope and must not be reverted:
  - deleted `.trellis/spec/frontend/interactive-space-h5.md`
  - deleted `大纲.md`
  - untracked `剧情脚本设定V1.md`
