# Brainstorm — lens: beautiful UI and motion

- **Zoom is the only navigation** — FEATURE — value 4 — effort L — risk med — category: navigation
  Why: the pack lists a home screen, run view, drawers, tabs, history and a breadcrumb morph as separate screens, and T-1330 adds a fleet level. Nothing ties them into one spatial model. Assumption: a single zoom axis (fleet → project → run → step → diff) with one key in and one key out is easier to learn than eight views.
  Done when: a scripted pty session goes from home to a step's diff using only `enter` and `esc`, and the frame sequence shows the camera easing between each level.

- **Let one thing move at a time** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the ideas so far add many independent animations (pulse, shimmer, flashes, breathing border, tickers). Assumption: they will compete once they run together. A motion arbiter gives each event an urgency rank, and only the top rank animates at full strength while the rest drop to static.
  Done when: a golden-frame test fires a guard refusal during a pulse and shimmer, and only the refusal animates; the others hold a still frame until it ends.

- **Show a which-key popup after a pause** — FEATURE — value 4 — effort S — risk low — category: discoverability
  Why: the keys n, h, m, d and t are already hard to remember, and T-1330 adds many more. A footer hint can't hold them all. After a prefix key and 400 ms of silence, a small panel lists the continuations with their labels.
  Done when: a pty test that presses `g` and waits shows a panel listing every `g`-prefixed binding from the registry, and the next key dismisses it.

- **Ship a TUI inspector for extension authors** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: the pack has Python extension panels and a widget firewall, but no way to see why a cell looks as it does. A key opens an overlay that shows, for the cell under focus, its owning widget, theme role, resolved colour, active motion token and last-render cost.
  Done when: `fm code tui --inspect` on a fixture run reports widget name, role and frame cost for a chosen cell, and the same data is available as JSON.

- **Show the CLI command behind every key** — FEATURE — value 4 — effort S — risk low — category: teaching
  Why: the user wants to "do anything" and also uses plain `fm`. A one-line strip shows the equivalent `fm code ...` command for the last action. Pressing `y` copies it, so the TUI teaches scripting and cannot become a dead end.
  Done when: launching a queued task from home prints `fm code --task T-xxxx --worker claude` in the strip, and running that command produces the same run.

- **Hold to confirm kill and stop** — FEATURE — value 3 — effort S — risk low — category: safety feel
  Why: T-1326 makes stop kill child CLIs, so a stray keypress now destroys a long planner run, as the nixie case shows. Holding `x` fills a ring over about 600 ms, and releasing early cancels it. Auto-repeat events stand in for key-up on terminals without the kitty protocol.
  Done when: a pty test sends repeated `x` for 700 ms and the run stops; sending `x` once leaves it running and the ring resets.

- **Draw a project heat calendar on the home screen** — FEATURE — value 3 — effort M — risk low — category: history
  Why: the weekly report and past runs exist only as text lists. A 7×N half-block grid per project shows days with proved tasks, red days and idle days, and moving along it scrubs the history list.
  Done when: a fixture with 30 days of run logs renders the calendar with correct counts per day, verified against the logs by a test, and it collapses to a one-row sparkline under 60 columns.

- **Turn type-ahead into pending tickets** — FEATURE — value 4 — effort M — risk med — category: input
  Why: the quiet planner and the user's "it just isn't doing anything" show the UI feels dead during long waits. Assumption: the user will type again while a run is busy. The input box stays live, never blocking on the harness, and anything entered becomes a queued ticket chip that is visibly waiting.
  Done when: a test types a second request while the first is in a stalled fake runner, the second appears as a queued chip within one frame, and it starts after the first closes.

- **Add a presenter mode with double-height headings** — FEATURE — value 2 — effort M — risk low — category: demo
  Why: the site and README lean on recorded demos (`--record`, animated SVG). DEC double-height and double-width lines make the focal "now" line legible across a room or in a screen share, with the laser-pointer cursor from the replay scrubber as a bonus. Assumption: most terminals support it; where they don't, it falls back to normal text.
  Done when: `--present` renders the now-line in double height on xterm and falls back cleanly on a terminal that lacks it, and golden frames cover both.

- **Pick up a ticket and reorder the queue** — FEATURE — value 3 — effort M — risk med — category: queue
  Why: "edit the queue from inside the TUI" is listed, but the motion for it is not. A row lifts (shadow row, raised colour), neighbours open a gap with a spring, and dropping it writes the new order to the task file atomically.
  Done when: a pty test moves T-B above T-A, the frames show a gap opening, and `fm task list` shows the new order.

- **Wild: Pin run requests to a ticket rail** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: assumption: the user thinks in "orders" (their repeated requests). Each request prints as a kitchen-order ticket that slides onto a rail along the top of the home screen, one per project, and is torn off with a short animation when the run closes proved. Open tickets show age with a slowly yellowing edge.
  Done when: starting three runs shows three tickets on the rail ordered by age, and a closed run's ticket leaves within 600 ms and appears in History.

- **Wild: Light the room from run state** — FEATURE — value 2 — effort M — risk low — category: ambient
  Why: the pack's bell and title cues need the terminal visible; unattended runs need a quieter signal. A local-only hook drives OpenRGB or a LAN Hue bridge (green proved, amber waiting, red refused, slow breathing while working). It is off by default and never sends anything beyond the LAN.
  Done when: with the setting on, a fake bridge records the colour sequence for a scripted run; with it off, no socket is opened (tested).

- **Wild: Cross-fade between projects as scenes with their own accent** — FEATURE — value 3 — effort M — risk low — category: multi-project
  Why: a "per-project accent from repo identity" idea exists, but not the scene change. Switching projects fades the accent and header together through an OKLCH blend, so being in the wrong project (nixie versus another) is obvious at a glance.
  Done when: switching projects produces intermediate frames whose accent steps monotonically, and a golden frame shows a different accent for each of two fixture projects.

- **Probe the render path at launch and record the result** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: assumption: some of the "just isn't doing anything" reports are really a screen that stopped painting (tmux, ssh, console). A 100 ms self-test paints a known glyph and colour and reads back with a cursor-position or colour query. On failure it drops to the plain linear view and says why in one line.
  Done when: under `TERM=dumb` and a simulated broken tty the TUI starts in linear mode with the reason shown, and under a normal pty it never shows the notice.
