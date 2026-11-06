# Brainstorm — lens: unspoken needs

**Answers first (the ones my lens can).** Unattended failures that leave no trace (OS kill, logged-out auth) should surface as a missing-beat line in the next session's first output, because the user won't open the web UI. A trigger's output in the capture inbox is held by `--round-first`, so the user never sees the rule working unless a digest line names it.

- **Stop a round when novelty dries** — PERFORMANCE — value 4 — effort S — risk low — category: brainstorm
  Why: the "ideas so far" list repeats one theme many times (heartbeat, replay-before-install, one yes card, tripwire file), so each round pays to re-derive it. Assumption: a cheap token-overlap check against the seen list is good enough.
  Done when: `fm ideas` prints a new-vs-seen ratio per round and skips the next deepen pass, logging why, when it falls under a set threshold.

- **Filter gaps through the dropped ledger** — FEATURE — value 5 — effort S — risk low — category: grounding
  Why: the user's "dropped" lines (already built, by design, measured, built under another task) show the same rejection reasons repeating, and the Missions 3-4 lesson says most ideas were already built. Assumption: the dropped reasons can be matched by capability name and file path.
  Done when: a cell fill or idea that matches a dropped entry is shown with that entry's reason and is not filed as a gap, and a test covers it.

- **Shard coverage.md by capability with a write-owner lint** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the standing steer keeps Missions 5-8 in parallel `fm lane`s, all filling cells of one grid, which invites merge conflicts and cross-row phrase reuse. Assumption: coverage.md is currently one file.
  Done when: two lanes fill rows of different capabilities with no merge conflict, and a write outside the lane's own capability is refused.

- **Turn gaps into tasks by root cause, not by cell** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: the open queue already holds about 40 deferred "Later from T-07xx" bundles, and the user has never asked for more tasks. Most cells will resolve to existing features. Assumption: cells that share a missing mechanism can be detected from their cited files.
  Done when: filling 58 cells files at most one task per distinct missing mechanism, each task listing its cell ids, and the report gives the cell-to-task ratio.

- **Show a cell progress line in `fm status` and the web UI** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: the user has to ask "how many are left" through a mission this size. The pack gives only a single fixed count (58) with no progress against it. Assumption: cell states are machine-readable.
  Done when: `fm status` shows existing, new, gap, n/a and unread counts with tokens spent, and the numbers match a recount from coverage.md.

- **Pin deliberation with golden fixtures per tier** — FIX — value 4 — effort M — risk low — category: regression
  Why: gates were tuned repeatedly (T-2334, T-2341 re-scoped), and the user then found the premise wrong. Nothing in the pack pins what depth S, M and L requests receive. Assumption: the plan gate can run on canned requests without a model.
  Done when: ten canned requests per tier have stored expected depth and verdicts, and changing a gate threshold shows a diff of which fixtures moved.

- **Offer a five-cell spot check with one-word answers** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user's rules distrust Foreman's own scoring ("signals Foreman didn't author", "a templated cell isn't counted"), so they will want to verify cells without reading 58. Assumption: each cell carries a re-runnable proof command.
  Done when: `fm genesis cells --sample 5` prints random cells with their proof command output, and "redo" reopens the cell.

- **Attach the decision table to the commit as a git note** — FEATURE — value 3 — effort M — risk low — category: provenance
  Why: after a week away the user reads `git log`, not research notes. Assumption: the options table already exists as a stored artifact.
  Done when: `git log --show-notes` on a landed task shows its readings, the chosen approach, the runner-up and the falsifier.

- **Wild: Run a pre-mortem on the Mission itself** — FEATURE — value 3 — effort M — risk low — category: moonshot
  Why: wild — Missions 3-4 found most ideas already built, which a blind child could have predicted. Before filling, a tool-less child that has never seen the code guesses which cells will turn out fake, built-already or n/a.
  Done when: the guesses are stored before the fill and scored afterwards, with the hit rate in the report.

- **Wild: Write each cell as the moment the user would be annoyed without it** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: wild — it fits the rule against templated cells because every sentence is forced to be a concrete user situation, drawn from the "asked" stream. Assumption: enough real corrections exist to draw from.
  Done when: every new cell cites one real user ask or correction, and a lint rejects any that cites none.

- **Wild: Tag a cell "gold" when a past correction would have been caught by it** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: wild — it replays the user's actual corrections (the "steered" lines, such as the T-2341 re-scope) against the cell's claimed mechanism, so the grid is graded by the user's own history rather than Foreman's.
  Done when: at least 10 cells are marked gold or "would not have caught", with the correction quoted, and the not-caught ones become tasks.

- **Show an explicit "unknown" instead of an empty cell** — FIX — value 3 — effort S — risk low — category: honesty
  Why: "58 empty cells" is the only state the pack reports. A cell that is unread, probe-failing or awaiting a cold read looks the same as an untouched one, and the lean rule already prefers "pending" to a false green. Assumption: those states already exist in some form.
  Done when: the grid shows distinct counts per state, and a sweep fails if any cell is in a state the legend doesn't name.

Next question: Which of the 58 cells would the user rather see as one line in `fm doctor` than as a filled grid row, and does the cell's reader ever look at coverage.md at all?
Next question: What does Foreman do today when the plan gate is skipped entirely (hookless harness, `fm code` on a weak model), and has anyone measured how often that happens?
