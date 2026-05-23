# Interactive-Space Offline H5 Works

> Delivery contract for uploadable offline H5 works built for interactive-space
> creation requests.

---

## Scope

Apply this spec when the deliverable is an interactive-space work and any of
these are true:

- The user asks for an interactive-space work, offline H5 interactive content,
  or an uploadable H5 work.
- The deliverable is a single `index.html` or a `.zip` whose root contains an
  H5 entry file.
- The work must run without network access and with all resources bundled
  locally.

Do not treat this as the default spec for ordinary marketing pages, content
sites, backend-connected web apps, multiplayer web apps, mini-programs, or
native applications. Those need their own frontend and product constraints.

## Default Delivery

When the user does not override the implementation shape:

- Prefer one self-contained `index.html`.
- Prefer portrait orientation.
- Build a minimal playable work before adding decorative complexity.
- Prefer DOM and CSS when the interaction does not require a Canvas game loop.
- Use original generic visuals instead of recognizable IP, logos, music,
  portraits, fonts, or branded assets.
- Include start, restart, score/status, end-state, error fallback, and
  high-score persistence when they fit the work.
- Do not add audio unless the user asks for it.

## Artifact Contract

### Entry And Packaging

- The entry file is always `index.html`.
- A single-file deliverable is one `.html` file.
- A multi-file deliverable is a directory that can be zipped as-is; after
  extraction, the zip root must directly contain `index.html`.
- The complete deliverable must stay below 8 MB.
- Multi-file assets must be referenced with relative paths.
- Do not ship wrapper directories, `__MACOSX`, build cache, or unrelated files
  in the upload package.

Recommended structures:

```text
index.html
```

```text
/
|-- index.html
|-- js/
|   `-- main.js
|-- images/
|   |-- bg.png
|   `-- icon.png
`-- audio/
    `-- bgm.mp3
```

### Offline Boundary

An interactive-space work is local-only:

- Bundle every image, font, script, stylesheet, library, and audio asset in the
  deliverable.
- Do not reference CDN files, remote images, remote fonts, remote scripts, or
  remote stylesheets.
- Do not use `fetch`, `XMLHttpRequest`, `axios`, `WebSocket`, SSE, or dynamic
  remote script loading.
- If a third-party library is necessary, vendor it into the deliverable and
  reference it locally.

### Navigation Boundary

The work must keep the user inside the delivered work:

- Do not embed `<iframe>`.
- Do not guide users to outside sites.
- Do not use outbound links or external navigation via `<a>`,
  `window.location`, `location.href`, or `window.open`.

## Implementation Rules

### Platform-Safe Code

- Use stable HTML5, CSS3, and ES6+ behavior compatible with WebKit-based mobile
  environments.
- Do not use `eval`, `new Function`, remote code injection, or unsafe HTML
  string assembly.
- Prefer `addEventListener` from script over `onload`, `onclick`, `onerror`,
  `ontouchstart`, and other inline `onXXX` attributes.
- Prefer `requestAnimationFrame` for animation work.
- Prefer Pointer or Touch interaction for primary mobile controls, then add
  mouse compatibility when useful.

### Mobile Layout And Input

- Choose exactly one target orientation for a work. Use portrait by default.
- Fit mainstream mobile screens without horizontal scrolling.
- Account for safe areas, DPR differences, and differing aspect ratios.
- Keep game state, controls, score text, and action buttons readable and
  tappable on small screens.
- If audio exists, playback must start from a user gesture.
- Avoid fixed-pixel layouts that crop the core work on phones.

### Runtime State

- State changes must be recoverable. A failure, pause, win, loss, or exhausted
  move set cannot leave the user without a next action.
- Use `localStorage` only when persistence is needed.
- Prefix every `localStorage` key with a work-specific business prefix.
- Avoid unnecessary repainting, oversized textures, particle floods, and layout
  thrash. Target stable behavior at 30 FPS or better on mainstream mobile
  devices.

### Error Fallback

Every work needs a visible failure fallback instead of a blank page.

```javascript
window.addEventListener('load', () => {
  try {
    initApp();
  } catch (error) {
    console.error(error);
    const fallback = document.createElement('div');
    fallback.style.cssText =
      'position:fixed;inset:0;display:flex;align-items:center;' +
      'justify-content:center;background:#fff;color:#111;font-size:18px;' +
      'padding:24px;text-align:center;z-index:9999;';
    fallback.textContent = 'Something went wrong. Restart and try again.';
    document.body.innerHTML = '';
    document.body.appendChild(fallback);
  }
});
```

## In-Work Modal Contract

Browser-native blocking dialogs are forbidden:

- Do not call `alert()`, `confirm()`, `prompt()`, or `print()`.
- Render tips, confirmations, input, pause states, wins, losses, and settlement
  states inside DOM or Canvas owned by the work.
- Keep only one primary modal screen active at a time.
- Drive visibility and input freezing with explicit state such as
  `currentScreen`, `isPaused`, or `canInput`.

Prefer a full-screen overlay and card-like modal body:

```html
<div id="screen-win" class="screen" aria-hidden="true">
  <div class="modal-card" role="dialog" aria-modal="true"
       aria-labelledby="screen-win-title">
    <h2 id="screen-win-title" class="modal-title">Challenge cleared</h2>
    <p class="modal-message">You won this round.</p>
    <div class="modal-actions">
      <button type="button" data-action="restart">Restart</button>
      <button type="button" data-action="next">Next</button>
    </div>
  </div>
</div>
```

Hide modal screens by default with visibility, opacity, and pointer-event state.
Show them by toggling classes and updating accessibility state:

```javascript
function hideAllScreens() {
  document.querySelectorAll('.screen').forEach((node) => {
    node.classList.remove('active');
    node.setAttribute('aria-hidden', 'true');
  });
}

function showScreen(id) {
  hideAllScreens();
  const target = document.getElementById(id);
  if (!target) return;
  target.classList.add('active');
  target.setAttribute('aria-hidden', 'false');
}
```

Modal minimums:

| Case | Required behavior |
| --- | --- |
| Tip | Use an in-work message region and button or non-blocking toast. |
| Confirm | Render explicit primary and secondary actions. |
| Input | Put an `input`, `textarea`, or in-work input component in the modal. |
| Settlement | Show outcome, score/result, and next action controls. |
| Pause | Provide resume and relevant restart/exit controls with recoverable state. |

## Content Safety

Do not generate or package interactive-space work content that includes:

- Illegal, extremist, gambling, fraudulent, pornographic, cult, or unsafe
  content.
- Inappropriate minor-related content such as dangerous imitation guidance,
  school bullying, or tobacco/alcohol encouragement.
- Unauthorized characters, logos, trademarks, music, fonts, images, likenesses,
  names, or personal data.
- Discriminatory, inflammatory, conspicuous-consumption, or conflict-baiting
  messaging.
- Forced sharing, forced following, off-platform transactions, download
  steering, ads, QR codes, external contact details, or traffic diversion.

If a requested work conflicts with this section or with the offline/platform
boundaries above, stop the conflicting implementation and offer a compliant
direction.

## Verification Checklist

Before reporting a delivered interactive-space work as ready, verify:

- [ ] `index.html` is at the deliverable root.
- [ ] No network request path exists.
- [ ] No external resource reference exists.
- [ ] No outbound navigation or `<iframe>` exists.
- [ ] No browser-native dialog call exists.
- [ ] Any modal UI is rendered by the work itself.
- [ ] Only one primary modal screen can be active at a time.
- [ ] All bundled assets use relative paths.
- [ ] The target orientation and mobile sizes are handled without horizontal
      overflow.
- [ ] A visible error fallback exists.
- [ ] Persistent state, when present, uses prefixed `localStorage` keys only.
- [ ] Estimated package size stays below 8 MB.
- [ ] Content passes the safety section above.

## Common Failure Modes

| Failure | Likely cause | Required correction |
| --- | --- | --- |
| Upload says the entry is missing | `index.html` is not at zip root | Repackage from the directory that directly contains `index.html`. |
| White screen | Runtime error or broken asset path | Add fallback handling and fix local relative paths. |
| Missing visuals/audio | Remote URL or absolute path | Bundle the resource and reference it locally. |
| Oversized package | Heavy images, audio, or libraries | Compress assets and remove non-essential payload. |
| Phone UI crops | Fixed layout or missing orientation strategy | Make layout responsive or scale Canvas to target screens. |

