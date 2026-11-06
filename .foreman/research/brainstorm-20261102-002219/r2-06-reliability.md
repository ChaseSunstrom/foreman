# Brainstorm — lens: reliability

Questions from earlier brainstorms that reliability can answer:
- **Harness-dependent cells:** the compaction, crash and usage-limit-pause cells quietly depend on Claude Code. The other harnesses have no compaction hook or SessionStart, so a probe has to start from files alone.
- **Cells with too little history to backtest:** forced compaction, killed sessions and mid-goal upgrades are rare in the real ledger. Those probes must be planted by fault injection, not measured.

- **Key the goal by repo identity, not path** — FIX — value 4 — effort S — risk low — category: durability
  Why: assumption: goal state is filed under the project path (the state dir is `foreman-4a056f`); a moved, re-cloned or renamed checkout would orphan a multi-day goal. A "garbage-collect state for repos that moved" idea exists, but nothing re-attaches state.
  Done when: a test moves a repo with an open goal to a new path, and `fm next` still shows the goal's rows. The key is the root-commit hash plus a path alias.

- **Version the goal file and test resume across an upgrade** — FEATURE — value 4 — effort M — risk med — category: migration
  Why: the goal "carries the plan over days", and the plugin updates mid-goal (the committed fallback library shows versions coexist). Assumption: goal files carry no schema version.
  Done when: a fixture goal written by the previous release's code resumes under the current code with identical rows. A future-version file is refused with a message, never silently reinterpreted.

- **Check the next-row pick is a pure function of files** — FEATURE — value 5 — effort M — risk low — category: resume determinism
  Why: the pack lists compaction and crash survival as the core promise. Running the next-row selector with and without the transcript and requiring the same row proves resume depends on files alone. It also gives hookless harnesses a real probe.
  Done when: a drill deletes the baton and the transcript, runs the selector from repo, ledger and goal file only, and gets the same row as an uninterrupted run, across 5 fixture goals.

- **Mutate the finish oracle** — FEATURE — value 5 — effort M — risk low — category: done-detection
  Why: assumption: tests show "done" fires when it should, but not that it flips back when a finished artifact vanishes.
  Done when: in a scratch copy of a finished-goal fixture, deleting or breaking each row's witness makes the oracle say not-done and name that row. At least 90% of single-witness mutations are caught, and the rest are listed.

- **Reject a truncated decomposition** — FIX — value 4 — effort S — risk low — category: plan integrity
  Why: assumption: a decomposer child that dies, times out or hits a context limit can emit a plan that parses but is partial. That plan would later read as "complete".
  Done when: every decomposer output must end with a row-count footer that matches the rows. A test truncating output at 10 random byte offsets never files a goal, and each case reports "incomplete plan".

- **Check evidence commit reachability** — FIX — value 3 — effort S — risk low — category: ledger integrity
  Why: rebases, force-pushes and squash merges remove SHAs that closed rows cite as proof. Assumption: nothing re-checks them, so "done" would rest on a dangling reference.
  Done when: a test rewrites history under a closed row, and the goal's re-verify marks that row "evidence unreachable" and reopens it. It does not report finished.

- **Break replan thrash with a circuit breaker** — FEATURE — value 3 — effort S — risk low — category: runaway control
  Why: a goal can add rows, replan and re-decompose unattended, and nothing in the pack caps how often. Scope-growth ledgers exist as ideas, but not a hard stop on churn.
  Done when: a goal that replans more than N times in 24h with no row closing pauses, writes the reason to the final-report user-only list, and keeps other work moving. A test simulates the loop.

- **Lock goal rows against concurrent writers** — FIX — value 4 — effort M — risk med — category: concurrency
  Why: parallel builder lanes close rows while the main thread edits the plan, per the Missions 5-8 steer (S/M briefs in lanes, merged in order). Assumption: the goal file is rewritten whole.
  Done when: a test runs 8 concurrent row-closes plus 1 plan edit, 50 times, and loses no close and corrupts nothing. Writes are per-row append-only or lock-guarded.

- **Warn when goal state sits on volatile storage** — SECURITY — value 3 — effort S — risk low — category: durability
  Why: the child environment runs under `/run/user/1000`, a tmpfs. Assumption: some state or probe scratch paths could land there and vanish on reboot or eviction.
  Done when: `fm doctor` resolves the goal and ledger paths and WARNs if any is on tmpfs or an unmounted path. A test with a fake tmpfs path trips it.

- **Wild: run an amnesia day** — FEATURE — value 4 — effort M — risk med — category: drill
  Why: wild. Once a week, `fm night` snapshots a live goal, wipes session memory in a scratch copy, resumes, and scores whether it picks the same row and states the same remaining work. It is a recurring drill, not a one-off test.
  Done when: the tick writes one line "amnesia: match/mismatch, rows differing", and a planted corruption produces a mismatch.

- **Wild: fast-forward 30 days of clock** — FEATURE — value 3 — effort M — risk low — category: time
  Why: wild. A multi-day goal meets DST, timezone changes, sleep and expiring n/a rulings. Assumption: day-count and expiry logic has no tests with a faked clock.
  Done when: a faketime run of a fixture goal across DST and +30d expires the right rows, ages the right stale banners, and never reports negative durations.

- **Wild: plant a decoy open row** — FEATURE — value 3 — effort S — risk low — category: done-detection
  Why: wild. A hidden row with a non-obvious witness is added to a finished fixture, and the done verdict must catch it. A miss counts as a failed canary, and the exam can reuse it weekly.
  Done when: the canary fixture reaches "not finished, row X open" with 100% recall over 20 randomised placements.

- **Replay the journal with one record torn** — FIX — value 4 — effort S — risk low — category: crash safety
  Why: the pack's kill-at-every-boundary ideas cover the goal baton in general. This one is narrower: truncate the last journal line mid-write and require recovery to drop only that line.
  Done when: for every byte offset of the final record, replay recovers all earlier records and reports "1 torn record dropped".

Next question: Which of the 58 cells' behaviours exist only inside a live session and would fail unattended, at night or on a hookless harness?
Next question: What does the goal engine do when two goals share a row, or when a repo has a goal and the user starts a different task mid-goal?
