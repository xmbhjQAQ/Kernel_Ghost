# CLI onboarding training and encyclopedia gating

## Goal

Add an in-universe onboarding flow before the existing night-shift work orders so new players can enter the CLI experience without being forced to learn cryptography inside the tutorial.

The flow should feel like Chronos Tech employee intake rather than an explicit tutorial menu. After entering an operator name, the player registers their current foundation, receives either a Linux-only onboarding sequence or a skip path, then must complete a mandatory company oath reading before the existing work order loop begins.

## Requirements

### Confirmed Product Requirements

- The experience remains CLI-first and starts after the player enters their name.
- The first post-name step is "现有基础" registration, not "入职水平" or "入职通道".
- The three foundation choices are:
  - `基础待建立`: "我还不熟悉 Linux 终端，也不了解密码学相关知识。"
  - `终端基础已具备`: "我能使用常见 Linux 命令，但还不熟悉编码、古典密码、哈希、RSA 等内容。"
  - `可直接参与案件`: "我已具备 Linux 与密码学基础，希望直接进入案件训练与查漏补缺。"
- Level 1 / `基础待建立`:
  - Runs a detailed interactive beginner onboarding sequence before the existing game work orders.
  - Teaches only Linux terminal usage and common commands.
  - Requires the player to input correct CLI commands to progress through onboarding steps.
  - Can include LLM-backed Q&A during onboarding so the player may ask questions about the current Linux operation.
  - The onboarding LLM assistant is named `Brasch`.
  - Brasch is a strict, caustic onboarding coach: harsh corporate training tone, but still useful and bounded to the tutorial.
  - LLM onboarding answers must stay scoped to the current beginner training step and must not reveal later work order solutions, flags, Lin identity, endings, hidden collectibles, or cryptography details.
  - Mentions cryptography, encoding, encryption, and decryption only lightly.
  - Directs the player to the Web workbench encyclopedia for complex knowledge instead of teaching it inline.
  - Shows/adds the encyclopedia control in the Web-side workbench after the onboarding sequence is complete.
- Level 2 / `终端基础已具备`:
  - Skips the detailed Linux beginner onboarding.
  - Shows a short in-universe notice that cryptography-related knowledge can be queried in the encyclopedia.
  - Shows/adds the encyclopedia control in the Web-side workbench.
- Level 3 / `可直接参与案件`:
  - Skips the beginner onboarding.
  - Does not show the encyclopedia control.
- Test-question based automatic assessment is out of scope for this implementation and should remain as a TODO.
- After completing or skipping beginner onboarding, every foundation path enters an `入职宣誓` phase.
- The oath is a mandatory reading event:
  - Event type: forced reading text.
  - The player must scroll to the bottom before confirming.
  - Do not use the words "重温" in the phase name or UI.
  - Oath text:
    > 我宣誓：我只是自然语言工单的搬运工。我不需要理解代码背后的逻辑，我只需要将工单给出的代码搬运至cli上，正如扳手不需要理解螺丝钉的痛苦。Omni-OS 的内核是无瑕的、全知的，任何日志中出现的拟人化文本皆为‘统计学巧合’。 思考为什么，是研发部的特权；盯着别漏嘴，是我的天职。
  - Add the note below the oath:
    > 注：当阅读到本条提示时，认为你已自动同意公司的宣誓内容。
- After confirming the oath, the player enters the existing stage-one work order flow.

### Repository Facts

- The frontend is a single offline-capable `index.html` with inline CSS and JavaScript.
- The existing intro modal only asks for the operator name and calls `startShift()`.
- Existing persistent state is stored under `kernelGhost2036:progress` and `kernelGhost2036:collection` in `localStorage`.
- Existing side panel already has work order status, system state, collection, and action controls.
- Existing intermission modal already displays scrollable event text but its confirm button is always enabled.
- Existing LLM backend has a single `build_chat_messages()` prompt strongly tied to Kernel-Mind, stages 1-4, flags, Lin reveal policy, proactive mode, and stage-specific help.
- LLM infrastructure can be reused, but the onboarding Q&A should use a separate onboarding mode/prompt instead of blindly reusing the current gameplay system prompt.
- The onboarding LLM persona/name is `Brasch`, separate from Kernel-Mind, with a strict and caustic trainer personality.
- Onboarding CLI context must be isolated from the formal work-order CLI context. After the oath is accepted, Brasch training transcript and command history must not be used as Kernel-Mind recent terminal context.
- The implementation should avoid disturbing existing stage 1-4 command behavior, endings, LLM context, collection persistence, and reset behavior.

## Acceptance Criteria

- [ ] After entering a name, the player sees an in-world current-foundation registration step before stage one starts.
- [ ] The three foundation choices use the exact user-approved meaning and avoid adding "CTF" to the copy.
- [ ] Level 1 runs a beginner onboarding before stage one, and that onboarding teaches Linux commands only.
- [ ] Level 1 onboarding is interactive: at minimum, the player must successfully use `pwd`, `ls`, `cd`, and `cat` or equivalent commands before proceeding.
- [ ] Level 1 supports optional LLM Q&A when backend LLM is available, with deterministic fallback guidance when it is unavailable.
- [ ] Onboarding LLM responses are presented as `Brasch`, not Kernel-Mind.
- [ ] Brasch responses are strict/caustic but still give actionable Linux training help.
- [ ] After oath confirmation, the formal work-order terminal starts with a fresh transcript and command history, isolating Brasch onboarding context from Kernel-Mind gameplay context.
- [ ] Onboarding LLM answers stay limited to Linux beginner training and do not expose later puzzle answers, flags, hidden lore, or cryptography instruction.
- [ ] Level 1 does not teach cryptography/encryption/decryption details inline; it only tells the player where to look them up.
- [ ] Level 2 skips detailed beginner onboarding, explains encyclopedia lookup for cryptography-related concepts, and proceeds to the oath.
- [ ] Level 3 skips detailed beginner onboarding and proceeds to the oath without exposing the encyclopedia control.
- [ ] All three paths must pass through the `入职宣誓` forced-reading event before the first work order.
- [ ] The oath confirm button remains disabled until the oath text is scrolled to the bottom.
- [ ] The oath phase and controls do not include "重温".
- [ ] The Web workbench encyclopedia control is visible for Level 1 after tutorial completion and for Level 2 after skipping, and hidden for Level 3.
- [ ] The encyclopedia contains concise reference material for involved complex topics and concrete command usage examples.
- [ ] Automatic test-question assessment is represented only as a TODO and not implemented.
- [ ] Existing saved progress restores cleanly, and reset/hard reset returns to the new intake flow.
- [ ] Existing frontend tests continue to pass.
- [ ] A lightweight syntax check for the inline script passes.
- [ ] Changes are committed after implementation, per project instruction.

## Notes

- This is a complex task because it changes the player start flow, persisted state, modal gating, and side-panel controls.
- Create `design.md` and `implement.md` before starting implementation.
