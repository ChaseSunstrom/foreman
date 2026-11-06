# Brainstorm — lens: approaches

- **Add a tween-and-easing clock to the renderer** — FEATURE — value 5 — effort M — risk med — category: motion
  Why: the request is "not just static colors", and the 1.2.43 redesign has views that fade, so some transition code exists. Assumption: it is ad hoc and not shared. One `Anim(value, target, ms, ease)` primitive would drive every moving thing: chip color changes, bar growth, the station track advancing and panel slides. Everything else on this list depends on it.
  Done when: a test steps a fake clock and asserts that a bar goes from 0 to 10 cells through the intermediate values, with the easing curve visible in the per-frame widths.

- **Redraw only changed cells, at a fixed frame rate** — PERFORMANCE — value 4 — effort M — risk med — category: renderer
  Why: animation multiplies redraws, and CI has already failed on CPU-time bounds (T-1281 and the earlier CPU-time work). Assumption: the TUI repaints whole screens. Keep a previous-frame buffer, emit only the diff, and cap at about 30 fps. Stop the timer when nothing is animating, so an idle TUI costs 0% CPU.
  Done when: a bench test replays a recorded run and shows bytes written per frame down by at least 80% against full repaint, and zero redraws while idle.

- **Color the live state with time-based gradients** — FEATURE — value 5 — effort S — risk low — category: look
  Why: the user's complaint is "static colors". Make the active station's label shimmer, the progress bar run a left-to-right truecolor gradient, and the "thinking" state breathe. Colors are functions of `(cell, t)`, not constants. Replace the static fills first and leave everything else alone.
  Done when: two renders of the same state at different timestamps differ in their SGR color codes, and the same two renders under `NO_COLOR` are identical.

- **Degrade by capability, with a reduced-motion setting** — FIX — value 4 — effort S — risk low — category: accessibility
  Why: gradients that assume truecolor look broken over ssh, tmux or Claude Code's own pane (T-1217 shows pane colors already misbehaving). Detect truecolor, then 256, then 16, then `NO_COLOR`. Add a `motion = off|calm|full` theme key and honor `REDUCE_MOTION`. Assumption: this detection isn't done today.
  Done when: running with `COLORTERM` unset emits only 256-color codes, and `motion=off` produces a static frame with no timer.

- **Make animated palettes part of the theme file format** — FEATURE — value 4 — effort M — risk low — category: customization
  Why: the 1.2.43 request asked for a "customizable, extendable" TUI with themes and keybindings. Let themes declare `gradient: [#..,#..]`, `pulse: 1.2s` and `flash: guard-deny` as data, so users restyle motion without touching code.
  Done when: a theme file with a gradient and a pulse renders animated, and a malformed entry falls back to the default theme with a one-line warning.

- **Draw charts in braille and block glyphs** — FEATURE — value 4 — effort M — risk low — category: visuals
  Why: the user said the old TUI "looked like crap with all the text", and the redesign moved to pictures (Gantt, token columns). Braille sparklines for the token rate, a sub-cell-resolution Gantt and eighth-block bars make those pictures sharper without new dependencies.
  Done when: a snapshot test shows a token series rendered as an 8-row braille sparkline, with exact glyphs for a fixed input.

- **Flash on events instead of animating idle** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: this is the "do less" route. Skip ambient animation and animate only on harness events: a guard deny flashes red and fades, a proved step wipes green, a diff change pops its bar. It is cheap, easy to test and distracting only when something matters. It is the fallback if the full clock slips.
  Done when: feeding a guard-deny event triggers a flash that decays to the base color within 400 ms of fake clock time.

- **Snapshot-test frames and export a run as an animated SVG** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: the README leads with `demo/live.svg`, so recordings matter to the project. Golden frames at fixed timestamps stop animation work from regressing silently, and the same frame stream can write an SVG or MP4 for the site.
  Done when: `fm code tui --replay run.jsonl --svg out.svg` produces an SVG whose frame count matches the replay, and a golden-frame test fails on a one-cell change.

- **Reuse Textual or Rich as an optional renderer** — FEATURE — value 2 — effort L — risk high — category: reuse
  Why: they give animation, layout and mouse support for free. The cost is a dependency in a stdlib-only codebase, and a second renderer to keep matching the first. Assumption: the project is stdlib-only, since the model client is described as "stdlib". Not recommended over the in-house path.
  Done when: `fm code tui --renderer textual` shows the same stations as the default renderer, and the default path still imports nothing outside the stdlib.

- **Mirror the TUI frames to the web UI** — FEATURE — value 3 — effort L — risk med — category: web
  Why: the pack lists the web UI as the only surface. Serve the same cell grid over a websocket to xterm.js, or as CSS-animated HTML, so one animation model drives both and a long unattended run can be watched from a browser.
  Done when: opening the local URL during `fm code` shows the live station track, and the DOM matches the terminal frame cell for cell in a test.

- **Let the border breathe with token rate** *(wild)* — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: nobody asked, but ambient state is a good fit for "not static colors". The frame edge pulses faster as tokens stream and slows to a dim glow when the harness waits on a verify run. You can tell at a glance whether the run is alive.
  Done when: the border pulse period in a test is shorter at 200 tok/s than at 5 tok/s.

- **Burst particles when a task closes green** *(wild)* — FEATURE — value 2 — effort M — risk low — category: delight
  Why: assumption: a small celebration on a proved close gives the end of a 2-minute unattended run some payoff. A few glyphs fly out from the check chip and fade over about 600 ms. It is off under `motion=calm`.
  Done when: closing a task spawns particles that all disappear by 700 ms, and none spawn when `motion=off`.

- **Draw the Gantt with kitty or sixel graphics** *(wild)* — FEATURE — value 2 — effort L — risk high — category: graphics
  Why: assumption: terminals with the kitty or sixel protocol can show a real antialiased time Gantt and token plot, with the glyph version as fallback. It is the highest-fidelity picture of the work, but support is patchy, and Claude Code's docked pane likely won't pass it through.
  Done when: on a kitty-protocol terminal the Gantt appears as an image, and elsewhere the braille version appears with no escape-code garbage.

- **Run a plasma screensaver while a long job waits** *(wild)* — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: for long unattended runs (the marathon showcase, T-1240) the screen is idle for minutes. After 30 seconds of no events, a slow per-cell color field dims the transcript, and any event or keypress brings the real view back.
  Done when: 30 seconds of fake idle time switches to the field, and the next event restores the previous frame exactly.
