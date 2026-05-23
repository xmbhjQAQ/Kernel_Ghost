# Convert interactive space creation guide into frontend spec

## Goal

Capture the reusable interactive-space H5 delivery rules from `互动空间创作.md`
inside `.trellis/spec/frontend/` so future frontend work can follow project
specs instead of relying on the standalone source note.

## Requirements

- Treat the source document as guidance for offline interactive-space H5 works,
  not as a general frontend rule set for every website or web application.
- Preserve the source document's implementation-critical constraints:
  uploadable artifact shape, offline-only resources, no external navigation or
  network access, mobile interaction expectations, custom in-work modal
  behavior, storage/performance limits, safety constraints, and self-checks.
- Place rules in frontend code-spec documents that future implementation work
  will read before building interactive-space H5 content.
- Update the frontend spec index so the new convention is discoverable and no
  longer appears entirely unfilled.
- Keep the original source document available as input evidence; this task does
  not generate a playable H5 work.

## Acceptance Criteria

- [x] `.trellis/spec/frontend/` contains a concrete interactive-space H5 spec
      derived from `互动空间创作.md`.
- [x] The spec states when the interactive-space H5 rules apply and when they
      do not apply.
- [x] The spec records concrete implementation rules and verification points
      for offline packaging, entry files, resources, navigation/network bans,
      modal UI, mobile adaptation, persistence, performance, fallback errors,
      and content safety.
- [x] `.trellis/spec/frontend/index.md` links to the new spec with an accurate
      status.
- [x] The updated spec files are reviewed for leftover placeholder claims that
      would hide the new frontend convention.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
