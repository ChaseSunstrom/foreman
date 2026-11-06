# Brainstorm — lens: reliability

- **Journal task close as a two-phase commit with resume** — FIX — value 5 — effort M — risk med — category: state integrity
  Why: recent commits show close-time bugs (`_task_files` refusing a scoped close over another task's dirty file, docs-impact blockers, scope checks) and `fm ship` stringing several steps together; assumption: close and ship are multi-step and a crash or kill mid-way leaves a half-closed task.
  Done when: a test kills `fm task finish` after each of its steps in turn, and `fm task finish` rerun afterward completes or cleanly rolls back every time, with `fm doctor` reporting no half-closed tasks.

- **Route every test launch through one run broker with a lock** — FIX — value 5 — effort M — risk med — category: concurrency
  Why: T-1964 to T-1987 each patched one path (fm check, ambient, fm ship, mid-gate edits) to avoid two suites at once, one at a time; the same class keeps recurring. Assumption: no single owner of "a suite is running" exists yet.
  Done when: a stress test starting ambient, `fm check` and `fm ship` at the same moment shows at most one suite process alive, and a killed owner's lock is taken over within a set timeout.

- **Give every child process a deadline, a reaper and a named owner** — FIX — value 4 — effort M — risk low — category: process control
  Why: capped `claude -p` children (T-0831), gates that "hung", and the brainstorm children themselves show unbounded child work; assumption: not all spawn sites set timeouts.
  Done when: `fm doctor` lists live children with owner and age, and a test child that sleeps past its deadline is killed and reported with the owning task and gate.

- **Quarantine corrupt state files instead of crashing on them** — FIX — value 4 — effort S — risk low — category: state integrity
  Why: state is scattered across files (tasks, lessons, loop state, locks) that hooks read on every call; a hook that throws on a bad file either blocks the user or silently disables the guard. Assumption: loads are not all schema-checked.
  Done when: a test truncates each state file in turn, and the next `fm` command moves it aside with a dated name, rebuilds or defaults, and prints one line naming the file. The guard hook still denies dangerous commands throughout.

- **Prove the guard hook fails closed** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: the guard hook is the safety promise in bypass mode; assumption: a crash, timeout or import error in it currently allows the command, or the behaviour is untested.
  Done when: tests inject an exception, a timeout and a missing lib file into the hook; each yields a deny (or a visible "guard degraded" notice) for a known-dangerous command, never a silent allow.

- **Run a nightly canary on the latest Claude Code release** — FEATURE — value 4 — effort M — risk low — category: compatibility
  Why: the foreman-ui mod patches Claude Code 2.1.x (T-0418, T-1217 pane colour), so upstream releases can break it unnoticed. Assumption: no automated check of new versions exists.
  Done when: a scheduled job installs the newest Claude Code in a temp dir, runs `roundtrip.py` and the hook bench against it, and files a captured task naming the first failing step.

- **Make hook latency a gate with a p95 budget** — PERFORMANCE — value 3 — effort S — risk low — category: hook speed
  Why: `bench_hooks.py` already exists as a gate; assumption: it reports averages and doesn't fail on a tail regression.
  Done when: a commit that adds 50 ms to one hook's p95 makes `fm check` fail, naming the hook and both numbers.

- **Detect and quarantine flaky tests with rerun-for-proof** — FEATURE — value 4 — effort M — risk med — category: test trust
  Why: 385 test files plus proof-by-failing-test make flakiness corrosive: a flaky pass counts as proof, a flaky fail triggers a needless fix. Assumption: no flake tracking exists.
  Done when: `fm task prove` reruns the proving test N times and refuses a verdict that disagrees across runs. A test that flips is listed by `fm doctor` with its flip count.

- **Wild: Crash-at-every-line test for task close** — FIX — value 3 — effort L — risk low — category: chaos testing
  Why: assumption: the two-phase close above needs a way to be believed. A tracer raises at each executed line of the close path, one line per run, and checks that the invariants hold afterward (wild).
  Done when: the harness covers every line reached by the close path and all runs end in a state `fm doctor` calls clean.

- **Wild: Shadow verifier replays each closed task's proof on a clean checkout** — FEATURE — value 4 — effort L — risk med — category: proof trust
  Why: proofs are commands Claude "actually ran"; a proof that passed only because of an untracked file or leftover state is false assurance. Assumption: closes aren't re-verified from scratch (wild).
  Done when: after a ship, a background worktree at the merged commit re-runs the task's DONE-WHEN commands, and a mismatch reopens the task with the diff of outputs.

- **Wild: Fuzz the guard hook from its own deny history** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the deny log is a free corpus of dangerous commands. Mutating them (quoting, `$IFS`, base64, subshell, env prefixes) tests the guard for evasion; assumption: deny history is logged (wild).
  Done when: a fuzz run of 10,000 mutations of past denied commands reports every mutation that is still allowed, and each becomes a regression case.

- **Add a "last known good" rollback for the installed plugin** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: Foreman edits its own protected core (core-integrity warnings, T-1998), so a bad ship could break the hooks that would repair it. Assumption: no automatic rollback of the installed copy exists.
  Done when: after each green `fm doctor`, the install is snapshotted; `fm rollback` restores the newest snapshot, and a test that corrupts a hook file recovers with one command run outside the broken hooks.

- **Make state counters derived values, not stored ones** — CLEAN — value 3 — effort M — risk med — category: state integrity
  Why: the dry-streak miscount (T-1987/T-1991), the stale open-work list, and the task-file ownership gaps (T-1968) share a cause: stored counters drifting from the facts. Assumption: other counters are stored the same way.
  Done when: each counter (dry rounds, first-time-pass, gates-running) is computed from the event log, and a test that deletes the stored counters gets identical `fm status` output.

- **Add a state invariant check at every task transition** — CLEAN — value 4 — effort S — risk low — category: state integrity
  Why: one focused task, one suite at a time, and files owned by one task are rules enforced in scattered places. Assumption: no single checker asserts them.
  Done when: every transition (focus, finish, ship, defer) calls one `check_invariants()`, and a test that forces two focused tasks fails at the transition with the rule name instead of later.
