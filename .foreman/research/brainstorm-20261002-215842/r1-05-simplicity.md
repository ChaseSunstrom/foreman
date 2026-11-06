# Brainstorm — lens: simplicity

- **Skip planning ceremony for trivial tasks** — PERFORMANCE — value 5 — effort M — risk med — category: ceremony
  Why: planning is the biggest call count (task_set 1290 events); median 18 bookkeeping calls per task. Assumption: many of the 287 tasks are one-file fixes that don't need sections.
  Done when: a "tiny" captured request (≤1 file, no security/core touch) goes capture→execute→finish in ≤3 fm calls, and an audit of the 287-task history shows the rule classifies them correctly.

- **Run gates only on what changed** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: gates cost 18.8 hours; one project's `cargo test` median is 8 min, about once per task. Assumption: the gate can map changed files to test targets.
  Done when: a task touching one crate runs only that crate's tests at the gate. A full run happens only at queue end or before release, and `fm check` states which scope it ran.

- **Cache gate results by tree hash** — PERFORMANCE — value 4 — effort S — risk low — category: gates
  Why: the same `cargo test` repeats across tasks and re-verify steps; the record already keeps evidence. Assumption: a content hash of tracked files is cheap to compute.
  Done when: running a gate twice on an unchanged tree returns the stored result in under 1 s, labelled "cached @hash", and any edit invalidates it.

- **Show one "what I need from you" line, or nothing** — FEATURE — value 4 — effort S — risk low — category: output
  Why: the user asked for "clean up your output in general" and quiet output, yet the UI has many surfaces (band, pane, toasts, footer, chime). Assumption: they only act on blocks and approvals.
  Done when: with nothing blocked the footer, toasts and chimes are silent. A blocking item shows exactly one line with its key.

- **Auto-pick the cheapest model per step** — FEATURE — value 4 — effort M — risk med — category: usage
  Why: the user is usage-sensitive and wants more subagents without burning tokens; fm-scout already uses Haiku. Assumption: steps can be tagged lookup/edit/review.
  Done when: a routing table maps step types to models, and a measured run shows fewer tokens at equal audit pass rate.

- **Retire stale rules by usage evidence** — CLEAN — value 3 — effort M — risk low — category: rules
  Why: T-0085 rules diet is open; always-on cost is ~43 lines. Assumption: the ledger shows which rules ever preceded a gate hit.
  Done when: `fm rules --usage` lists each rule with a trigger count, and rules never triggered over 50 tasks are proposed for removal.

- **Detect doc drift on task close** — FEATURE — value 4 — effort M — risk low — category: freshness
  Why: the user asked that long sessions have no "out of date information, documentation". Assumption: docs mention symbols or paths that the diff touches.
  Done when: closing a task that renames or removes a documented symbol or path flags the doc line, and a test shows a flagged drift.

- **Wild: Let Foreman say "I'd skip this task"** — FEATURE — value 3 — effort M — risk med — category: judgment
  Why: wild; the inbox only grows (T-0077…T-0094 are old). Foreman could propose dropping or merging captures that are obsolete, duplicated or already fixed by later commits.
  Done when: `fm inbox prune` lists items with a one-line reason each, and nothing is removed without a yes.

- **Wild: Overnight "dry run" of the queue** — FEATURE — value 3 — effort L — risk med — category: planning
  Why: wild; hours-long tasks suggest estimating before committing. Foreman could use cheap models to pre-plan the whole queue and flag the tasks that will be slow, risky or need a user yes, so approvals are batched upfront.
  Done when: `fm queue preview` outputs an estimated time and the number of user approvals for every queued task, and approvals can be granted once.

- **Wild: Give each project a "speed budget" with a weekly report** — FEATURE — value 3 — effort S — risk low — category: metrics
  Why: wild; the measured data (42 of 125 hours in close-out, 18.8 in gates) was found by hand. A standing report would catch regressions as they happen.
  Done when: `fm report` prints median time per phase against last week, and flags any phase that grew over 25%.

- **Wild: Batch user yeses into one session-start approval** — FEATURE — value 4 — effort M — risk high — category: autonomy
  Why: wild; every protected-core edit needs a yes per task and the user wants full autonomy with no commands handed to them. Assumption: scoping a standing yes to named paths and a time window is acceptable.
  Done when: one approval covers listed paths for N hours, edits outside it still ask, and the grant shows in the band and expires visibly.
