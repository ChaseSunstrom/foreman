# Brainstorm — lens: capability map

- **Add an attention inbox with a pinned "needs you" strip** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: the user runs unattended marathons ("keeps going through the queue until it's done or needs you"); the prior list has an alert idea but no queue of pending asks. Assumption: asks today surface only as inline text.
  Done when: a fake run that hits a blocked step and a guard refusal shows two entries in the strip, each with its task id and the exact command to resolve it, and the entries clear once resolved.

- **Show a "why" line for every guard verdict** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: recent commits keep adding guard hints (T-1288, T-1289); the TUI could surface the rule name and the way forward next to the verdict, not just flash it. Assumption: the guard returns a rule id.
  Done when: a refused command in a golden frame displays rule name plus hint text on one line, and the line is absent for allowed commands.

- **Add a TUI-side escape sanitizer with a test corpus** — SECURITY — value 4 — effort S — risk low — category: security
  Why: model and tool output is drawn raw in a custom renderer; OSC/CSI injection could rewrite the title, clipboard or the screen. Assumption: output is not already scrubbed. Distinct from the earlier "strip escapes" item by shipping a corpus of hostile samples as a ratchet.
  Done when: a test feeds 20 hostile sequences (OSC 52, cursor moves, title set) through the renderer and the emitted bytes contain none of them except Foreman's own.

- **Add `fm code tui --doctor`** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: capability detection (truecolor, mouse, graphics, tmux passthrough) is the root of "looks like crap" reports, and the repo already has `fm doctor` as a gate. Assumption: no TUI-specific diagnosis exists.
  Done when: running it prints detected color depth, unicode width, mouse and sync-output support, and a swatch row, and under `TERM=dumb` reports the fallback it will use.

- **Use synchronized-output (DEC 2026) for tear-free frames** — PERFORMANCE — value 3 — effort S — risk low — category: reliability
  Why: animated redraws over tmux/SSH flicker without it. Assumption: the renderer writes frames in multiple writes.
  Done when: each frame is wrapped in begin/end sync sequences when supported, and a byte-capture test shows one write per frame.

- **Add an in-TUI "cost of this look" meter** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: the repo obsesses over context and CPU tax (context-tax ratchet, bench_hooks); a showy TUI should prove it is free. Shows render CPU% and ms/frame in a debug overlay.
  Done when: toggling the overlay shows ms/frame and CPU%, and a bench asserts the TUI idles under a set CPU budget on CI.

- **Generate the docs gallery from golden frames** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: README leads with demo/live.svg; the TUI has no equivalent. Golden frames per theme can be rendered to SVGs automatically so docs never go stale.
  Done when: one command regenerates a docs page with an SVG per view and theme, and CI fails if the committed gallery differs from the output.

- **Add a headless "TUI as JSON" frame stream for agents** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: Foreman is checked by agents and tests; a structured frame (stations, chips, verdicts as data) lets a reviewer agent verify what the UI claimed without parsing ANSI. Assumption: view state is already a data model.
  Done when: `--frames json` emits one object per state change and a test confirms it matches the station state of a scripted run.

- **Add a tmux/Claude Code pane companion mode** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: the existing foreman-ui pane has an open T-1217 bug (background forced #262626); the code TUI could share the same renderer in a narrow docked layout with a transparent-background option.
  Done when: at 40 columns the TUI renders a compact layout with no wrapped garbage and respects the terminal's default background.

- **Wild: Let the run's failures compose the theme** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Colors drift warmer as the retry count climbs and cool back down on a proved close, so a glance across the room tells you whether the run is struggling. Assumption: retry count is available in state.
  Done when: a scripted run with 3 failures renders measurably different hue values than a clean run, and `--calm` disables it.

- **Wild: Push a phone notification with a one-image run postcard** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild. Marathon runs finish while the user is away; a rendered PNG of the final receipt card goes only to a user-configured webhook. Nothing is sent unless enabled.
  Done when: with a local test webhook configured, a closed run POSTs one image and, with no setting, makes zero network calls.

- **Wild: Add a "tail -f for humans" ticker mode** — FEATURE — value 2 — effort S — risk low — category: simplicity
  Why: wild. A single-line, scrolling status for a status bar or terminal title ("T-1294 · step 3/5 · tests green · $0.41") for people who don't want a full screen.
  Done when: `--ticker` prints one updating line to the terminal title and stdout, with no multi-line output.
