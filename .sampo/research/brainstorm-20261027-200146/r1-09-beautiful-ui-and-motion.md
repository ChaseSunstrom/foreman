# Brainstorm — lens: beautiful UI and motion

- **Make the pane's background follow the terminal theme** — FIX — value 4 — effort S — risk low — category: foreman-ui pane
  Why: T-1217 is blocked because Claude Code paints the docked pane's background #262626 (48;2;38;38;38), so the pane clashes with the surrounding UI. Assumption: the pane can read the host's palette or a light/dark flag.
  Done when: in both a light and a dark Claude Code theme, the pane's background matches the surrounding area in a screenshot taken at each setting.

- **Split register.tsx so the band and pane render from their own module** — CLEAN — value 3 — effort M — risk med — category: foreman-ui structure
  Why: T-0166 is deferred because the band and pane sit inside register.tsx with their stateful helpers. Moving them out is a prerequisite for every visual change below.
  Done when: the band and pane import from their own module, and the existing foreman-ui tests pass without changing their assertions.

- **Give every motion a reason: animate only state changes** — FEATURE — value 4 — effort M — risk low — category: motion language
  Why: the live tree and the work bar already show time bars and latest calls (demo/live.svg). Assumption: motion currently runs on timers rather than on state transitions, so it can imply activity that isn't happening.
  Done when: a run with no state change produces no animation frames, and a state change produces one transition of 200 ms or less.

- **Design empty, loading and error states for the Activity lanes and Agents graph** — FEATURE — value 4 — effort S — risk low — category: states
  Why: the Activity lanes, Agents graph and History panes all render data that can be absent (no run yet, or a stalled run). Assumption: those panes currently show a blank area in these cases.
  Done when: each pane shows a labelled empty state with its next command, and a test renders each pane with no data and checks the text.

- **Make the Foreman pane keyboard-first and screen-reader labelled** — FEATURE — value 3 — effort M — risk low — category: accessibility
  Why: the pane has a work bar, a stage rail, lanes and a graph, all of which are mouse-oriented in the demo. Assumption: no ARIA labels or focus order exist yet.
  Done when: every pane control is reachable with Tab, and an automated check finds an accessible name on each.

- **Show the stalled-run card with a live countdown and one-key actions** — FEATURE — value 4 — effort S — risk low — category: fm code TUI
  Why: the user asked for a stalled card with w (wait), k (kill) and m (switch runner) keys (T-1373). A countdown makes the stall visible without a log read.
  Done when: a stalled run shows elapsed time updating once a second, and pressing w, k or m triggers the matching action in a test.

- **Turn the zine and vase into a shareable run card** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: fm extras already renders a run as a zine and a vase (T-1556), but they are only viewable locally. Assumption: users would share a finished run if it made a clean image.
  Done when: fm extras writes a PNG of one finished run at a fixed size, and a snapshot test checks its dimensions.

- **Play a single sound-free completion pulse, not a fanfare** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: sonic recipes exist (T-1556), but the user's requests are about tokens and burn, so noise would hurt more than help. Assumption: the user runs the app while working.
  Done when: a finished task pulses the pane border once in 300 ms, with sound off by default and a test checking that the default is off.

- **Animate the site charts only once, when they scroll into view** — PERFORMANCE — value 3 — effort S — risk low — category: site motion
  Why: T-1615 already draws site charts once when seen. Extending that rule to the Today charts keeps motion from costing CPU on a page that is only read.
  Done when: scrolling a chart into view draws it once, and a second scroll does not restart it.

- **Give fm desk a stable e-paper layout that never repaints in place** — FEATURE — value 3 — effort M — risk low — category: e-paper desk
  Why: the desk card is an e-paper card and the glance is never a port (T-1615). Full repaints on e-paper are slow and flicker, so the layout needs to change only the cells that changed.
  Done when: a render with one changed field writes only that field's cells, verified by a diff test.

- **Let the user pick one design language across the web UI, desk and mod** — CLEAN — value 3 — effort M — risk med — category: design system
  Why: the web UI, the mod pane, the site and the desk card each draw their own style, and fm marks (T-1555) set icons on one grid. Assumption: the tokens already exist in one place for the icons only.
  Done when: colours, spacing and type sizes come from one token file, and a lint check fails on a hard-coded colour outside it.

- **Wild: a marquee over the terminal that reads each run as a short story** — FEATURE — value 2 — effort L — risk med — category: delight
  Why: wild. The zine and vase show a run can be drawn as an artefact, so a scrolling caption could narrate what Claude is doing in plain words, with no added model calls.
  Done when: a caption line updates from the journal in under 100 ms and makes no network or model call.

- **Wild: a pet glyph in the pane that grows with each clean gate** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Gate passes are visible state (fm check), and a small animated glyph tied to them gives the user a cheap, honest sense of progress.
  Done when: each passing gate advances the glyph one stage, and a failing gate holds its stage without resetting it.

- **Wild: a Breakout-style game in the pane that unlocks when checks run long** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Breakout already runs while checks run (T-1556), so the idea extends it: the game is a pause, not a distraction, and it stops the moment a check finishes.
  Done when: the game starts only while a check is running, and it stops within one frame of the check's exit.
