# Brainstorm — lens: capability map

- **Run user journeys as verify commands (`fm flow`)** — FEATURE — value 5 — effort L — risk med — category: UI verify
  Why: assumption: `fm shot` and the "browser ladder" capture still frames, but a UI task can't yet prove a click-through (open menu, fill form, see the toast) like Playwright or Cypress does.
  Done when: a `.flow` file of goto/click/type/expect steps runs headless, exits non-zero on a failed expect, and leaves a trace plus per-step screenshots.

- **Render a component state matrix (`fm stories`)** — FEATURE — value 5 — effort M — risk low — category: UI verify
  Why: Storybook and Chromatic show every component × state × theme × viewport. The pack has empty/loading/error ideas and golden frames, but no single contact sheet that works for web components and TUI widgets.
  Done when: one command writes a sheet covering default, hover, focus, disabled, empty, loading and error states in each theme, and a missing state fails the check.

- **Annotate a screenshot to file scoped tasks** — FEATURE — value 4 — effort M — risk low — category: feedback loop
  Why: the user's complaints are visual ("not like that"). Figma comments and Marker.io pin feedback to a spot; the pack has margin notes for events but nothing for screenshots.
  Done when: clicking a region on a saved screenshot creates a task holding the element selector, crop, viewport and note, and the task's verify re-shoots that region.

- **Gate web pages on a weight and vitals budget** — FEATURE — value 4 — effort M — risk low — category: perf
  Why: Lighthouse budgets are standard. The pack covers a motion budget linter and a TUI paint budget, but nothing for page bytes, font and image weight, CLS or long tasks on generated sites.
  Done when: `fm check web-budget` fails a page whose bytes, layout-shift score or main-thread block time exceed `.foreman` limits, and the output names the offending asset.

- **Lint CSS architecture (`fm check css`)** — CLEAN — value 3 — effort S — risk low — category: UI verify
  Why: the pack checks tokens and slop tells, but not the structural debt generated CSS accumulates.
  Done when: a report lists unused selectors, `!important` count, specificity spikes, a z-index map and hardcoded colours outside tokens, with a ratchet against regressions.

- **Forge a consistent icon family** — FEATURE — value 4 — effort M — risk low — category: design assets
  Why: generated UIs mix icon sets, or draw ad-hoc SVGs with varying stroke widths. No icon or illustration capability appears in the pack's playbooks or cards.
  Done when: a grid spec (size, stroke, corner radius) generates or lints a set of SVG icons, and any icon off-grid or off-stroke is flagged.

- **Write a scrollytelling playbook with a scrub checker** — FEATURE — value 4 — effort M — risk med — category: motion playbook
  Why: the pack proposes a scroll-scrubbed hero for the site only. A general playbook for pinned scenes, scroll timelines and reduced-motion fallbacks is a separate gap.
  Done when: the playbook ships a template plus a check that the page stays usable with motion off, with scroll disabled and at three viewports.

- **Inject a 3D dev HUD** — FEATURE — value 3 — effort M — risk low — category: 3D
  Why: three.js stats panels and spector.js show draw calls, triangles and texture memory. The pack has a 3D perf budget but no live inspector.
  Done when: a dev-only overlay shows draw calls, triangles, texture MB and frame time against budget lines, and the same numbers are exposed to `fm shot` for gating.

- **Write a docs-writing playbook with a structure check** — FEATURE — value 3 — effort S — risk low — category: playbook
  Why: the pack plans to run the docs' commands and cold-read the README, but has no guidance on how Claude should structure docs (tutorial, how-to, reference, explanation).
  Done when: a playbook exists and a check flags pages that mix the four kinds, and orphan pages or dead anchors.

- **Write a UI sound playbook for the web** — FEATURE — value 2 — effort S — risk low — category: motion playbook
  Why: assumption: only terminal bells appear in the pack. A short WebAudio playbook (synthesised tones, muted by default, respects user settings) completes "motion that explains state" for browsers.
  Done when: a template plays distinct synthesised cues for success, error and tap, and a check confirms there is no autoplay and a mute control exists.

- **Replay a recorded UI session beside the task timeline** — FEATURE — value 4 — effort L — risk med — category: debug (wild)
  Why: wild: an rrweb-style recorder for the page under construction, so "it glitched when I did X" becomes a scrubbable repro attached to a task.
  Done when: a recorded session replays deterministically in a headless browser and a failing assertion at a chosen timestamp becomes the task's verify.

- **View glTF models in the terminal (`fm view`)** — FEATURE — value 3 — effort M — risk low — category: 3D (wild)
  Why: wild: the pack proposes a stdlib software rasteriser for the TUI. Pointing it at any `.glb` lets a user eyeball a generated 3D asset over ssh with no browser.
  Done when: `fm view model.glb` orbits the model with arrow keys at ≥10 fps on a 120×40 terminal, and a bad file reports a clear error.

- **Generate a project wordmark typeface** — FEATURE — value 2 — effort L — risk med — category: design assets (wild)
  Why: wild: non-generic styling needs a distinctive mark. A procedural display face built from stroke-axis parameters, with the glyphs the title needs, gives the site, TUI banner and receipts a signature.
  Done when: a command emits an SVG wordmark and subset font from a seed, and the same seed reproduces identical output.
