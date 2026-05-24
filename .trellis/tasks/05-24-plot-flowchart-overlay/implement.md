# Plot Flowchart Overlay Implementation Plan

## Checklist

- [x] Read frontend implementation spec before editing.
- [x] Add route-map button CSS and responsive positioning below the guidebook
  button.
- [x] Add route-map modal markup and route-map container.
- [x] Add `plotArchive` load/save helpers with ID filtering.
- [x] Add static `plotRouteCatalog` and derivation helpers:
  - current node/ending detection
  - route visibility/masking
  - next-unlock hint generation
- [x] Wire `cacheElements()` and `bindEvents()` for opening/closing the modal.
- [x] Update `renderState()` and reset flow so route knowledge updates and
  clears correctly.
- [x] Add focused frontend tests for:
  - route-map control/modal wiring
  - persistent archive load/save/reset behavior
  - hidden branch masking with `???`
  - current position derivation
- [x] Run frontend tests.
- [x] Run a browser smoke test or equivalent syntax check for `index.html`.
- [ ] Commit changes after verification.

## Validation Commands

```bash
python -m pytest tests/test_frontend_context.py
node -e "const fs=require('fs'); const html=fs.readFileSync('index.html','utf8'); const script=html.match(/<script>([\\s\\S]*)<\\/script>/)[1]; new Function(script); console.log('index.html script syntax ok');"
git status --short
```

## Risky Files and Rollback Points

- `index.html`: large single-file frontend. Keep changes grouped by existing
  CSS, markup, and script sections.
- `tests/test_frontend_context.py`: string-based tests can become brittle; keep
  assertions focused on stable function names and critical behavior.

Rollback point: if route-map derivation touches too much command logic, revert
to a pure read-only renderer based on existing state and only persist reached
ending IDs.

## Review Gate

Before starting implementation, confirm the plan with the user:

- Cross-playthrough route knowledge persists.
- Ordinary stage-six endings become visible once stage six is reached.
- Hidden endings stay `???` until their prerequisite route is exposed or ending
  is reached.
- Full reset clears route knowledge.
