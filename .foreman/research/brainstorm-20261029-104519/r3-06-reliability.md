# Brainstorm — lens: reliability

- **Make task close transactional with a journal and resume** — FIX — value 5 — effort M — risk med — category: state integrity
  Why: recent commits show close-time bugs (`_task_files` refused a scoped close over another task's dirty file; core-integrity warned mid-task). Close is a multi-step sequence (gates, scope check, docs-impact, commit, status write); a crash or kill mid-way leaves a half-closed task. Assumption: no write-ahead record exists today.
  Done when: killing `fm task finish` at each step boundary (injected fault test) and rerunning it either completes or cleanly reports "resumed from step N", leaving task and git state consistent.

- **Give every child process a deadline, a reaper and a named owner** — FIX — value 5 — effort M — risk low — category: process control
  Why: the backlog carries "Salvage partial results from capped `claude -p` children" (T-0831) and the repo has ambient runs, ship runs and fm check all launching suites. A hung child blocks gates silently. Assumption: timeouts are not uniform today.
  Done when: a test child that sleeps forever is killed at its deadline and the gate failure names the child, its owner task and the timeout, and no orphan remains in `ps`.

- **Add a single test-run broker with a lock file and stale-owner takeover** — FIX — value 5 — effort M — risk med — category: concurrency
  Why: T-1964, T-1984 and T-1974 each patched a different path (ambient, ship, check) to avoid two suites at once; three point fixes show the invariant is not enforced in one place. Assumption: launch sites still call subprocess separately.
  Done when: a stress test launching ambient, `fm check` and `fm ship` concurrently shows at most one suite process alive at any instant, and a lock whose pid is dead is taken over within 5 seconds.

- **Make hook failures fail-safe and visible with a circuit breaker** — SECURITY — value 5 — effort M — risk med — category: guard hook
  Why: the guard hook is the only protection in bypass mode, and the bench for hook latency exists (`bench_hooks.py`). If the hook crashes or times out, behaviour is undefined from the pack. Assumption: a crash currently allows the command.
  Done when: forcing the hook to raise on a destructive command results in a deny with the message "guard unavailable", and three consecutive crashes surface in `fm doctor` with the traceback.

- **Fuzz `parse_intake` with round-trip and no-loss properties** — FIX — value 4 — effort S — risk low — category: parsing
  Why: three of the last asks were intake parsing bugs (bare `@path` lines dropped, titles cut mid-word, capitalization). Lossy parsing silently discards user words. Assumption: no property tests exist.
  Done when: a property test over generated intake text asserts every non-blank input line appears in some item's title, block or scope, and it runs in the suite.

- **Validate the state files with a schema check on every load and a quarantine on corruption** — FIX — value 4 — effort M — risk low — category: state integrity
  Why: Foreman keeps tasks, lessons and loop state on disk and parallel lanes write them; "Persist loop state in a crash-safe journal" is already a listed idea but nothing covers a partly written file today. Assumption: writes are not all atomic rename.
  Done when: truncating a state file mid-JSON makes the next `fm` command move it to `quarantine/`, restore the last good copy and print one line saying so, instead of a traceback.

- **Make every gate idempotent and prove it by running twice** — CLEAN — value 4 — effort M — risk low — category: gates
  Why: T-1974 "one full fm check per tree" and the writing-gate test (gate 1 reruns when another gate writes under its paths) show gates interacting through the filesystem. Assumption: no check that a second run gives the same verdict.
  Done when: a doctor self-test runs each gate twice on a clean tree and fails if verdicts or the tree diff differ.

- **Detect and quarantine flaky tests with rerun-for-proof** — FEATURE — value 4 — effort M — risk med — category: test trust
  Why: `fm task prove` shows a test fails without the change; a flaky test could pass that for the wrong reason. Assumption: proof runs once each way.
  Done when: prove runs the failing side three times and refuses a proof whose failures are not consistent, naming the unstable test.

- **Wild: Crash at every line of task close** — FIX — value 4 — effort L — risk low — category: fault injection — wild
  Why: assumption: close is the highest-value state transition. A tracer-driven harness raises at each executed line in turn, then asserts the invariants hold after a resume.
  Done when: the harness sweeps all lines of the close path with zero invariant violations and runs in CI nightly.

- **Wild: Keep a nightly canary project Foreman works on** — FEATURE — value 4 — effort L — risk low — category: canary — wild
  Why: assumption: regressions in hooks surface only through the user's real work; a small fixture repo with scripted asks run against the newest Claude Code release catches them first (the repo already has `plugin/tests/e2e/roundtrip.py`).
  Done when: a scheduled job runs a scripted five-task session and posts pass or fail with the diff against last night's transcript shape.

- **Wild: A shadow verifier that replays each closed task's proof on a clean checkout** — SECURITY — value 4 — effort M — risk low — category: proof integrity — wild
  Why: assumption: proofs are recorded with commands "it actually ran" but stale environment or dirty files could make them pass only locally.
  Done when: closing a task triggers a clean `git worktree` checkout of the commit, the recorded proof command is rerun there, and a mismatch reopens the task with the diff.

- **Self-heal `fm doctor --fix` for stale locks, runs and half-closed tasks, with a dry run** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: after crashes the user has no single command to clear stale locks, orphan runs or inconsistent task states; core-integrity warnings already mislead about what to do. Assumption: manual cleanup today.
  Done when: seeding stale lock, dead run record and a half-closed task, `fm doctor --fix --dry-run` lists three repairs without changing anything, and `--fix` makes the next `fm doctor` fully green.
