# Implementation Plan

## Checklist

- [x] Add frontend tickets, state fields, virtual files, help text, and command dispatch for work orders #003 and #004.
- [x] Implement Care-Bot deterministic command functions and flag transition.
- [x] Implement Collective Mind weight deterministic command functions and flag transition.
- [x] Renumber comment anomaly code paths from stage #003 to #005.
- [x] Renumber final escape / ending code paths from stage #004 to #006.
- [x] Update stage labels, patience display threshold, collection names, and intermission trigger points.
- [x] Update backend LLM stage policy and fixed prompt text for stages #003-#006.
- [x] Update tests for frontend stage flow and backend policy.
- [x] Run frontend syntax check and relevant Python tests.
- [ ] Commit the completed task changes after verification.

## Validation Commands

- `node -e "const fs=require('fs'); const html=fs.readFileSync('index.html','utf8'); const script=html.match(/<script>([\\s\\S]*)<\\/script>/)[1]; new Function(script); console.log('index.html script syntax ok');"`
- `python -m pytest tests/test_frontend_context.py tests/test_llm_backend.py`

## Risky Files

- `index.html`: central frontend state machine and persistence.
- `kernel_ghost_server.py`: stage-aware LLM prompt policy.
- `tests/test_frontend_context.py`, `tests/test_llm_backend.py`: source-contract tests may need stage expectation updates.

## Rollback Points

- Before changing backend policy, verify frontend stage mapping is internally consistent.
- Before committing, inspect `git diff` to avoid including unrelated user changes except files required by this task.
