# Brainstorm — lens: bold bets

- **Make the TUI a compositor of Foreman's own scene graph** — FEATURE — value 5 — effort L — risk med — category: architecture
  Why: the list repeats widget kits, themes, shaders and extension APIs separately. Assumption: they all want one retained scene of nodes (position, style, tween, z) that every effect writes to and one diff renderer reads.
  Done when: a test builds a scene with two overlapping animated nodes, steps an injected clock, and the emitted escape stream matches a golden file.

- **Ship a "proof weather" overlay that tints chrome by held-rate** — FEATURE — value 4 — effort M — risk low — category: color
  Why: the user's complaint is "just static colors"; state-driven color is on the list only for run state. Here the accent drifts from cool to warm as the share of criteria with command-run evidence falls. Assumption: the held-rate is cheaply readable from the task file.
  Done when: with the held-rate faked at 100% and 40%, the header accent differs by a measurable hue delta in the frame dump.

- **Add a live "Foreman vs plain Claude" shadow meter** — FEATURE — value 5 — effort L — risk med — category: benchmarks
  Why: the user steered toward "better than CC and cheaper/faster", and the bench records per-task cost and time. Assumption: the bench's stored medians can serve as a baseline curve for the current task type. Draw the baseline as a ghost line against live cost and time.
  Done when: a finished run's end card states cost and time as deltas against the stored baseline, and it renders without baseline data.

- **Open the TUI on the failing test, not the dashboard** — FEATURE — value 4 — effort M — risk low — category: focus
  Why: the closing receipts and "finish names a red step" commits show the user cares most about what is red. Assumption: the red step is available in the event log. The focal element morphs to the first unproven criterion and its verify command, with output streaming in place.
  Done when: replaying a log with one red step leaves the frame's focal region showing that step's name and last command output lines.

- **Wild: Turn the guard into a visible bouncer sprite at the screen edge** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; the guard is Foreman's signature feature yet invisible. A small half-block character blocks, shrugs and waves through, with a count of refusals as a badge. Assumption: guard verdicts are in the event stream.
  Done when: a replayed refusal event plays a distinct sprite sequence, and the frames after it show the badge count increased by one.

- **Record the TUI as the demo asset generator** — FEATURE — value 4 — effort M — risk low — category: marketing
  Why: the README leads with demo/live.svg, recorded by hand. Run `fm code tui --record` against a seeded fake run to build the SVG/MP4 in CI, so the demo can't go stale. Assumption: the frame dump format feeds an SVG writer.
  Done when: CI regenerates the demo SVG from a fixture log, and a changed theme alters the file's hash.

- **Add "pace-aware" animation tied to real model latency** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: static looks come partly from motion that ignores state. Idle shimmer speed scales with seconds since the last token, and stops entirely when the stream stalls beyond a threshold, which shows a plain "silent for 40s" chip. Assumption: the stream timing is in the log.
  Done when: with a fake clock, the shimmer period differs between 1s and 20s since the last token, and it is absent at 60s.

- **Let a task's own TUI skin travel with it in the repo** — FEATURE — value 3 — effort S — risk low — category: theming
  Why: themes are discussed only as user files. A `.foreman/theme.toml` in a project makes a recording or a team's screen look the same everywhere, and a hash-gated trust prompt covers an untrusted checkout. Assumption: repos may be cloned from untrusted sources.
  Done when: opening a repo with a theme file applies it only after the trust step, and a changed file asks again.

- **Wild: Render the plan as a growing tree that sprouts a leaf per proven criterion** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; the stations track is linear, but plans have criteria and subagents. A braille-drawn tree gains a leaf when evidence lands and wilts a leaf if a later edit invalidates proof. Assumption: invalidation is detectable from the evidence timestamps.
  Done when: a log with one proof then an edit to a covered file renders one leaf, then one wilted leaf.

- **Add a pty-driven "visual diff" gate across themes in CI** — CLEAN — value 4 — effort M — risk low — category: testing
  Why: the golden-frame idea is listed, but CI has been red several times on environment differences (3.12, macOS). Sets the gate to compare cell grids after normalizing escapes, with a per-theme tolerance for color rounding. Assumption: a fixed TERM and size give stable output.
  Done when: CI fails on a one-cell change in any view, and passes on a 256-color rounding difference.

- **Wild: Make the finale a one-line shell prompt segment that outlives the TUI** — FEATURE — value 3 — effort S — risk low — category: ambient
  Why: wild; after the run ends, the result disappears with the screen. A prompt segment prints "T-1294 proved 6/6 $0.41" until the next task starts. Assumption: users can source a snippet in their shell.
  Done when: `fm code prompt` prints that segment from the last run's log and prints nothing when no run exists.

- **Auto-pick a calm layout when the docked pane is narrow** — FEATURE — value 3 — effort S — risk low — category: layout
  Why: the foreman-ui pane is docked beside Claude Code with a forced #262626 background (T-1217), so this surface is cramped and off-theme. Under 50 columns the chart views collapse to a bar plus a single status line, and the theme's background is overridden to match. Assumption: the width is detectable at start and on resize.
  Done when: frames at 40 and 120 columns use different layouts, and neither has a line wider than the terminal.

- **Wild: Let a failed run leave a "scar" in the next run's header** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; the lesson system already records failures, but the TUI never shows them. A thin crack line in the header names the last lesson relevant to this task and fades after three clean runs. Assumption: lessons are indexed by task area.
  Done when: starting a task in an area with a recent lesson shows its one-line title in the header, and a third clean run removes it.
