# LLM Stream Contracts

## Scenario: Onboarding vs Gameplay LLM Modes

### 1. Scope / Trigger

- Trigger: frontend CLI can call the backend LLM stream during both onboarding and formal gameplay.
- Risk: if both phases share prompt context, onboarding trainer content can pollute Kernel-Mind gameplay context or reveal later puzzle/lore details.

### 2. Signatures

- Endpoint: `POST /api/llm/stream`
- Frontend context builder: `buildLlmContext(options)` in `index.html`
- Backend prompt router: `event_mode(context)` and `build_chat_messages(context)` in `kernel_ghost_server.py`

### 3. Contracts

Common request fields:

- `eventName: string` determines prompt mode.
- `operatorName: string`
- `stage: number`
- `cwd: string`
- `command: string`
- `userMessage?: string`
- `recentLines: string[]`
- `recentEntries: { kind: string, text: string }[]`
- `lastCommand: string`
- `lastCommandOutput: string[]`

Onboarding-only request fields:

- `eventName: "onboarding_help"`
- `onboardingStep: number`
- `onboardingExpectedCommand: string`

Mode mapping:

- `onboarding_help` -> Brasch onboarding prompt.
- `manual_ai_chat` -> Kernel-Mind manual chat prompt.
- `confirmed_ai_help` -> Kernel-Mind confirmed-help prompt.
- `proactive_after_command` -> Kernel-Mind proactive prompt.
- Any other event -> Kernel-Mind story-flavor prompt.

### 4. Validation & Error Matrix

- Missing or unknown `eventName` -> backend falls back to story mode.
- `onboarding_help` with missing `onboardingExpectedCommand` -> Brasch may answer generally, but must stay within Linux onboarding scope.
- LLM disabled/unconfigured -> `/api/llm/stream` returns service unavailable; frontend must use deterministic fallback lines.
- Provider stream error -> backend emits SSE `error`; frontend must remove empty stream lines and use fallback lines.

### 5. Good/Base/Bad Cases

- Good: Level 1 player asks `ai_chat ls 是什么意思？`; frontend sends `eventName: "onboarding_help"` and `onboardingExpectedCommand: "ls"`; backend uses Brasch prompt.
- Base: Formal stage one player asks `ai_chat 这个 ERROR 是什么？`; frontend sends `eventName: "manual_ai_chat"`; backend uses Kernel-Mind stage-one policy.
- Bad: Formal gameplay context includes Brasch training transcript in `recentLines` or `lastCommandOutput`.

### 6. Tests Required

- Backend test asserts `event_mode({"eventName": "onboarding_help"}) == "onboarding"`.
- Backend test asserts onboarding prompt names Brasch, forbids Kernel-Mind identity, and blocks formal game answers.
- Frontend test asserts onboarding `ai_chat` sends `eventName: "onboarding_help"` and includes onboarding step/expected command fields.
- Frontend test asserts `startWorkOrdersAfterOath()` clears terminal transcript and command history before `screen: "playing"`.

### 7. Wrong vs Correct

#### Wrong

```js
// Sends onboarding questions through the gameplay prompt.
requestLlmFlavor({ eventName: "manual_ai_chat", userMessage: message });
```

This lets Kernel-Mind answer beginner training questions and can leak gameplay tone, stage rules, or lore constraints.

#### Correct

```js
requestLlmFlavor({
  eventName: "onboarding_help",
  userMessage: message,
  fallbackLines: [{ kind: "ai", text: "Brasch: 当前步骤输入 pwd。" }]
});
```

This routes the request to Brasch and keeps onboarding separate from formal gameplay.

#### Wrong

```js
// Starts stage one while preserving onboarding transcript.
state = { ...state, screen: "playing", stage: 1 };
```

Kernel-Mind can receive onboarding transcript through recent terminal context.

#### Correct

```js
elements.terminalLog.textContent = "";
commandHistory.splice(0, commandHistory.length);
historyIndex = -1;
state = { ...state, screen: "playing", stage: 1 };
```

Formal gameplay starts with a clean CLI context after the oath.
