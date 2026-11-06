# Brainstorm — lens: reliability

- **Prove every hook's failure mode with a fault-injection matrix** — FEATURE — value 5 — effort M — risk low — category: hooks
  Why: hooks gate every edit, yet the pack shows no test of what happens when one crashes, hangs, or reads corrupt state (the crash left zero-byte objects and `fm doctor` still passed). Assumption: each hook currently has an implicit, unverified fail-open or fail-closed behavior.
  Done when: a test suite injects a crash, timeout, and truncated-state fault into each hook and asserts the documented outcome (block or allow) plus a logged event; a hook with no declared policy fails the suite.

- **Write state through one journaled writer** — FIX — value 5 — effort M — risk med — category: state
  Why: truncated briefs/state JSON were found only after a crash; many modules (fmcore, fmbudget, fmhooks) write state. Assumption: not all writes use temp-file plus rename plus fsync.
  Done when: a lint test fails if any module in plugin/lib writes under the state dir outside the writer, and a kill-mid-write test leaves either the old or the new file, never a partial one.

- **Make every gate verdict carry a freshness stamp** — FEATURE — value 4 — effort S — risk low — category: evidence
  Why: "nothing is done without evidence fm ran itself", but evidence can go stale when a file is edited after the run. Assumption: evidence is currently tied to the criterion, not to the tree state.
  Done when: closing a task after an edit that follows its last passing run is refused with "evidence predates edit of <path>", and a rerun clears it.

- **Detect a silent no-op verify command** — FIX — value 4 — effort S — risk low — category: gates
  Why: guard tests "passed for the wrong reason", and verify commands were corrected by hand three times (steered items). A verify that exits 0 without exercising anything is the same class. Assumption: no check today catches `pytest -k nomatch` (0 selected) or an empty grep.
  Done when: a verify that runs zero tests or matches nothing is recorded as inconclusive, not passing, using the runner's output.

- **Bound every child process with a process-group kill and an orphan sweep** — FIX — value 4 — effort M — risk med — category: processes
  Why: reviewer subagents, gates, and fm serve spawn children; the reviewer wait and the load-flaky test suggest hung or lingering work. Assumption: timeouts kill only the direct child.
  Done when: a test that spawns a grandchild and hits the timeout finds no surviving process, and session start reports any orphan left by a previous run.

- **Add a mutation check to the guard's own tests** — FEATURE — value 4 — effort M — risk low — category: tests
  Why: guard tests passed for the wrong reason, and a second adversary pass found a whole class the first missed. Mutation testing measures that directly. Assumption: no mutation tooling exists, and a stdlib AST mutator is feasible.
  Done when: `fm mutate fmguard` flips operators and branches in the parser, and each surviving mutant is listed; the suite must kill a set threshold.

- **Wild: Run a tamper-evident hash chain over the ledger** — FEATURE — value 3 — effort M — risk low — category: integrity
  Why: assumption: the ledger is plain append-only JSONL; a truncated or hand-edited line is undetectable, yet bench, budget, and lessons all trust it.
  Done when: each ledger line holds the hash of the previous one, `fm doctor` reports the first broken link, and a deleted middle line is flagged.

- **Wild: Ship a "last known good" plugin snapshot with auto-rollback** — FEATURE — value 4 — effort L — risk med — category: self-change
  Why: `fm evolve` mutates instruction files and Foreman edits its own lib, so one bad self-change could disable the hooks that would catch it. Assumption: no snapshot is taken before self-changes.
  Done when: if the canary hook run fails after a plugin edit, the previous tested snapshot is restored automatically and the event is logged.

- **Wild: Fuzz the hook payload schema against the real Claude Code versions** — SECURITY — value 3 — effort M — risk low — category: compat
  Why: Foreman parses Stop payloads and background_tasks fields owned by the harness; the user cares about compatibility, and a harness update could change them silently. Assumption: payload parsing is tolerant only by accident.
  Done when: recorded payloads from several harness versions replay through all hooks, unknown or missing fields degrade to a logged warning rather than a crash, and fm doctor lists the last version seen.

- **Bound hook and gate output so one runaway log can't blow context** — PERFORMANCE — value 3 — effort S — risk low — category: output
  Why: gate output feeds the transcript and the 6000-char rules budget shows context is tight. Assumption: gate output is not truncated before it is echoed.
  Done when: a gate emitting 5 MB returns a head-and-tail summary under a set cap, the full log is kept on disk, and the path is printed.

- **Wild: Add a deterministic "replay seed" to every flaky-class failure** — FIX — value 3 — effort M — risk low — category: flakiness
  Why: one test class failed once under load and passed on rerun, with no record of why. Assumption: tests use unseeded time or ordering.
  Done when: a failing gate prints the random seed, the load average, and a one-line command that reruns exactly that case, and the rerun reproduces the order.
