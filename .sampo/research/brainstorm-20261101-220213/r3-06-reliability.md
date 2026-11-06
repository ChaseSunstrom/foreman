# Brainstorm — lens: reliability

- **Fail `fm task finish` on a hook that crashed silently** — FIX — value 5 — effort M — risk med — category: hooks
  Why: p95 is 278 ms over 13533 runs, but nothing in the pack says how many exited non-zero or timed out. A crashed hook means the guard is off with no signal. Assumption: friction logs only count successes.
  Done when: a test kills a hook mid-run and `fm doctor` shows "hook X crashed, guard unverified" and the next `fm task finish` refuses.

- **Run a guard liveness canary at session start** — FEATURE — value 5 — effort S — risk low — category: guard
  Why: "core:interpreter-code-driving-foreman blocked 42x" proves it fires sometimes, not that it is armed now. Plugin updates and host upgrades can unhook it silently.
  Done when: SessionStart feeds a harmless forbidden command to the guard in-process, and a deliberately disabled hook yields a visible "guard not armed" line.

- **Fail closed with a table of every hook's failure mode** — CLEAN — value 4 — effort M — risk med — category: hooks
  Why: the lean steers say hooks must stay fast, which tempts fail-open on timeout. Assumption: no single table says which hooks fail open and which closed.
  Done when: a test crashes and stalls each hook and asserts the documented outcome. The guard fails closed, the advisory hooks fail open and say so.

- **Replay the guard's block log against every rule change** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: two brief-guard false positives (a dict key and a `.join(` read as paths) show rule edits are tested by hand. Fixing them could unblock legitimate commands or open an evasion.
  Done when: `fm check` replays the logged decisions plus the false-positive corpus and fails on any flipped verdict not marked intentional.

- **Quarantine flaky tests behind the full-check refusal** — FIX — value 4 — effort M — risk low — category: tests
  Why: T-2526 makes `fm task finish` refuse on a failed full `fm check`, so one flaky test now blocks every task. T-2529 shows interpreter-specific failures already exist.
  Done when: a test failing then passing on rerun is logged to a flake ledger. It blocks finish only after N repeats, and `fm doctor` lists the ledger.

- **Make state writes crash-safe with a kill-at-every-boundary test** — FIX — value 4 — effort M — risk med — category: state
  Why: T-2334 (git timeouts leaving a task with no start point) and the baton, ledger and repo disagreement after a kill show writes that are not atomic. Assumption: some files still use plain overwrite.
  Done when: a harness kills the process at each write boundary of task start, evidence and finish, and every resulting state loads and heals.

- **Atomically swap plugin files and pin running sessions** — FIX — value 3 — effort M — risk med — category: install
  Why: T-0418 (updating the installed foreman-ui) and parallel lanes mean one session can run old hooks against new `fm`. Assumption: no version pin exists.
  Done when: a test updates the plugin mid-session and the running session still gets a consistent hook and verb version.

- **Test hook latency under parallel builder lanes** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: the 278 ms p95 likely comes from mostly single-session runs, while the pillars demand parallel lanes. Assumption: contention on shared state locks is unmeasured.
  Done when: `bench_hooks.py --lanes 6` reports p95 and fails past a budget.

- **Pre-stage a gated revert for every `fm ship`** — FEATURE — value 3 — effort M — risk low — category: ship
  Why: shipping to main is authorised, and T-2527 watches CI afterwards. A red main has no one-step reverse.
  Done when: `fm ship` writes a revert commit, ready but unpushed, and `fm ci-watch` offers it on failure.

- **Wild: Run an N-version shadow guard** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: wild. A second guard, written blind by a tool-less child from the gen-0 rules only, runs in shadow. Any disagreement with the real guard files a task and teaches which rule is underspecified.
  Done when: a week of shadow logs yields a disagreement table, and at least one disagreement is turned into a corpus case.

- **Wild: Run a CPU-starved dogfood day** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: wild. Hooks are timed on a fast dev machine. Running a session under `taskset` plus `nice` finds timeouts the user's other hardware would hit.
  Done when: a throttled run reports which hooks exceed their budget, and the budget table is updated.

- **Wild: Give each area a reliability error budget** — FEATURE — value 3 — effort M — risk low — category: gates
  Why: wild. Borrowing the SRE idea, each surface (hooks, ship, lanes, web UI) gets a monthly allowance of failures from `fm friction`. Exhausting it freezes new features in that area until a fix task closes.
  Done when: `fm doctor` prints each area's budget burn and `fm next` offers a fix before a feature when the budget is spent.

- **Detect evasion after a guard block** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard blocks 42x a week, but nothing says whether the agent then retried the same intent through another route. Assumption: blocks are logged without a follow-up check.
  Done when: a test where a blocked command is retried via `bash -c` or a script file is flagged as an evasion attempt in the log and in `fm doctor`.

Next question: Which reliability signals (crashes, timeouts, retries) does `fm friction` record today, and which failures leave no trace at all?
Next question: What happens to a headless or server run when the state directory fills or goes read-only mid-task?
