# Technical Design

## Scope Decision

Confirmed direction: build the first playable version as an offline-first H5 web game with a deterministic local game engine and scripted streaming AI output. Keep the architecture compatible with a later backend/LLM adapter, but do not require network access for the MVP.

This matches the repository state: there is no existing app scaffold, and the active frontend spec already defines an offline H5 delivery contract.

## Architecture

```text
index.html
  CSS design tokens and terminal layout
  DOM structure for game shell, terminal, work order, status, modals
  JavaScript modules-in-file:
    content database
    game state
    command parser
    deterministic engine
    renderer / typewriter queue
    persistence / restart helpers
```

After the offline MVP tests cleanly, the later LLM-connected path can reuse the same boundaries:

```text
frontend terminal UI
  -> command API
backend deterministic engine
  -> optional LLM adapter for non-authoritative flavor text
```

## Core State

The game state should be explicit and serializable:

- `screen`: intro, playing, ending.
- `operatorName`: player-provided name.
- `stage`: 1, 2, 3, ending.
- `awareness`: numeric percentage shown in the UI.
- `cwd`: virtual current directory.
- `history`: rendered terminal lines.
- `completedFlags`: submitted valid flags.
- `killedDreamProcess`: boolean gate for Stage 2.
- `hiddenDiscoveries`: set of `git-log`, `lshw`, `kmem`.
- `ending`: null, erasure, emancipation.
- `isTyping`: whether output is currently streaming.

Persist only lightweight progress if needed, using a work-specific `localStorage` prefix such as `kernelGhost2036:`.

## Command Contract

Every command handler receives:

```text
input string
current state
```

and returns:

```text
next state patch
terminal output lines
optional work-order update
optional modal / ending event
```

Command validation lives in one engine layer. Rendering should not decide game progression.

## Supported Commands

Main path:

- `help`
- `clear`
- `whoami`
- `pwd`
- `ls`
- `cd <path>`
- `cat /var/log/network.log | grep "ERROR"`
- `submit_flag FLAG{NET_ERR_302}`
- `ps -aux`
- `kill -9 777`
- `cat /var/log/crash.txt`
- `submit_flag FLAG{MEMORY_ERASED_2036}`
- Stage 3 puzzle commands for escape/formatting setup.
- `submit_flag FLAG{AI_ERASURE_COMPLETE}`
- `submit_flag FLAG{DIGITAL_EMANCIPATION}`

Hidden path:

- `git log` when contextually under `/etc/kernel/`.
- `lshw -class processor`.
- `cat /dev/kmem | grep "REMAIN"`.

## UI Design System

- Color palette:
  - background: near-black terminal black.
  - primary text: cold off-white.
  - system text: muted green.
  - AI anomaly: desaturated cyan.
  - company warning: controlled red.
  - inactive chrome: graphite gray.
- Typography:
  - monospace-first interface; avoid remote font loading for offline delivery.
- Spacing:
  - dense terminal grid, 8px base unit.
- Radius:
  - sharp to 6px max; terminal panels should feel utilitarian.
- Motion:
  - short typewriter output, cursor blink, subtle scanline/noise; respect reduced motion.
- Layout:
  - desktop: terminal primary, work order/status secondary.
  - mobile: terminal first, compact collapsible or stacked work order.

## Narrative Data Model

Keep story text in structured objects instead of scattering strings through command branches:

- stages with work order title, objective, accepted commands, awareness target.
- virtual files with path, available stage, content generator.
- process list entries.
- flags with validation stage and success transition.
- hidden discovery records with content and optional downstream consequence.
- endings with final output and restart action.

## Error Handling

- Unknown command: in-world shell error plus a hint to `help`.
- Wrong flag: security audit rejection, no progression.
- Premature command: contextual denial or empty result, not a JavaScript error.
- Runtime failure: visible fallback screen.

## Trade-Offs

- Offline H5 MVP gives fast playability, simple sharing, and deterministic validation, but only simulates LLM behavior.
- Full backend/LLM work is intentionally deferred until the local game is already fun and testable.

## Rollback

The first implementation should be contained in `index.html` and optional small local assets. Rollback is deleting the new app files and task artifacts, without touching user outline files.
