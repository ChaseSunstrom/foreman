# Brainstorm — lens: beautiful UI and motion

- **Adopt a truecolor gradient theme engine with live interpolation** — FEATURE — value 5 — effort M — risk low — category: theme
  Why: the request says "not just static colors"; the TUI is described as stations, chips, bars. Assumption: colors are currently fixed per-role constants.
  Done when: a theme file can declare gradient stops per role, and a snapshot test renders the station track with at least 3 distinct interpolated RGB values across its width, falling back to 256/16-color when `COLORTERM` isn't truecolor.

- **Animate the station track with a flowing progress pulse** — FEATURE — value 5 — effort M — risk low — category: motion
  Why: the user's steer was "pictures" (station track, check chips, change bars). Assumption: the track is static between state changes. A traveling highlight on the active station shows the harness is alive.
  Done when: with a fake clock, two frames 100 ms apart differ in the active station's cells only, and the animation stops when the run is idle.

- **Ease state transitions between stations and chips** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the pack notes "views fade the screen be…" so fades already exist in places. Extend this to chips going pending → running → pass/fail with a color tween and a brief flash on fail.
  Done when: a chip changing state renders ≥3 intermediate frames across a configured duration, and the final frame equals the static state.

- **Add a unified frame scheduler with a reduced-motion switch** — CLEAN — value 4 — effort M — risk low — category: accessibility
  Why: several animations need one tick source, or they fight and flicker. Assumption: animation is ad hoc today. Setting `FM_REDUCE_MOTION=1` or `NO_COLOR` must disable it.
  Done when: all animations register with one scheduler capped at a set fps, and with reduced motion on the output has zero time-varying frames in a 2 s capture.

- **Show a streaming shimmer on the model's thinking line** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: the model's words are now hidden behind a view, so a thinking indicator is the only sign of progress during long turns. A shimmer sweeping the text replaces a bare spinner.
  Done when: while a turn is awaiting a reply, the status line's highlight position changes each tick and clears on the first token.

- **Draw sparkline and braille charts for tokens, cost and time** — FEATURE — value 4 — effort M — risk low — category: data viz
  Why: the TUI already has token columns and a time Gantt. Smooth braille-resolution sparklines of cost burn against the dollar cap make them live.
  Done when: a rendered cost sparkline of N samples uses braille cells at 2×4 sub-cell resolution and updates as samples arrive, verified by snapshot.

- **Render diffs with syntax-aware color and animated line reveal** — FEATURE — value 4 — effort M — risk med — category: diffs
  Why: diffs are a core station. Assumption: they use flat red/green. Token-level highlighting plus an eased reveal of the changed lines makes them readable at a glance.
  Done when: a Python diff snapshot shows at least keyword, string and comment colors distinct from add/remove backgrounds, and the reveal completes within 300 ms.

- **Design empty, loading and error states for every view** — FEATURE — value 4 — effort S — risk low — category: polish
  Why: a design-led pass needs them; assumption: only the happy path was designed. Include a skeleton shimmer for loading, and an error panel that names the cause and the next command.
  Done when: each view has a snapshot test for empty, loading and error, and no view shows a blank region in any of them.

- **Add a guard-verdict "shield" flash with a sound-free haptic cue** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: guard refusals are Foreman's signature. A brief border pulse in red on refusal, and a green settle on allow, makes them feel like events. A terminal bell is optional and off by default.
  Done when: a refusal event triggers a border color animation lasting ≤500 ms, then returns to the base color.

- **Ship hot-reloading theme files with a live preview picker** — FEATURE — value 3 — effort M — risk low — category: theme
  Why: the ask calls for a customizable, extendable UI. Editing a theme file should update the running TUI immediately, and a picker shows each theme applied to a real frame.
  Done when: modifying the active theme file changes the next rendered frame without restart, and a bad file keeps the old theme and shows an error line.

- **Wild: Render the run as a living "factory floor" scene** — FEATURE — value 3 — effort L — risk med — category: wild
  Why: wild. Work items travel as tiny glyphs along conveyor belts through plan, edit, guard and verify stations, with rejected items bouncing back at the guard. Assumption: the station model has enough state to drive it.
  Done when: a toggled "floor" view shows an item glyph moving between stations as steps advance, and a guard refusal visibly returns it.

- **Wild: Add a confetti-and-receipt finale when a task closes proved** — FEATURE — value 2 — effort S — risk low — category: wild
  Why: wild. Closing a task after `fm task prove` is the product's core moment. A short particle burst followed by a tidy receipt of what was proved makes it shareable and recordable for demos.
  Done when: a proved close plays under 1.5 s of particles ending on a static receipt, and failing or unproved closes never play it.

- **Wild: Export any session as an animated SVG replay** — FEATURE — value 4 — effort L — risk med — category: wild
  Why: wild. The README already leads with `demo/live.svg` and an MP4. Rendering the TUI's frame log to an animated SVG would let users make their own, and let the repo regenerate its demos deterministically.
  Done when: `fm code replay --svg out.svg` on a recorded run produces a file that renders animated in a browser and is byte-identical across two runs.

- **Respect terminal capabilities with an adaptive render profile** — CLEAN — value 3 — effort S — risk low — category: compatibility
  Why: the CI runs on Linux and macOS, and the tests must be deterministic. A profile detecting truecolor, unicode width and fps budget keeps looks consistent and prevents garbage on a basic TTY.
  Done when: running with `TERM=dumb` and with `COLORTERM=truecolor` both produce valid output, and the snapshot suite passes under each profile.
