# Brainstorm — lens: beautiful UI and motion

- **Render every refusal as a blocker card** — FEATURE — value 5 — effort M — risk low — category: pane UX
  Why: the recent commits fix blockers one at a time (docs-impact path suggestions, `run.py` "no test matches", the core-integrity warning). The pane and web UI presumably show these as plain text. assumption: they do.
  Done when: a refused `fm task done` shows a card with the cause, the offending path and a copyable "try this" command. A snapshot test fails if any blocker is rendered without a next-step line.

- **Draw test and gate runs on a lane timeline that shows overlap** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: T-1964 and T-1984 were both "two suites at once", a bug you could only find by luck. A lane per run, with overlapping spans striped red, makes the bug visible and tells you whether the fix held.
  Done when: starting two runs on purpose shows a red-striped overlap on the web UI timeline, and a single run shows none.

- **Add a proof diff view that shows what the proving test covers** — FEATURE — value 5 — effort L — risk med — category: diff view
  Why: `fm task prove` shows the test fails without the change, but the diff doesn't show which changed lines that test touched. assumption: a coverage or trace hook is available.
  Done when: the closed-task view shows changed lines shaded by whether the proof test executed them, and a split pane shows the "fails before" and "passes after" output side by side.

- **Share one width-aware truncation helper across every surface** — CLEAN — value 3 — effort S — risk low — category: polish
  Why: T-1987 fixed a title cut mid-word at 90 characters ("…DONE-WHEN fallbac") and capitalised a command ("Fm batch"). The pane, tree, tray and web UI each truncate on their own. assumption: they do.
  Done when: one helper (word boundary, wide-character aware, keeps command case) is used by all four surfaces, and a test feeds each a CJK title and a long `fm …` title with no mid-word cut.

- **Let the pane's border breathe by state** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: motion should explain state. A slow green pulse means idle, steady amber means a gate is running, solid red means blocked, so you can read the session from across the room. assumption: the pane can recolour its border; T-1217 suggests Claude Code limits its background.
  Done when: each of the three states has a distinct border behaviour, `prefers-reduced-motion` turns the pulse into a static color, and a screenshot test covers all three.

- **Gate UI changes on screenshots in reduced-motion mode** — FEATURE — value 4 — effort M — risk med — category: visual regression
  Why: T-1217 (pane painted #262626) and the demo SVG going stale show visual drift gets caught by eye. A frozen-frame screenshot gate stops it.
  Done when: `fm check` renders the web UI and pane fixtures with animations off, diffs them against the baselines, and fails on a changed pixel region above a threshold. The failure output names the screen.

- **Turn the deferred backlog into an ageing board** — FEATURE — value 4 — effort M — risk low — category: queue view
  Why: about 30 "Later from T-07xx/T-08xx" items sit as one flat list. Cards that fade with age, group by origin task, and carry a one-key "drop with reason" action (recorded as a dropped decision) make pruning a visual habit.
  Done when: the queue view groups deferred items by origin, items older than N days render dimmer, and dropping one writes a dropped entry the brainstormers can read.

- **Add a graveyard view of dropped ideas** — FEATURE — value 3 — effort S — risk low — category: memory UI
  Why: your drops come with reasons ("conflicts with T-0401's never-idle design", "YAGNI"). A searchable list of them, shown when you review a new idea, stops repeat proposals.
  Done when: typing "idle" in the graveyard finds the T-0401 drop with its reason, and a new idea that matches a dropped one shows a warning chip with a link.

- **Wild: stamp the task closed with a "PROVEN" mark** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: a close needs a moment of finality. Wild: a short stamp animation lands on the receipt with the proof command and a short hash, then settles into a small mark that stays in the history list.
  Done when: closing a task plays the animation once (skipped under reduced motion), and the same mark with the command appears in History.

- **Wild: draw the repo as a treemap city that glows where work happens** — FEATURE — value 3 — effort L — risk med — category: repo visualisation
  Why: the map has 1877 files, with `plugin/skills` at 1248 of them. A treemap where tiles glow with recent edits and a task's scope shows as an outline lets you see blast radius, scope creep and untested areas at once.
  Done when: the web UI shows a treemap sized by lines of code, a task's scoped paths highlighted, and clicking a tile lists the tasks and tests that touch it.

- **Wild: render the queue as a subway map** — FEATURE — value 2 — effort M — risk low — category: queue view
  Why: tasks are stations along a line, gates are interchanges, and blocked work (T-0325, T-0335) sits at a closed station with the human-only reason as a sign. Dependencies and the loop's next stop are visible at a glance.
  Done when: the web UI shows the open queue as a line map where the focused task is marked "you are here", blocked tasks show their reason, and the map matches `fm` queue output.

- **Add a hook-latency sparkline to the pane and web UI** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: `bench_hooks.py` exists as a gate, but a regression only shows as a failed run. A small trend line per commit, with the budget drawn as a faint line, shows drift before it fails.
  Done when: the pane footer shows a sparkline of the last 20 bench runs with the budget line, and a regression past the budget turns it amber before the gate fails.

- **Wild: export a day as a time-lapse clip from the event log** — FEATURE — value 3 — effort L — risk med — category: shareable output
  Why: `demo/live.svg` is a hand-recorded session. The pane, tree and Activity lanes already draw from event data, so a replay renderer could produce a sped-up clip of any real day for a PR or the site. assumption: events are stored with timestamps.
  Done when: `fm` turns one day's events into an SVG or MP4 under 30 seconds, and a test renders a fixture log into identical frames twice.
