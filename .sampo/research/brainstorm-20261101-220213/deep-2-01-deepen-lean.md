# Brainstorm — lens: deepen: lean

- **Make the lean ledger one table per surface-by-stage cell** — FEATURE — value 5 — effort M — risk low — category: lean grid
  Why: the 61 empty cells in #12 are filled by templated prose today. A cell that must hold a measured number (hook p95, bytes injected, verbs touched) for its surface can't be templated, which meets the "coverage must be real" steer.
  Done when: `fm genesis sweep` fails a #12 cell that has no number and a file path, and passes all 61 with measured values.

- **Charge every new verb a deletion at `fm task finish`** — FEATURE — value 5 — effort M — risk low — category: ratchet
  Why: gen-0 §6 says subtract as you add, and the ideas list repeats "pay for every verb with a deletion". Verbs are counted already (`fm burden --by-verb`), but nothing at finish links the two.
  Done when: finishing a task that adds a verb with no retired verb, merge or slim in the same diff is refused, naming both counts.

- **Ablate injection blocks by withholding one per session** — FEATURE — value 5 — effort L — risk med — category: ablation
  Why: context averages 387k per reply and the SessionStart note is ~2k chars x 89. No measure says which block earns its bytes. Rotating a withheld block, then comparing first-time pass and cost against the baseline, gives that evidence.
  Done when: `fm lean ablate` prints each block's bytes, the pass-rate delta when it was withheld, and a keep or cut verdict, with at least 20 sessions per arm.

- **Retire stack cards by use, softly and reversibly** — CLEAN — value 4 — effort S — risk low — category: dead weight
  Why: 5 of 1219 cards are used. A cold-shelve moves unused cards to an archive that `fm lib show` still reads and restores on first request.
  Done when: the shipped plugin tree has fewer than 100 cards, and `fm lib show NAME` on a shelved card returns it and records the restore.

- **Give each surface a latency and bytes budget in doctor** — FEATURE — value 4 — effort M — risk low — category: budgets
  Why: hook p95 is 278 ms overall, but headless/server, Desktop and the web UI don't cost the same. A single number hides which surface got heavier.
  Done when: `fm doctor` prints a p95 and injected-bytes line per surface and goes red when one exceeds its budget.

- **Name the commit that made it heavier** — FEATURE — value 4 — effort M — risk low — category: attribution
  Why: the lean row only compares against the previous generation. When hook p95 or injected bytes rise, bisecting by hand is the cost. Backfilling over git history makes a regression point at a commit and its task id.
  Done when: `fm lean blame` reports, for a metric that rose, the first commit past the threshold and its T-id, tested on a planted regression in a fixture repo.

- **Ship a core install profile for headless and server use** — FEATURE — value 4 — effort M — risk med — category: profiles
  Why: the headless/server column is among the empty cells, and a server never needs the web UI, Desktop or the mod. Assumption: a no-UI profile is mostly a manifest split, not new code.
  Done when: `install.sh --profile core` installs with no UI assets, `fm doctor` passes, and the footprint is at least 40% smaller than the full install.

- **Time hooks from outside the harness in the night tick** — PERFORMANCE — value 3 — effort S — risk low — category: watchdog
  Why: the p95 figure comes from sessions that Foreman itself logs. A synthetic probe run by `fm night` uses an independent clock, as the steer prefers signals Foreman didn't author.
  Done when: the night tick appends a probe p95 per hook, and the digest names any hook whose probe p95 exceeds its logged p95 by 25% or more.

- **Show what each cold read cost against what it caught** — FEATURE — value 3 — effort S — risk low — category: tower cost
  Why: the Haiku-then-Sonnet reads run on every tower file, and the sweep itself is a cost nobody measures. Lean ought to cover the machinery that enforces lean.
  Done when: `fm lean tower` prints tokens spent, FAILs raised and FAILs upheld per read type, and flags any read that upheld none in 30 days.

- **Run the whole exam with every optional hook off (wild)** — FEATURE — value 4 — effort L — risk med — category: lean twin
  Why: wild. Hook-less runs show the part of the score that's really the hooks, and which hooks are decoration. Defer it to the final exam per the cadence steer; the zero-token arms can preview it.
  Done when: one table lists each optional hook with the exam score lost when it alone is disabled, and hooks at zero loss are queued for retirement.

- **Prove "leave no trace" with a one-file eject round trip (wild)** — FEATURE — value 3 — effort M — risk med — category: eject
  Why: wild. T-0794 queues eject and fuses. An install, a task, an eject and a diff of the tree against the pristine repo check that Foreman is as light as claimed.
  Done when: after eject, the tree and settings differ from the pre-install snapshot only by the user's own commits, tested in CI.

- **Give each capability a sunset clock at birth (wild)** — FEATURE — value 3 — effort S — risk med — category: lifecycle
  Why: wild. Every new capability would carry a measure and a date, and past the date without evidence it goes to the shelf unless someone renews it with a recorded reason. This turns T-2503's "pending" state into a time limit, so pending can't last forever.
  Done when: a capability past its date with no measurement shows as red in the sweep and files a retirement task.

- **Forecast when the lean ratchet will bite (wild)** — FEATURE — value 2 — effort S — risk low — category: forecast
  Why: wild. Fit the trend of hook p95 and injected bytes from the git-history backfill, and print the date each would cross its budget. A stated date is also a bet for the prediction book.
  Done when: `fm lean` prints a crossing date for each metric, records it as a bet, and `fm outcomes` settles it later.

- **Garbage-collect state for repos that moved or vanished** — CLEAN — value 3 — effort S — risk med — category: state
  Why: `~/.claude/foreman/state/projects/` keeps one directory per project forever. Assumption: stale ones exist on a machine with many repos. Deleting needs a look first, so archive before removal.
  Done when: `fm gc --state` lists dead project dirs with sizes, archives them on `--apply`, and restores them with one command.

Next question: Does a cut that passes the lean ratchet ever lower the first-time pass rate in the long-horizon tier, and who would see it before the final exam?
Next question: Which of the 61 cells are n/a by nature (e.g., Desktop × operate), and can that be recorded once as a rule rather than cell by cell?
