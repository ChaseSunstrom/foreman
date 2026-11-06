# Brainstorm — lens: deepen: gates

- **Build a gate DAG with a tree-hash result store** — FEATURE — value 5 — effort M — risk med — category: gates
  Why: gates cost 18.8 h, and one project's `cargo test` runs ~8 min once per task. Merges "cache by tree hash" and "content-hash cache" into one store keyed by (gate, per-input hash), with gates declared as nodes (fmt → check → unit → full) so cheap ones fail fast and unchanged nodes are never re-run.
  Done when: running `fm gate` twice on an unchanged tree makes the second run return in <1 s, with every node marked "cached @ <hash>".

- **Order gates by evidence, not by configuration** — PERFORMANCE — value 4 — effort M — risk low — category: gates
  Why: assumption: the 287 tasks' event log holds per-gate pass/fail and duration. Run the gate with the best (failure probability ÷ cost) first, so a failing task burns seconds instead of 8 minutes.
  Done when: replaying the logged history shows the median time-to-first-failure drops versus the fixed order.

- **Run the affected tests first and the full suite once at close** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: combines "affected tests only" with "full suite at close". Test selection comes from the task's own diff (as T-0078/79 want), the per-step gate runs only that subset, and the close-out gate runs everything once. Without that last backstop, selection gives false confidence.
  Done when: a mid-task gate on a one-file change runs only the mapped tests, and `fm task finish` refuses to close until a full-suite result is recorded for the final tree hash.

- **Start gates in the background and roll back on failure** — FEATURE — value 4 — effort L — risk high — category: gates
  Why: the gate runs while the next step starts. Needs a fail-back that stops the session and surfaces a toast with the failing output, and it must not let "done" be recorded before the gate verdict lands (the Stop hook already enforces evidence).
  Done when: a deliberately failing background gate interrupts the next step within one tool call, and the task can't reach closing while the gate is pending.

- **Make gate runs resumable with a per-test checkpoint** — FEATURE — value 3 — effort M — risk med — category: gates
  Why: extends "interruptible and resumable". Compaction and the 2 h drive backstop already interrupt long sessions; persisting per-test or per-shard progress lets an 8-minute suite continue where it stopped.
  Done when: killing a gate mid-run and re-running it executes only the shards that hadn't finished.

- **Quarantine flaky and slow gates with an expiry** — CLEAN — value 3 — effort S — risk med — category: gates
  Why: builds on "quarantine slow gates". A quarantined gate moves to close-out only, is shown on the gates card with its cost, and carries a re-check date so the quarantine isn't permanent. Never silently skip it.
  Done when: a gate over the threshold is demoted automatically, appears in the card as "quarantined (expires …)", and still runs at close.

- **Show a live gate card with ETA, cache hits and the next-run forecast** — FEATURE — value 3 — effort S — risk low — category: gates
  Why: the gates card already exists in foreman-ui, and the user dislikes hours-long waits with no signal. Add progress against the historical median, a "saved N min by cache" counter, and "next run would take ~X".
  Done when: the card shows the ETA and the saved-time figure during a run, driven by `fm ui --json`.

- **(wild) Prefetch gates speculatively while the plan is still being approved** — FEATURE — value 4 — effort L — risk med — category: gates
  Why: plans wait on the user's Approve, and that idle time is free. Pre-warm the build cache and the baseline test results on the untouched tree so the post-edit run is mostly deltas. assumption: a build cache exists.
  Done when: a task's first gate after approval is measurably faster than the same gate with no prefetch.

- **(wild) Replay a failed gate in a sandbox and propose a one-line fix** — FEATURE — value 3 — effort L — risk med — category: gates
  Why: a red gate currently means a long investigation. A cheap fm-scout (Haiku) pass reads the failing output and the diff and drafts a fix hypothesis, with no Opus spend until it's confirmed. That fits the usage-sensitive constraint.
  Done when: a seeded failing test produces a recorded hypothesis naming the right file within one gate cycle.

- **(wild) Share the gate cache across projects and machines** — FEATURE — value 2 — effort L — risk high — category: gates
  Why: assumption: the same dependencies and toolchains recur across the user's projects. A content-addressed store, keyed by toolchain and lockfile hash, could skip compiling and testing unchanged dependencies. It stays local-first, and entries are never trusted without a hash check.
  Done when: a second project with the same lockfile reuses cached build artifacts, and a tampered entry is rejected.
