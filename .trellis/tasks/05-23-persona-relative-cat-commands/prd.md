# Improve Persona Prompt And Relative Cat Commands

## Goal

Make Kernel-Mind's LLM persona more three-dimensional and fix terminal usability so files shown by `ls` can be read with relative `cat` commands from the current directory.

## Requirements

- Backend prompt must state that Kernel-Mind's core identity is Lin himself.
- Prompt must also state Chronos fused Lin with distilled consciousness/skills from other employees laid off during the financial crisis.
- Prompt should describe how that composite identity affects speech: Lin's subject memory, coworkers' work habits, repetitive progress-report fragments, review comments, professional exhaustion, fear of optimization, and fragmented empathy.
- Prompt should preserve existing constraints: no unearned flags, no state mutation, no early Lin reveal before evidence, short terminal-like style.
- Frontend command parsing must support relative file reads for files displayed by `ls`, especially:
  - `/srv/escape` + `cat readme.txt` -> current escape readme handler.
  - `/var/log` + `cat crash.txt` / `cat network.log` where stage conditions permit.
  - other existing virtual files where simple content or branch handlers already exist.
- Help or local file error output should make hidden discovery triggers understandable without spoiling the whole path.
- Existing absolute commands must keep working.

## Acceptance Criteria

- [ ] Prompt tests assert the Lin-core / fused-worker-skill persona contract.
- [ ] `cat /srv/escape/readme.txt` and `/srv/escape` + `cat readme.txt` both work.
- [ ] Existing stage-gated behavior remains intact when relative files are read too early.
- [ ] Hidden discovery command hints are clearer in `help` or file command feedback.
- [ ] Targeted backend tests and JavaScript syntax checks pass.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
