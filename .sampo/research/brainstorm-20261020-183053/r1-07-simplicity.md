# Brainstorm — lens: simplicity

- **Add one motion primitive: ease-between-states** — FEATURE — value 5 — effort M — risk low — category: motion
  Why: the request is "not just static colors". Assumption: the TUI is stdlib Python (fmcode.py) with no animation layer. One `tween(from, to, ms)` helper that every widget uses (a bar growing, a chip changing color, a station lighting up) gives motion everywhere without per-widget code.
  Done when: a unit test steps the tween with a fake clock and gets monotonic frames that land exactly on the target, and the station track, change bars and check chips all use it.

- **Animate only on state change, never idly** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: the user disliked the earlier cluttered TUI, so constant motion would repeat that mistake. Rule: a thing moves only when its state changes (plan→edit, check red→green), plus one spinner on the single active station. Everything else is still.
  Done when: a recorded idle session with no events emits zero redraws apart from the active-station spinner (counted in a test).

- **Replace fixed colors with a themed gradient ramp** — FEATURE — value 4 — effort M — risk low — category: look
  Why: "not just static colors". Define each theme as about 6 semantic tokens (ok, bad, busy, dim, accent, surface) and derive ramps from them. Bars, Gantt and token columns shade along the ramp by value, and truecolor degrades to 256 and then 16 colors.
  Done when: `fm code tui --theme X` renders the same frame in truecolor, 256 and 16 colors, with snapshot tests for each and no raw color literals outside the theme module.

- **Give the screen one focal "now" line** — FEATURE — value 5 — effort M — risk low — category: layout
  Why: the user said the TUI "looked like crap with all the text", and the fix so far was pictures. Simplicity pushes further: one large line says what the harness is doing now (e.g. "verifying step 3 · 2 of 4 checks green"), and the rest sits dimmed around it. Assumption: the current view has several equal-weight panels.
  Done when: a snapshot of a mid-run frame has exactly one full-brightness region, and the rest of the screen uses the dim token.

- **Add a `--calm` / NO_MOTION mode that is also the test mode** — FEATURE — value 3 — effort S — risk low — category: accessibility
  Why: this keeps animation honest for accessibility, SSH and CI. Honor `NO_COLOR`, `REDUCE_MOTION` and a non-TTY by drawing final states instantly. The same path gives deterministic frames for tests.
  Done when: with `NO_COLOR=1` and reduced motion set, the output has no escape-coded color and no intermediate frames, and the test suite uses this mode for its snapshots.

- **Cap the frame rate and diff-draw the screen** — PERFORMANCE — value 4 — effort M — risk med — category: rendering
  Why: richer animation risks flicker and CPU burn, and CI already trips on CPU-time bounds (T-1281 area). Render at 20 fps at most, write only changed cells, and use synchronized-output escapes where the terminal supports them.
  Done when: a 60 s animated replay uses under X% CPU (X set from the existing bench), and bytes written per second stay under a budget asserted in a test.

- **Fade views in and out instead of hard cuts** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the earlier steer already says "views fade the screen" in the redesign. Extend the same primitive to every view switch, so one transition style covers diff, plan and verify views.
  Done when: switching view emits at least 3 intermediate frames over 150 ms or less, and none with reduced motion.

- **Delete the panels nobody looks at** — CLEAN — value 3 — effort S — risk med — category: layout
  Why: assumption: the TUI shows more stations than people read. Use the session's own event log to count which views get opened, move rarely used ones behind a single key, and remove the dead ones.
  Done when: the default screen has at most 4 regions and each remaining region has a test naming the user question it answers.

- **Wild: Render the run as a living subway map** — FEATURE — value 4 — effort L — risk med — category: delight — wild
  Why: assumption: the stations are already a track. Make it a real transit line where a small train glides station to station, a failed check shows a signal turning red, and a retry loops back on a side track. A whole screen reads at a glance with no words.
  Done when: replaying a recorded run with one failed and retried step shows the train moving forward, stopping at red, looping back and then passing, verified by frame snapshots.

- **Wild: Make the terminal breathe with the model's pace** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: a single ambient pulse (border or spinner glow) whose rate follows tokens per second, slow while the model thinks and quick while it streams. It replaces the need for a stats panel to feel progress.
  Done when: the pulse period is a pure function of the token rate, tested at three rates, and it disappears in calm mode.

- **Wild: Export the run as a looping SVG postcard** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: the README already leads with `demo/live.svg`, so the project values shareable recordings. `fm code tui --postcard` would turn the animation timeline into an SMIL SVG, so the same primitive that drives the live view produces the README art.
  Done when: running the command on a recorded session writes an SVG under 200 KB that contains animation elements and renders without scripts.

- **Ship three themes only, plus a one-file override** — FEATURE — value 3 — effort S — risk low — category: customization
  Why: the user asked for a customizable and extendable TUI, and simplicity argues for a small surface. Offer dark, light and high-contrast, and let a single `~/.foreman/tui.toml` override tokens and keys, with unknown keys named in an error.
  Done when: overriding one token in the file changes the frame, and a typo in the file prints the offending key name and uses the defaults.

- **Golden-frame tests for every animation's first, middle and last frame** — CLEAN — value 4 — effort M — risk low — category: testing
  Why: the project gates on tests and CI (several red runs recently), and animation code regresses silently. Use a fake clock and snapshot three frames per tween, so any change to the look shows up as a reviewable diff.
  Done when: `python3 plugin/tests/…` fails with a printed frame diff when a tween's midpoint color changes, and passes on macOS and Linux CI.
