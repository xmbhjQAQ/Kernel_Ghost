# Implementation Plan

## Batch 1: Stage-Scoped Help

- [x] Replace static `helpResult()` output with helper-driven stage-specific output.
- [x] Keep universal commands visible.
- [x] Add one short active-stage line based on `state.stage` / `state.screen`.
- [x] Keep stage 6 optional evidence hints broad and non-walkthrough.
- [x] Add frontend tests that stage 1 help does not include later-stage commands.

Validation:

```bash
node -e "const fs=require('fs'); const html=fs.readFileSync('index.html','utf8'); const script=html.match(/<script>([\s\S]*)<\/script>/)[1]; new Function(script); console.log('index.html script syntax ok');"
python -m pytest tests/test_frontend_context.py
```

## Batch 2: Masked And Clickable Collections

- [x] Update `renderDiscoveries()` so all found collectibles are rendered as buttons.
- [x] Keep undiscovered non-intermission titles as `???`.
- [x] Change `collectionHint()` / `collectionStatus()` to avoid undiscovered spoilers.
- [x] Generalize archive modal opening:
  - [x] keep intermission lookup
  - [x] add relic lookup
  - [x] add easter egg / puzzle archive summary lookup
- [x] Add tests for hidden labels and clickable found non-intermission entries.

Validation:

```bash
python -m pytest tests/test_frontend_context.py
```

## Batch 3: Brasch Tone

- [x] Update `build_onboarding_messages()` to forbid soft empathetic cushioning.
- [x] Keep strict Linux-training utility and no-spoiler rules.
- [x] Update backend prompt tests to assert the stricter tone contract.

Validation:

```bash
python -m pytest tests/test_llm_backend.py
```

## Batch 4: Guide Document

- [x] Rewrite `剧情文章与详细攻略.md` to match the current six-stage game.
- [x] Include promotional story intro and gameplay intro.
- [x] Include novel-style story article.
- [x] Include detailed walkthrough for mainline, endings, every collection category, intermissions, and common failures.
- [x] Ensure current implemented item names and commands are covered.

Validation:

```bash
rg -n "宣传|玩法|虚无的回响|赛博荒原的火种|回音壁|燎原之火|Relics|Easter Eggs|Puzzle Archives|Intermissions" "剧情文章与详细攻略.md"
```

## Batch 5: Final Verification

- [x] Run JavaScript syntax validation.
- [x] Run full pytest.
- [x] Review git diff for unrelated dirty files.
- [ ] Commit and push only this task's files.

Validation:

```bash
python -m pytest
git status --short
```
