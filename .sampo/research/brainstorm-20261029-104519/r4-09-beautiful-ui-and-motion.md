# Brainstorm — lens: beautiful UI and motion

- **Play queue items as one card that travels the stages** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: assumption: FLIP covers reorders only. A task is a different element in the list, the pane, and the detail view, so state changes read as jumps. One shared-element card that slides capture → plan → edit → prove → close makes the lifecycle visible.
  Done when: in the web UI, opening a task from the queue animates the same DOM node into the detail view (view-transition name matches), and under `prefers-reduced-motion` it swaps instantly (a Playwright check on both).

- **Show gate progress as a determinate bar with a learned ETA** — FEATURE — value 4 — effort M — risk low — category: loading states
  Why: gates and ship test runs take long, and recent commits show the user cares about them overlapping and hanging. A spinner says nothing. Past run durations per gate are already recorded, so the bar can fill to a median and say "~38s, usually 41s".
  Done when: `fm check` shows a bar whose end time is within 20% of the actual run on a stored fixture history, and a gate with no history shows an indeterminate state.

- **Reserve widths for changing values so nothing jitters** — CLEAN — value 3 — effort S — risk low — category: typography
  Why: assumption: live times, counts and time bars repaint constantly, and a "9s → 10s" or "99 → 100" change shifts neighbouring columns. Use tabular numerals on the web, fixed-width fields in the pane and right-aligned counters.
  Done when: a render test steps a counter from 9 to 1000 and every other column on the row keeps the same x-offset in both the pane and the web UI.

- **Give the pane designed width tiers** — FEATURE — value 4 — effort M — risk med — category: layout
  Why: the demo shows the docked pane beside Claude, so its width is whatever is left. Width-aware truncation and a fuzz test are already listed, but each tier needs its own layout: wide gets lanes and graph, medium gets a stacked summary, narrow gets a one-line status plus the beacon.
  Done when: golden frames at 120, 80, 50 and 30 columns each render a distinct layout with the work bar and the needs-you state still visible.

- **Make the pane mouse-native** — FEATURE — value 3 — effort M — risk med — category: interaction
  Why: assumption: the pane is read-only to the eye. SGR mouse reporting lets a click on a task id focus it, a click on a lane expand it, and a drag reorder the queue. The pane already reports ids that are meant to be clickable.
  Done when: a scripted SGR click on a queue row focuses that task, and a click on empty space does nothing and doesn't leak escape codes.

- **Link every chart on the Today panel with a brush** — FEATURE — value 3 — effort M — risk low — category: data viz
  Why: the pane and web UI have Activity lanes, the Agents graph, History and the Today charts side by side, but they're separate views. Drag a time range on one and the others filter to it, so "what was happening at 14:10?" is one gesture.
  Done when: brushing 14:00–14:30 on the Today chart filters Activity, History and Agents to that range, and Esc clears it.

- **Render syntax-aware word diffs with moved-block detection** — FEATURE — value 3 — effort M — risk low — category: diffs
  Why: the live tree shows each call's diff compactly under the prompt. Line diffs make a renamed variable look like a rewrite, and word-level highlighting plus a "moved" tint helps the user trust a change at a glance.
  Done when: renaming one identifier across three lines highlights only that token, and a block moved within a file renders as moved rather than deleted plus added.

- **Draw charts with the terminal graphics protocol when available** — FEATURE — value 3 — effort L — risk med — category: pane charts
  Why: assumption: the Today charts are character-cell art. Kitty or iTerm2 image protocols can draw smooth anti-aliased lines, with braille or block fallback elsewhere.
  Done when: a capability probe picks the image path in a protocol-capable terminal and the braille path elsewhere, and both render the same series from one data function.

- **Add a density toggle and a one-thing zen view to the web UI** — FEATURE — value 3 — effort S — risk low — category: web UI
  Why: assumption: one density suits neither a glance across the room nor a deep audit. Compact and comfortable modes share the tokens, and zen shows only the focused task's plan, current step and what's blocking it.
  Done when: the toggle persists across reloads, and zen hides every panel except the focused task's three sections.

- **Wild: Let the palette follow the day and the repo's health** — FEATURE — value 2 — effort M — risk low — category: ambience
  Why: wild. The accent warms toward sunset hours and cools to teal when gates are fresh and green. It turns amber when proofs are stale, so repo health is felt peripherally without reading anything.
  Done when: a stored fixture with stale gates renders a measurably different accent hue than the green fixture, and contrast stays at or above 4.5:1 in both.

- **Wild: Show the queue as a factory floor in the web UI** — FEATURE — value 2 — effort L — risk med — category: playful views
  Why: wild. Tasks ride a conveyor through plan, edit, prove and close stations, so a stuck gate is a visibly jammed belt and an idle loop is an empty floor. It is a view beside the list, not instead of it.
  Done when: the view renders every open task at the station matching its state, and pausing the animation leaves a static, readable layout.

- **Wild: Mirror Foreman's state to a physical light or key** — FEATURE — value 2 — effort M — risk low — category: devices
  Why: wild. A small local hook writes the state (working, needs you, blocked, idle-green) to a Stream Deck key, USB keyboard LED or smart-bulb webhook. The needs-you beacon then works with the terminal buried. It is off by default and sends nothing off the machine unless the user sets a LAN target.
  Done when: with the integration enabled, a state change calls the configured local command exactly once with the new state name, and with it disabled nothing is invoked.

- **Copy any view as a themed, scrubbed SVG with one key** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: `demo/live.svg` shows the project already produces polished recordings. Make that a first-class `fm snap` for the pane or a web panel, with paths and tokens redacted before the file is written, so users can share a bug or a win without hand-editing.
  Done when: `fm snap` writes an SVG of the current pane, and a seeded fake secret and the home directory path are absent from the output.
