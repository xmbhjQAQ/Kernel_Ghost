# Implementation Plan

- [x] Read `过渡事件（重写）.md` and map its five sections into `intermissionPools`.
- [x] Replace existing pool text in `index.html`.
- [x] Add pool 5 and ensure #005 completion triggers it.
- [x] Update tests for five-pool intermission coverage.
- [x] Run syntax check and relevant pytest.
- [ ] Commit and push.

## Validation Commands

- `node -e "const fs=require('fs'); const html=fs.readFileSync('index.html','utf8'); const script=html.match(/<script>([\\s\\S]*)<\\/script>/)[1]; new Function(script); console.log('index.html script syntax ok');"`
- `python -m pytest tests/test_frontend_context.py tests/test_llm_backend.py`
