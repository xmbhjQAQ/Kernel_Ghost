# Implementation Plan

## Checklist

1. Read relevant frontend specs and existing start/event/persistence code.
2. Extend HTML/CSS for:
   - current-foundation registration UI,
   - optional encyclopedia workbench section/control,
   - disabled forced-reading confirm state.
3. Extend initial state, restore normalization, and render logic for foundation/onboarding/oath/encyclopedia fields.
4. Refactor `startShift()` so it stores the operator name and opens foundation registration instead of starting stage one directly.
5. Implement foundation selection handlers:
   - beginner -> terminal onboarding,
   - terminal -> encyclopedia visible + oath,
   - ready -> no encyclopedia + oath.
6. Implement Level 1 Linux-only onboarding command gates and copy.
7. Add optional onboarding LLM Q&A:
   - frontend sends an onboarding-specific event name/context,
   - backend uses a narrow onboarding prompt for strict, caustic coach `Brasch`,
   - fallback stays deterministic when LLM is disabled/unavailable.
8. Implement oath forced-reading mode using the existing event modal.
9. Clear onboarding transcript/command history when oath is accepted so formal CLI/LLM context is isolated.
10. Add encyclopedia rendering and visibility gating.
11. Ensure `help`, restart, hard reset, progress save/restore, and mobile side panel still behave.
12. Add focused tests or update existing frontend tests for the new flow, context isolation, and onboarding LLM prompt separation.
13. Run validation:
    - inline script syntax check,
    - `python -m pytest`,
    - browser smoke test if feasible.
14. Commit changes.

## Validation Commands

- `node -e "const fs=require('fs'); const html=fs.readFileSync('index.html','utf8'); const script=html.match(/<script>([\\s\\S]*)<\\/script>/)[1]; new Function(script); console.log('index.html script syntax ok');"`
- `python -m pytest`

## Risk Points

- Reusing the event modal for both forced oath and archived intermissions can accidentally leave the confirm button disabled. Reset oath-mode state every time an intermission is shown.
- Persisted progress from older versions may lack new fields. Normalize every new field.
- Onboarding commands must not interfere with existing stage-one command semantics after onboarding ends.
- The encyclopedia should be hidden for Level 3 even after restart/restore unless the player selected Level 1 or Level 2 in the current save.
- The existing Kernel-Mind prompt is stage-specific; onboarding Q&A should not route through the exact same prompt without an onboarding mode guard.
- If the terminal transcript is not cleared at the handoff, Kernel-Mind can receive Brasch tutorial lines as recent context. Clear transcript and command history at `startWorkOrdersAfterOath()`.

## Rollback

If the new intake flow breaks existing gameplay, revert the intake-specific changes and restore `startShift()` to directly initialize `screen: "playing"`, `stage: 1`, and `ticket: "stage1"`.
