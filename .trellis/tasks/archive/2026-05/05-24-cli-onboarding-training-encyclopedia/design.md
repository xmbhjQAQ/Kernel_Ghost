# Design: CLI Onboarding Training and Encyclopedia Gating

## Architecture

Implement the feature inside the existing single-file frontend (`index.html`):

- Extend the existing intro modal from a one-step name entry into a small intake flow.
- Keep the terminal as the primary tutorial surface. Do not introduce a separate tutorial page.
- Reuse the existing `eventScreen` modal for the oath, but add a forced-scroll mode so the confirm button can be disabled until the content reaches the bottom.
- Add a right-panel encyclopedia control/section that is shown only when `state.encyclopediaVisible` is true.
- Preserve the existing stage-one start behavior behind a new function that starts the actual night-shift work order after onboarding and oath completion.
- Treat onboarding and formal work orders as separate CLI contexts. When the oath is accepted, clear the terminal transcript and command history before stage one starts so Kernel-Mind never receives Brasch training lines through `recentLines`, `recentEntries`, `lastCommand`, or `lastCommandOutput`.

## State Model

Add state fields to `createInitialState()`:

- `foundation`: empty string or one of `beginner`, `terminal`, `ready`.
- `onboardingStatus`: `not_started`, `in_progress`, `complete`, or `skipped`.
- `oathAccepted`: boolean.
- `encyclopediaVisible`: boolean.

Restore normalization should preserve these fields and default older saves safely.

Recommended screen flow:

1. `intro`: name input.
2. `foundation`: current-foundation registration.
3. `onboarding`: Level 1 Linux-only CLI onboarding, if selected.
4. `oath`: forced-reading oath event.
5. `playing`: existing stage-one work order flow.

Existing saves with `screen: "playing"` or `screen: "ending"` should continue to restore to those screens.

## Flow Contracts

### Name Entry

`startShift()` should no longer directly start stage one. It should sanitize and save the operator name, then show the foundation registration UI.

### Foundation Registration

Foundation choices set:

- `beginner`: onboarding in progress, encyclopedia hidden until onboarding completes.
- `terminal`: onboarding skipped, encyclopedia visible, then oath.
- `ready`: onboarding skipped, encyclopedia hidden, then oath.

### Level 1 Onboarding

Use terminal lines and a simple command-gated checklist for Linux basics:

- `pwd`: confirm current directory.
- `ls`: inspect current directory.
- `cd tickets`: enter a directory.
- `cat intro.txt` or equivalent training file: read an onboarding file.

Keep cryptography copy high-level: mention that later work may involve encoding/encryption/hash/RSA, and direct the player to the encyclopedia after onboarding.

Allow optional natural-language questions during onboarding. The onboarding assistant is named `Brasch`: a strict, caustic Chronos onboarding coach who answers with pressure and impatience, but still gives actionable Linux training help. The frontend can route `ai_chat <question>` or a dedicated onboarding help command through the existing LLM streaming endpoint, but the backend should recognize an onboarding event/mode and use a narrower prompt.

Do not reuse the current gameplay prompt unchanged for onboarding. The current prompt assumes Kernel-Mind stage gameplay, Flag secrecy, Lin reveal pacing, and proactive threat/lost behavior. Reusing the transport is safe; reusing the full prompt is likely to leak tone and constraints into beginner training.

### Oath

The oath is a modal forced-reading event:

- Title: `入职宣誓`.
- Source/time should match Chronos HR/compliance flavor.
- Confirm button disabled until scrolled to bottom.
- On confirmation, call the stage-one start function.

### Encyclopedia

Add a side-panel workbench control/section visible when `state.encyclopediaVisible` is true. It should include:

- Encoding and decoding lookup notes.
- Hash concept notes.
- Classical cipher concept notes.
- RSA concept notes.
- Linux command usage examples relevant to the game.

Keep it concise and reference-style. It is a lookup control, not a tutorial replacement.

## Compatibility

- Existing localStorage saves should normalize without throwing.
- Hard reset clears all progress and returns to name entry.
- Restart without clearing collection should still return to name entry and preserve collection.
- Existing collection rendering and intermission replay must keep working.
- Existing stage progression, flags, and endings should not change.
- The existing gameplay LLM prompt should remain behaviorally stable for stages 1-4.
- Onboarding LLM mode should degrade to deterministic local guidance if the backend is unavailable.
- Onboarding LLM output should identify as `Brasch` when an assistant name is needed, never Kernel-Mind.
- Brasch should be harsh in tone without teaching unsafe content, spoiling later game answers, or refusing ordinary beginner Linux questions.
- Formal gameplay LLM context should start after the oath and must not include onboarding transcript or command history.

## Trade-Offs

- Keeping the onboarding in the same terminal preserves immersion and avoids a separate UI surface.
- A concise encyclopedia reduces overload but may not fully teach complex cryptography; this matches the requirement that cryptography is not taught in the beginner tutorial.
- Reusing `eventScreen` for the oath limits markup churn but requires careful mode cleanup so normal intermission archive behavior is not affected.
- Reusing the LLM transport minimizes frontend/backend surface area, but a separate onboarding prompt avoids tutorial answers being polluted by stage-specific Kernel-Mind lore and Flag policies.
