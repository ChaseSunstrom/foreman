# Brainstorm — lens: reliability

- **Make every state write atomic with a torn-write fuzz suite** — FIX — value 5 — effort M — risk low — category: state integrity
  Why: assumption: the ledger, step pointer and queue are JSON/markdown files written by many hooks and children concurrently. Pack shows lone-surrogate and broken-pipe fixes (T-0839), so write-path bugs are still surfacing one at a time.
  Done when: a test kills a writer at every write boundary (rename, fsync, partial bytes) across all state writers and `fm doctor` plus the next read recover with no data loss and no traceback.

- **Run a per-hook watchdog that fails open with a recorded reason** — FIX — value 5 — effort M — risk med — category: hooks
  Why: hooks run in every turn; a hung or crashed hook on the Stop or PreToolUse path can wedge a session. The pack has ideas on latency but none on a hard per-hook deadline with a bounded fail-open/fail-closed table (guard fails closed, recorders open).
  Done when: a test injects a sleeping hook, the session proceeds within the deadline, and the ledger holds one line naming the hook, the deadline and the decision taken.

- **Reconcile the queue against git after any crash, reset or branch switch** — FIX — value 4 — effort M — risk med — category: resume
  Why: resume exists for `/compact`, but the pack shows T-0841 resumed-session bugs and snapshot work for `git reset --hard`. Assumption: no check that "task says step 3 done" still matches the tree after the user runs git by hand.
  Done when: after a hand-run `git reset --hard HEAD~2` mid-task, the next session start prints which closed steps lost their evidence and reopens them.

- **Add a single-instance lease for every long-running verb** — FIX — value 4 — effort S — risk low — category: concurrency
  Why: T-0841 shows two sessions and a watcher conflicting; `fm bus watch`, `fm serve`, `fm night` each handle this separately (T-0834 dropped one check). Assumption: no shared lease primitive with stale-owner takeover.
  Done when: starting a second `fm serve` or `fm night` prints the owner's pid and age and exits 0; killing the owner with -9 lets a new one take over within the stale window.

- **Ship a cold-start `fm selftest` that exercises every hook with recorded payloads** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the pack's gates are `fm doctor`, roundtrip and bench, but hook payload schema drift from new Claude Code versions is a recurring theme (doctor version check, T-0788 etc.).
  Done when: `fm selftest` replays a bundled payload per hook event against the installed `claude` version and prints pass/fail per event, nonzero exit on any decode failure.

- **Make the test suite hermetic and fail on any write outside its sandbox** — CLEAN — value 4 — effort M — risk low — category: tests
  Why: 155 test files, plus a stray tracked `skill-index.json` with local paths (T-0836) shows leakage into the repo and home.
  Done when: the suite runs under a read-only HOME and a snapshot diff of the repo and HOME after the run is empty.

- **Classify every fm exit as retryable, user-fixable or bug** — FEATURE — value 3 — effort S — risk low — category: cli contract
  Why: T-0839 added exit 141 for broken pipe, so exit codes are being fixed ad hoc; hooks and children can't tell transient from permanent failures.
  Done when: every verb's failure returns one of three documented codes, and a table test asserts each verb's errors map to one.

- **Bound disk growth with a budget check in `fm doctor`** — FIX — value 3 — effort S — risk low — category: storage
  Why: compact output saves full text (capped per file, T-pack), snapshots under refs/foreman, children's private folder; total footprint has no ceiling. Assumption: no global quota.
  Done when: filling the spill store past the configured budget evicts oldest uncited files first and doctor reports the size and the eviction.

- **Wild: Run a nightly chaos drill that kills, freezes and clock-skews a throwaway session** — FEATURE — value 4 — effort L — risk med — category: chaos
  Why: wild; the pack's recovery ideas are all one-off (T-0841, wedged heartbeats), never exercised on a schedule. Assumption: `fm night` can host a drill job like the sentinel (T-round5).
  Done when: a drill SIGKILLs a scripted session mid-step, jumps the clock an hour, and the next start resumes at the exact step, with the result written to the night report.

- **Wild: Keep a last-known-good Foreman install and auto-roll back when doctor fails after self-edit** — FEATURE — value 4 — effort M — risk med — category: self-protection
  Why: wild; Foreman edits its own hooks and libs in rounds, yet one bad merge could disable the guard everywhere it's installed.
  Done when: a deliberately broken hook edit makes the next session start restore the prior commit, print one line saying so, and `fm doctor` passes.

- **Wild: Add a dead-man's file that every crash path writes with its last 20 events** — FEATURE — value 3 — effort S — risk low — category: crash recovery
  Why: wild; wedged or killed runs are detected only by stale heartbeat (T-0834 notes), with no record of what happened just before.
  Done when: killing a hook with an uncaught exception leaves a file naming hook, event and last 20 ledger lines, and `fm doctor` surfaces it once.

- **Detect duplicate or conflicting Foreman installs (marketplace plus install.sh)** — FIX — value 4 — effort S — risk low — category: wiring
  Why: round 4 shipped both marketplace install and the script; both can register the same hooks, doubling every guard and ledger write. Assumption: nothing checks for it.
  Done when: with both installed, `fm doctor` prints one line naming both paths and the fix, and hooks run once per event.

- **Pin write ownership: stamp every state write with writer and version, reject downgrades** — FIX — value 3 — effort M — risk med — category: rollback safety
  Why: assumption: an older plugin copy (marketplace cache) can open state written by a newer one and silently drop fields.
  Done when: opening a newer-schema state file with an older build refuses with a clear message instead of rewriting it, covered by a test.
