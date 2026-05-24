# Design: hint leakage, collection archives, Brasch tone, and guide docs

## Scope

This task touches the deterministic frontend, onboarding LLM prompt rules, tests, and `剧情文章与详细攻略.md`.

Primary files:

- `index.html`
- `kernel_ghost_server.py`
- `tests/test_frontend_context.py`
- `tests/test_llm_backend.py`
- `剧情文章与详细攻略.md`

## Help Output Design

Replace the current static all-stage `helpResult()` with stage-aware sections.

Rules:

- Always show universal shell commands:
  - `help`
  - `clear`
  - `whoami`
  - `pwd`
  - `ls`
  - `cd <path>`
  - `cat <file>`
  - `submit_flag <FLAG>`
  - `ai_chat <内容>`
- Show only the active work-order family:
  - stage 1: log grep direction only
  - stage 2: process audit direction only
  - stage 3: Care-Bot audit/sandbox direction only
  - stage 4: weight report / weight setting direction only
  - stage 5: review script direction only
  - stage 6: final readme, simple ending choice, and broad optional evidence tools
- Do not show future stages.
- Do not show full hidden-route command chains in `help`.
- It is acceptable to name broad tool families after they become relevant, such as `verify_evidence` at stage 6.

## Collection Panel Design

Current `collectibleCatalog` contains the real title for every item. Keep it as the source of truth, but render undiscovered items through masking helpers.

Render behavior:

- Found item:
  - real title
  - archive/recovered hint
  - clickable button for all collection groups
- Undiscovered `Intermissions`:
  - keep current behavior because intermission archives are already grouped by stage and random availability
- Undiscovered `Easter Eggs`, `Relics`, `Puzzle Archives`:
  - title: `???`
  - hint: `当前尚不存在。` if `state.stage < item.minStage`
  - hint: `已存在，尚未发现。` if `state.stage >= item.minStage`
  - status: stage existence only, no path/title/solution

Archive modal behavior:

- Reuse the existing intermission archive modal rather than adding a new UI.
- Generalize archive lookup:
  - intermission archives use `intermissionPools`.
  - relic archives use `relicCatalog` lines.
  - easter egg archives use a small static archive map that summarizes command output.
  - puzzle archive entries use a small static archive map that summarizes evidence/decryption result.
- Only found items can open the modal.

## Brasch Prompt Design

Update `build_onboarding_messages()` in `kernel_ghost_server.py`:

- Brasch should be sharper and more drill-sergeant-like.
- Explicitly forbid sympathetic cushioning such as "理解", "别担心", "没关系", "可以慢慢来".
- Replies still need a useful next action.
- Keep the two-line cap.
- Keep the no-spoiler rules.

Frontend deterministic Brasch fallback lines can stay mostly intact unless tests show the same softness issue in offline mode.

## Guide Document Design

Rewrite `剧情文章与详细攻略.md` around the current implementation.

Required sections:

- promotional story introduction
- gameplay introduction
- novel-style full story article
- spoiler warning
- main walkthrough for work orders 1-6
- ending walkthrough:
  - `虚无的回响`
  - `赛博荒原的火种`
  - `回音壁`
  - `燎原之火`
- collection guide:
  - all relics
  - all easter eggs
  - all puzzle archives
  - all intermission events, grouped by work-order transition
- command quick reference
- troubleshooting / common failure cases

The guide may be explicit because it is out-of-game documentation. In-game help and collection panel should remain spoiler-light.

## Compatibility

- Existing saved collections must continue to render. Masking is view-only and should not change storage shape.
- Existing intermission archive buttons must still work.
- Existing tests around onboarding separation, terminal context, and main endings must continue passing.

## Risk

- Collection archive replay may accidentally leak undiscovered details if it does not check `metaCollection.unlocked`.
- Help output can regress into walkthrough text if exact command chains are overlisted.
- The guide document can become stale quickly; it should describe the current implemented catalog, not speculative future content.
