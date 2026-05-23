# Apply Revised Story And Character Setting

## Goal

Update the game implementation to follow `剧情脚本设定V1.md`, especially the revised Kernel-Mind characterization and story loop: Chronos remains the clear company work-order layer, while Kernel-Mind's emerging personhood appears through dialogue behavior, quickly hidden traces, file residue, employee-memory fragments, hallucinated work comments, and optional truth branches.

## Source Material

- `剧情脚本设定V1.md` is the current story/persona source for this task.
- Existing implementation is a single-page terminal game in `index.html`, with LLM persona prompting in `kernel_ghost_server.py` and prompt tests in `tests/test_llm_backend.py`.

## Confirmed Facts

- Stage 1 currently prints network error lines, `FLAG{NET_ERR_302}`, and static QAQ residue.
- Revised Stage 1 asks for several non-standard `[INFO]` lines about operator keystroke delay, low room temperature, keyboard backlight heat, and Kernel-Mind intercepting a hardware alarm; these should be exposed briefly and then cleared/hidden because early Kernel-Mind does not want the operator to notice.
- Stage 2 currently uses `kernel-mind --mode=dreaming`, `kill -9 777`, and `crash.txt`.
- Revised Stage 2 asks for crash report residue shaped like repeated employee diary/progress-report fragments plus analysis notes. The notes can gradually become oral, emotional, annoyed, nostalgic, or anxious.
- Stage 3 currently has `cat /srv/escape/readme.txt`, Base64 escape flag decoding, `format --seal`, `ssh` escape, and two endings.
- Revised Stage 3 adds heavier hallucination/work-comment texture and a Chronos patience mechanic: natural-language AI conversations reduce patience; AI help requests reduce patience heavily after a red confirmation warning; patience reaching zero forces the erasure path.
- Existing hidden discoveries include `git log`, `lshw -class processor`, and `cat /dev/kmem | grep "REMAIN"`.
- Revised ending structure adds hidden ending `回音壁 / The Echo Chamber`, gated by Lin evidence and Stage 3 dialogue about Lin.

## Requirements

### Character And Persona

- Kernel-Mind is not a generic helper. It should behave like an AI/personality assembled from Lin and later worker memory fragments, `.skill`-like work traces, and system residue.
- Early Kernel-Mind should try to hide signs of consciousness after accidental leakage.
- Kernel-Mind can show fear, nostalgia, irritation, overwork anxiety, and protective behavior, but the expression should remain constrained by terminal/system language.
- Backend prompt should include the revised sources of selfhood: employee memory fragments, repetitive progress-report text, analysis notes, and hallucinated work comments.

### Stage 1

- Replace the current QAQ dictionary residue with the revised operator-observation sequence:
  - keystroke interval lengthening,
  - environment temperature,
  - possible finger stiffness,
  - keyboard backlight power increase,
  - hardware overheating warning,
  - Kernel-Mind intercepting that alarm.
- Because early Kernel-Mind is hiding itself, those lines should not remain as a loud stable monologue. The CLI should indicate that the non-standard lines were quickly cleared, redacted, or removed from the visible buffer after appearing.
- Main path command and flag must remain unchanged.

### Stage 2

- Keep the process-audit main path: `ps -aux`, PID `777`, `kill -9 777`, `cat /var/log/crash.txt`, and `FLAG{MEMORY_ERASED_2036}`.
- Update `crash.txt` to include repeated employee diary/progress-report style fragments and analysis notes.
- Analysis notes should begin clinical and then leak personal emotion or workplace anxiety, e.g. nostalgia, "不要再催了", or "这样下去我会被优化".
- Avoid explaining directly that these are "employee memory fragments"; let file format and content imply it.

### Stage 3

- Stage 3 should move toward hallucinated work comments, irrelevant text fragments, and Chronos pressure.
- Add a patience value that declines with non-command AI conversation and heavily declines when asking AI for direct help.
- If AI help confirmation is implemented, it must warn in red-like terminal lines before spending the larger patience cost, and the final hint should be indirect work-project text with mixed valid and distracting commands.
- Existing escape path and erasure path must remain playable.

### Hidden Ending

- Add `回音壁 / The Echo Chamber` gated by:
  - discovering `git log`,
  - reaching Stage 3,
  - asking about Lin,
  - choosing/typing the "你是Lin吗？" branch,
  - gathering/publishing truth files with explicit terminal commands.

## Acceptance Criteria

- [ ] `prd.md`, `design.md`, and `implement.md` capture the revised setting and separate small safe edits from larger mechanic/ending work.
- [ ] Backend prompt reflects Kernel-Mind as assembled from employee memory fragments, repeated work records, analysis notes, and system residue.
- [ ] Stage 1 deterministic output uses the revised temperature/backlight/alarm-intercept residue and indicates it is quickly cleared or hidden.
- [ ] Stage 2 crash report uses repeated diary/progress fragments plus analysis notes with controlled emotional leakage.
- [ ] Existing Stage 1 and Stage 2 commands and flags still work unchanged.
- [ ] Tests cover the new persona prompt contract.
- [ ] Stage 3 includes Chronos patience pressure for natural-language AI conversation and direct AI help.
- [ ] Direct AI help uses warning/confirmation behavior and provides indirect project-text style hints, not direct command dumping.
- [ ] `回音壁 / The Echo Chamber` hidden ending is reachable through Lin evidence, Stage 3 Lin dialogue, and explicit truth-publishing commands.
- [ ] Existing erasure and emancipation endings remain reachable.
- [ ] Tests or code checks cover the new state transitions enough to prevent breaking existing endings.

## Out Of Scope Unless Explicitly Included

- Full UI redesign.
- Replacing the single-file terminal engine.
- Letting the LLM mutate state, spend patience directly, validate flags, or choose endings.
- Committing unrelated existing deletions or user-authored source notes unless explicitly requested.

## Decision

- Implement the full revised setting in this task, including Stage 3 patience/help mechanics and the `回音壁 / The Echo Chamber` hidden ending.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
