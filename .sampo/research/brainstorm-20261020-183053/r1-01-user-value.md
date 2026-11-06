# Brainstorm — lens: user value

- **Animate the station track with a live pulse** — FEATURE — value 5 — effort M — risk low — category: motion
  Why: the user said the TUI "looked like crap" and then asked for "better animations... not just static colors"; the station track (plan, steps, guard, verify) is the centerpiece, and a static track can't show which station is working.
  Done when: in a recorded frame sequence the active station's glyph and color change across at least 4 frames, and a finished station stops changing.

- **Render color as truecolor gradients with 256 and 16-color fallbacks** — FEATURE — value 5 — effort M — risk low — category: look
  Why: "not just static colors". T-1217 already shows palette trouble in Claude Code's pane (#262626 background). Assumption: the TUI currently uses flat ANSI colors.
  Done when: with COLORTERM=truecolor the work bar and time Gantt emit interpolated 24-bit colors, and with TERM=xterm-256color or NO_COLOR the same frame renders without 24-bit escapes.

- **Add an eased transition between views and stations** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the earlier redesign made "views fade the screen"; extend that into one easing helper (slide, fade, count-up for tokens and cost) so all motion shares timing.
  Done when: a unit test steps the easing helper through a fixed clock and gets monotonic values from 0 to 1, and token and cost counters count up on change instead of jumping.

- **Flash guard verdicts and verify results** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: guard refusals and red steps are the moments users care about most, and `finish names a red step` shipped in 1.2.43, so the data exists. A short flash or shake on a refusal, and a settle on a pass, makes them readable at a glance.
  Done when: a refused command makes its chip flash for under 600 ms, then hold a steady red; a pass settles to green.

- **Ship a theme engine with a gallery, live preview and animated palettes** — FEATURE — value 4 — effort M — risk med — category: themes
  Why: the T-… request asked for "customizable, extendable", with themes and keybindings. A `fm code theme` command could list, preview and switch themes, with gradients, breathing accents and time-of-day variants defined in a small JSON file.
  Done when: `fm code theme set NAME` changes the next launch and a user theme file in the Foreman home dir appears in the list.

- **Honor reduced-motion, NO_COLOR and a frame budget** — FIX — value 4 — effort S — risk low — category: accessibility
  Why: CI has been red on CPU-time bounds, so animation must not burn CPU or flicker on slow SSH links. Assumption: there is no motion cap yet.
  Done when: `FM_REDUCE_MOTION=1` or a non-TTY renders static frames, and an idle TUI uses under 2% CPU in a 10 s measurement.

- **Draw sparklines and block-character charts for cost, tokens and time** — FEATURE — value 4 — effort M — risk low — category: look
  Why: the user preferred "pictures" over text, and token columns and the time Gantt already exist. Sparklines extend that to cost per turn and compaction events, which fits the long-session, cost-per-correct-session benchmark work.
  Done when: the token view shows a sparkline of the last N turns, with a mark where a compaction occurred.

- **Golden-frame snapshot tests and a recorder that exports an animated SVG** — CLEAN — value 4 — effort M — risk low — category: testing
  Why: `demo/live.svg` shows the project already publishes recordings, and animation work needs regression protection. Render deterministic frames from a fake clock and compare them, and reuse the same path for README demos.
  Done when: `python3 plugin/tests/...` fails when a frame changes, and `fm code tui --record out.svg` writes a playable animation.

- **Make ids and stations clickable and report progress to the terminal** — FEATURE — value 3 — effort M — risk low — category: interaction
  Why: T-0796 (clickable ids, progress bar, spinner, motion, palette) is deferred but matches this request. Use OSC 8 links and the OSC 9;4 progress bar for the taskbar and tab.
  Done when: a task id in the TUI is an OSC 8 link, and the terminal tab shows progress that tracks the work bar.

- **Replay a finished run as a scrubbable timeline** — wild — FEATURE — value 4 — effort L — risk med — category: replay
  Why: assumption: the run ledger records timestamps for plan, steps, guard verdicts and diffs. Play it back at 1x to 20x with the same animations, so a user can watch overnight work in two minutes.
  Done when: `fm code replay RUN` plays a finished run and the left and right arrow keys scrub it.

- **Show a completion moment with a receipt card** — wild — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user ships releases and long unattended runs; the end of one deserves a payoff. Fill the track, show a small confetti or shimmer, then a card with time, cost, checks proven and the diff size, ready for a screenshot.
  Done when: finishing a run shows the card for a set time, and `--no-fx` skips the animation but keeps the card.

- **Add an ambient "factory floor" mode** — wild — FEATURE — value 2 — effort L — risk med — category: playful
  Why: Foreman's name and its Agents graph suggest a view where workers and subagents appear as small animated figures moving along the station track, with idle ones dozing. It is for a second monitor and for demos.
  Done when: `fm code tui --view floor` shows one figure per active agent and their positions follow the real station state.

- **Pulse the whole UI from the model's rhythm** — wild — FEATURE — value 2 — effort M — risk low — category: ambient
  Why: assumption: the TUI receives streaming events. A slow breathing border while the model thinks, a faster one while it streams and a still one while it waits for the user make the state readable without text, in line with the user's dislike of text.
  Done when: border brightness follows three distinct rates for thinking, streaming and waiting, checked by a frame-sequence test.
