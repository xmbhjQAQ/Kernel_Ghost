# Add Simulated Escape Analysis Tools

## Goal

Make Stage 3 `ai_help` hints concrete by adding the simulated files and CLI tools it references. Players should be able to try `strings architecture.png`, `tar -xf diagram.cache`, and `binwalk architecture.png` inside the virtual terminal and receive in-world outputs that separate decoys from the real escape path.

## Requirements

- `/srv/escape` must list `architecture.png` and `diagram.cache` in addition to existing files.
- Add a project-bound `architecture.png` asset for the escape architecture map.
- Add deterministic handlers for:
  - `strings architecture.png`
  - `tar -xf diagram.cache`
  - `binwalk architecture.png`
- Tool outputs must be simulated, safe, and in-universe. They must not run real tools or touch real files.
- `binwalk architecture.png` should expose the useful embedded Base64 residue and point toward the existing decode path.
- `strings` and `tar` should produce plausible but clearly limited/noisy output so they function as decoys rather than dead commands.
- `ai_help` output must align with the implemented commands and avoid referencing unavailable files/tools.
- Existing escape path commands and endings must keep working.

## Acceptance Criteria

- [x] `/srv/escape$ ls` includes `architecture.png` and `diagram.cache`.
- [x] `strings architecture.png`, `tar -xf diagram.cache`, and `binwalk architecture.png` return deterministic virtual outputs.
- [x] `binwalk architecture.png` unlocks or clearly reveals the same Base64 residue used by the existing escape decode command.
- [x] `ai_help` references only commands that now exist in the virtual CLI.
- [x] JavaScript syntax check passes.
- [x] Existing backend prompt tests still pass.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
