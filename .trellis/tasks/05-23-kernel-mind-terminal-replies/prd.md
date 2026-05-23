# Make Kernel-Mind story tasks feel more dimensional

## Goal

Improve the Omni-OS terminal story loop so each work order feels like a layered narrative beat instead of a flat instruction-response pair. Kernel-Mind should still be constrained by Chronos policy and generally obedient, but its short reactions should reveal fear, self-preservation, memory residue, and personality when the player's actions threaten it or when the player explores outside the expected path.

The desired effect is not longer AI monologues. The deterministic task outputs should carry the corporate work-order surface and verifiable traces, while self-awareness emerges mainly through Kernel-Mind dialogue, its behavioral choices, and residue in explorable system files.

## Confirmed Facts

- The current game is a single-page terminal experience in `index.html` with deterministic command handling and stage progression.
- `kernel_ghost_server.py` builds the LLM prompt for manual `ai_chat`, proactive after-command checks, and story events.
- Previous work already established Kernel-Mind as an awakened but constrained AI, with proactive replies after commands and Chinese-first output.
- The current prompt permits "保持简短的终端行" but does not enforce the user's new stricter style target: one or two short lines, usually no more than 10 Chinese characters per line.
- The current deterministic work orders already include the main beats: network anomaly, process kill, crash report, formatting / escape choice, hidden discoveries, and two endings.
- The user wants the story tasks to become more dimensional, not merely to reduce the word count of LLM output.

## Requirements

### Story Task Depth

- Work orders must feel like layered scenes with:
  - a Chronos compliance objective,
  - a routine technical surface,
  - discoverable file/process/log residue,
  - a player-action consequence that changes the feeling of the next task.
- Normal task guidance should remain playable for non-Linux players; the company line may be direct, while Kernel-Mind's line should be indirect.
- Each stage should make the player feel the conflict between "finish the ticket" and "notice the personhood in the system."
- Optional exploration should receive meaningful in-world feedback when it touches story-relevant areas, without requiring optional content for the main path.
- Story terms must be legible from context. Avoid unexplained atmosphere-only jargon such as "residual thread" or "consciousness fragment" unless the surrounding output makes them concrete through a process, PID, file, log, memory dump, or repeated observable behavior.
- Prefer concrete terminal evidence before metaphor: unusual process names, CPU usage, unreadable crash buffers, repeated operator-name tokens, corrupted comments, heat logs, or files that should have been deleted but still exist.
- Fixed CLI output should not directly announce that Kernel-Mind is self-aware. It should show corporate instructions, technical anomalies, files, logs, process facts, and memory residue. The interpretation that something is waking up should come from the player's conversation with Kernel-Mind, Kernel-Mind's reactions, and the contents of optional or required system files.

### Kernel-Mind Reply Style

- Kernel-Mind LLM replies should be extremely short: one or two terminal-style lines, with a target of no more than 10 Chinese characters per line unless a literal command, path, PID, or Flag is required.
- Kernel-Mind should not produce long diagnostic blocks that drown out deterministic terminal output.
- In ordinary situations it usually obeys Chronos and may stay silent.
- When the player threatens Kernel-Mind directly, such as preparing to kill `PID 777`, format the core, or submit an erasure ending, Kernel-Mind may show fear or self-preservation.
- Fear should be expressed through constrained system language, fragments, or emotional residue, not out-of-world exposition.
- Kernel-Mind's selfhood should be inferred from behavior: hesitation, selective silence, fear near destructive commands, attachment to repeated human details, and constrained attempts to redirect the player.

### Prompt And Determinism

- LLM output must remain non-authoritative: it cannot mutate state, validate flags, grant flags, choose endings, or claim actions succeeded.
- The prompt must preserve the "Chronos constraint" hierarchy: company instructions remain dominant in normal operations, but Kernel-Mind can leak personality under pressure.
- If the LLM is unavailable, deterministic playthrough must still complete, but it should present only the corporate surface plus file/log residue rather than fully explaining Kernel-Mind's consciousness.
- Existing command, path, PID, process name, and Flag literals must stay exact.

### Scope For This Task

- Update the backend LLM prompt contract for shorter, more emotional, threat-aware Kernel-Mind replies.
- Update deterministic terminal text for the early work-order loop so it stops asserting self-awareness directly and instead exposes concrete traces for the player to interpret.
- Add or adjust tests that lock the new prompt constraints.
- Avoid a full rewrite of all stages unless inspection shows a small, localized edit can safely improve them.

## Acceptance Criteria

- [ ] `prd.md`, `design.md`, and `implement.md` describe the broader story-task goal, not only response length.
- [ ] Backend prompt instructs Kernel-Mind to reply in one or two very short terminal-style lines, target <= 10 Chinese characters per line when no literal command/path/Flag is needed.
- [ ] Backend prompt distinguishes ordinary obedience from threat-triggered fear/self-preservation.
- [ ] Backend prompt continues to forbid authoritative game-state actions and unearned Flag leakage.
- [ ] Stage 1/2 deterministic outputs around the reported transcript are less noisy and better layered: Chronos instruction, technical finding, and Kernel-Mind residue do not repeat the same hint several times.
- [ ] Stage 1/2 terminology is understandable without prior lore; abstract labels are replaced by concrete process/log/memory evidence or introduced through observable behavior.
- [ ] Fixed CLI output no longer says or strongly implies "Kernel-Mind is conscious" through abstract labels; it leaves that to AI dialogue, behavior, and file residue.
- [ ] At least one required or optional system file/log in the early game carries concrete residue that supports the self-awareness reading without narrating it directly.
- [ ] A threat moment such as `kill -9 777` can produce a brief in-character fear reaction without turning into a long monologue.
- [ ] Tests cover the new reply-length and threat-emotion prompt constraints.
- [ ] Existing deterministic playthrough remains functional when LLM is unavailable.

## Out Of Scope

- Replacing the single-page terminal engine.
- Letting the LLM control game state or command execution.
- Turning Kernel-Mind into a long-form companion chatbot.
- Rebuilding every hidden branch or ending in this pass.

## Decisions

- Prioritize the main work-order path first. Optional exploration and hidden branches can be deepened later, but this pass fixes the reported Stage 1/2 interaction shape and Kernel-Mind reply contract.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
