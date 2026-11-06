# Brainstorm — lens: reliability

- **Add a single-writer lock for the test runner** — FEATURE — value 5 — effort M — risk low — category: concurrency
  Why: the last ten commits each patched one path that could start a second suite (ambient, `fm check`, `fm ship`, mid-gate edits). Each fix is a separate guard, so the next entry point will miss it. Assumption: a lock is not already shared by all callers.
  Done when: a test starts `fm check`, ambient, and `fm ship` simultaneously and exactly one suite process runs, with the others queued or skipped and logging the holder's pid.

- **Reap stale locks and runs after a crash** — FIX — value 4 — effort S — risk low — category: recovery
  Why: the lock above and `gates_running` flags can outlive a killed process and block work forever. Assumption: these markers are files or state entries without pid-liveness checks.
  Done when: killing a gate run with SIGKILL, then running `fm check`, clears the dead marker and proceeds with a one-line notice.

- **Salvage partial output from capped `claude -p` children** — FEATURE — value 4 — effort M — risk med — category: children
  Why: T-0831 is deferred, and a capped or timed-out brainstorm child currently loses everything it produced. This lens itself runs as such a child.
  Done when: a child killed at its cap leaves its streamed text in the result and the round reports "partial, N ideas" instead of "failed".

- **Make `parse_intake` property-tested** — FIX — value 4 — effort M — risk low — category: testing
  Why: three recent fixes (T-1989 @path-only lines, mid-word title cuts, capitalized identifiers) were all intake edge cases found by use. Fuzzing would find the rest first.
  Done when: a generative test over random mixes of items, block lines, @paths, and long titles checks that no input text is lost and no title is cut mid-word; it runs in the suite.

- **Add a "suite overlap" invariant to doctor** — FEATURE — value 3 — effort S — risk low — category: diagnostics
  Why: overlap bugs were found only by dogfooding. Assumption: process listings can identify `run.py` instances.
  Done when: `fm doctor` fails if two test-runner processes are alive for one tree, and a test spawns two to prove it.

- **Replay the failing hook call from a captured trace** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: the guard hook decides on bash commands in bypass mode, and a false deny or allow is hard to reproduce. T-0798 (replay) is deferred.
  Done when: `fm replay <id>` re-runs a recorded hook input through the current guard and prints the old and new verdicts.

- **Time-box every gate and name the one that hung** — FIX — value 4 — effort S — risk low — category: timeouts
  Why: a stuck gate (the roundtrip e2e, say) blocks `fm ship` with no clue which step stalled. Assumption: per-gate timeouts are not uniform today.
  Done when: a gate that sleeps past its limit is killed and the output reads "gate 2 (roundtrip) timed out after Ns", with the task still resumable.

- **Make task close atomic and resumable** — FIX — value 4 — effort M — risk med — category: state
  Why: close involves scope check, docs-impact, `_theirs` filtering, and commit; the `_task_files` bug shows these steps disagree about state. A half-closed task is a likely failure.
  Done when: killing `fm task finish` between any two steps and rerunning completes it or reports exactly which step to redo, with no duplicate commits.

- **Chaos-test the loop with injected faults (wild)** — FEATURE — value 3 — effort L — risk low — category: chaos
  Why: forever-loop correctness (dry streaks, budget drops) is verified only by reading and real runs. Assumption: the loop can run against a fake model.
  Done when: a harness that randomly kills children, exhausts budget, and corrupts a state file ends in every run with a consistent task list and an accurate stop reason.

- **Let a second "shadow" Foreman audit the first (wild)** — FEATURE — value 3 — effort L — risk med — category: self-check
  Why: Foreman edits its own protected core, and the core-integrity warning already misfired on in-scope changes (T-1998). An independent read-only checker of invariants would catch drift the author cannot see.
  Done when: after each core-task close, a separate read-only process re-derives scope and gate results and flags any disagreement in the receipt.

- **Make a flaky-test quarantine with a rerun-for-proof rule (wild)** — FEATURE — value 3 — effort M — risk low — category: flakiness
  Why: `fm task prove` shows that a test fails without the change; flaky tests could fake that proof. Assumption: proof runs happen once.
  Done when: proof reruns the failing and passing states three times each, and a test that flips is marked flaky and refused as proof.

- **Add a black-box "last known good" rollback (wild)** — FEATURE — value 3 — effort M — risk med — category: rollback
  Why: Foreman updates its own hooks and lib; a bad core commit could break the guard that protects everything else. Assumption: no self-rollback exists.
  Done when: if `fm doctor` fails after a core change lands, `fm rollback` restores the previous passing commit of the core and the test confirms the guard hook runs again.

- **Give every "no match" error a way forward** — FIX — value 2 — effort S — risk low — category: errors
  Why: T-1995, T-1996, and the latest ask all repair messages that dead-end (docs path, `-k`, test names). A shared "did you mean" helper would stop the one-off fixes.
  Done when: docs-impact, `run.py`, and task-id lookups all use one suggester, and a test checks that each wrong name yields up to three suggestions.

- **Track hook latency regressions per commit** — PERFORMANCE — value 3 — effort S — risk low — category: perf-guard
  Why: `bench_hooks.py` is a gate already, but T-0832 shows hook cost matters in every call. Assumption: results are not stored over time.
  Done when: bench results append to a history file and `fm doctor` warns if the median rises over 25% against the last ten runs.
