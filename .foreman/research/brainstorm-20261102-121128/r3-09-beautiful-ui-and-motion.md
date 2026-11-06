# Brainstorm — lens: beautiful UI and motion

- **Build a UI gallery with golden screenshots** — FEATURE — value 5 — effort M — risk low — category: UI testing
  Why: assumption: the web UI and foreman-ui have no pixel-level check. T-1217 (pane painted #262626) shows a visual bug that only a person noticed.
  Done when: `fm ui gallery` renders every component and screen in empty, loading, error, long-id and unproven states from fixtures, and `fm doctor` fails on an unapproved pixel diff.

- **Fade values as they go stale** — FEATURE — value 4 — effort S — risk low — category: trust cues
  Why: the earlier questions ask which gauges Foreman trusts only because it wrote them, and a dead timer still reads as a confident number. Opacity tied to age makes a stale value look stale.
  Done when: a value older than 2× its refresh interval renders at reduced opacity with an "as of 14h ago" label, and a test with a frozen clock asserts the style change.

- **Open a number's provenance on click** — FEATURE — value 4 — effort M — risk low — category: trust cues
  Why: assumption: the Today charts and held-rate show numbers with no path back to their source. A popover turns "trust me" into "here's the command".
  Done when: clicking any figure in the web UI shows the command or ledger query that produced it, its sample size and its age, and a test fails if a figure has no provenance record.

- **Make every motion map to a state-machine edge** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: assumption: the stage rail animation idea lacks a rule for what may move. One named transition per task-state edge (queued→active→proving→closed, plus blocked and unproven) means motion only ever explains a change.
  Done when: a test enumerates the task state machine's edges and fails if one has no transition, or if any animation runs with no state change behind it.

- **Allow one pulsing element per screen** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: assumption: the pane, bands and lanes can all animate at once. A single attention slot goes to the item that needs the user (an `fm ask` grant or a blocked task), and everything else stays calm.
  Done when: a render test with five simultaneous alerts shows exactly one animated element, chosen by a stated priority order.

- **Degrade colour for NO_COLOR, 16-colour and non-truecolor terminals** — FIX — value 4 — effort M — risk low — category: terminal
  Why: T-1217 comes from hard-coded 48;2 truecolor backgrounds clashing with the host. Anyone over ssh or in a plain TTY gets wrong colours or none.
  Done when: `NO_COLOR=1` and `TERM=xterm` runs of `fm status` and the pane keep every verdict readable via glyphs and weight, with snapshot tests for each tier.

- **Encode verdicts with shape, not colour alone, and respect reduced motion** — FEATURE — value 4 — effort M — risk low — category: accessibility
  Why: assumption: proven, unproven and overridden are distinguished mainly by colour, and the ideas so far add a hatched unproven state without an accessibility contract.
  Done when: an automated check simulates deuteranopia and `prefers-reduced-motion`, confirms the three receipt states stay distinguishable, and confirms motion becomes instant fades.

- **Show which diff hunks the proof command exercised** — FEATURE — value 5 — effort L — risk med — category: diff view
  Why: the proof kinds already include a "test fails without the change" check, but the reader can't see what it covered. A gutter mark on each hunk turns the receipt into something checked at a glance.
  Done when: the diff view in the web UI marks each hunk as exercised, unexercised or unknown from coverage of the proof run, and a fixture task with one untouched hunk shows it as unexercised.

- **Reflow the pane across narrow, medium and wide terminals** — FEATURE — value 3 — effort M — risk low — category: responsive
  Why: assumption: foreman-ui's pane and live tree are laid out for a wide terminal, and `register.tsx` is already overloaded (T-0166).
  Done when: the pane renders at 60, 100 and 160 columns with a documented drop order (graph first, work bar last), tested at each width.

- **Put inline sparklines in CLI status lines** — FEATURE — value 3 — effort S — risk low — category: terminal
  Why: the Today charts live only in the pane and web UI. Hook p95, cost per task and held-rate as one-line Unicode sparklines would put the trend into `fm doctor` and `fm status`.
  Done when: `fm doctor` prints a sparkline for hook p95 over the last 14 days, falling back to a number alone with no Unicode.

- **Draw the forecast as a range on the work bar** — FEATURE — value 3 — effort M — risk low — category: progress
  Why: the forecast-then-score idea exists but not how to display it. A ghost band for the likely finish range shows uncertainty, and a miss is visible when the bar leaves the band.
  Done when: the work bar shows a p25–p75 band from past tasks of the same kind and logs an "outside band" mark when a task finishes beyond it.

- **Render proof coverage as a repo treemap** — FEATURE — value 3 — effort L — risk med — category: visualization — wild
  Why: assumption: the map knows 2117 files and the proof records know which were touched and verified. A treemap sized by lines, coloured by proven, unproven or never-touched, would be a new picture of the repo, and a day's work would visibly fill it in.
  Done when: a web UI page renders the treemap from `fm map` and the proof ledger, and a fixture repo with one unproven file shows it hatched.

- **Show the night's work as a sunrise strip** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: `fm night` ticks run unattended and the morning brief is text. A dark-to-dawn timeline, with each tick a dot and failed or unwatched ticks hollow (T-2607), makes the night's coverage legible and pleasant.
  Done when: the first session of the day shows the strip, and a night with a missed tick renders a visible gap with the reason.

- **Print the daily report on a thermal-receipt stylesheet** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: assumption: the "receipt" metaphor is already core to Foreman. A narrow monospace print layout (58mm, tear-off line, total minutes and cost) could go to a real receipt printer or a PDF, and people would show it off.
  Done when: `fm report --print` produces a 58mm-wide page that fits one sheet for a typical day and includes each task's proven, unproven or overridden state.

Next question: which screens or panes does the user actually open each week, and which of the UI's features have they never scrolled to?
Next question: when the UI shows a verdict, how long does a reader take to tell proven from unproven in a screenshot, and could a cold reviewer without the legend get it right?
