# Brainstorm — lens: bold bets

- **Seal holdout tests before the fix is written** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: the same agent writes both the proof test and the fix. Recent history shows a proof that silently proved nothing (T-1994: `-k core_integrity` matched no test, and the run passed anyway).
  Done when: a child that never sees the implementation writes acceptance tests from the DONE-WHEN alone. `fm task done` runs them, and a fix that special-cases the visible test fails the sealed one.

- **Parse guard commands with a real shell AST** — SECURITY — value 5 — effort L — risk med — category: guard
  Why: the guard tracks `_DCWD["seen"]` pairs, nested reads and script reads by hand. That points to a heuristic parser, which is where bypasses live.
  Done when: a corpus of 200 obfuscated destructive commands (quoting, `$()`, `eval`, heredocs, `bash -c`) is all blocked and 500 benign ones all pass. Every existing guard test still passes.

- **Compile the hot hook path to a native binary** — PERFORMANCE — value 4 — effort M — risk med — category: latency
  Why: `bench_hooks.py` is a gate and T-0832 (shell prefilter) is deferred. Interpreter start-up is the floor for every tool call.
  Done when: `bench_hooks.py --runs 20` shows a p95 under 10 ms for the guard path. The Python path takes over when the binary is missing, with identical verdicts on the guard test corpus.

- **Escalate through model tiers on gate failure** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: T-1231 (beat Claude Code on cost) and T-1266 (ceremony profile per kind and model) are both deferred for lack of a mechanism. A cheap-first ladder gives one.
  Done when: a duel run shows lower cost at an equal pass rate. Each task record lists the tier of every attempt and why it escalated.

- **Race two approaches in worktrees and keep the better pass** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: assumption: many open FIX tasks have more than one plausible fix. The smallest diff with a discriminating proof is a measurable winner.
  Done when: `fm task race T-n` runs two lanes in separate worktrees, merges the one that passes with the smaller diff, and records why the other lost.

- **Audit any PR with a Foreman GitHub Action** — FEATURE — value 4 — effort M — risk low — category: CI
  Why: the tests badge and T-0352 (publish) show CI is already in play. Foreman's discipline currently only applies to sessions it runs.
  Done when: on a sample PR the action comments with the changed files that have no proof, the missing DONE-WHENs and the gate results. It exits non-zero when configured strict.

- **Run gates in a hermetic container** — FEATURE — value 3 — effort M — risk med — category: reproducibility
  Why: overlapping suites and host-dependent failures keep producing fixes (T-1967, T-1974). A no-network rootless run separates "red because of the change" from "red because of the host".
  Done when: `fm check --hermetic` runs the gates with no network in a rootless container. Its pass/fail verdict matches the host run on the current suite.

- **Mine runtime invariants from test runs** — FEATURE — value 3 — effort L — risk med — category: verification
  Why: assumption: Foreman's state files (task ledger, locks, loop state) have implicit invariants that only break at close or crash.
  Done when: a Daikon-style tracer proposes at least five invariants over the task state. Each is accepted as an assertion or rejected with a reason. One seeded violation is caught.

- **Route specialist sub-agents by trailing held-rate** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: T-0829 (lens scaling from `lens_rates`) shows per-agent yield is already recorded but unused.
  Done when: `fm status` shows each specialist's last-20 held rate. Dispatch picks the highest-rate one for a task kind, and a test shows a failing specialist is demoted.

- **Ingest runtime errors as repro-first tasks** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: assumption: intake takes only pasted text and typed asks, and a log tail or Sentry-style export is the next source.
  Done when: `fm intake --from-log app.log` creates one FIX task per distinct stack trace, with a reproduction command as its DONE-WHEN.

- **Wild: Stake budget on first-time passes** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. Each agent stakes a slice of usage on "this task passes first time", and the close shows odds against outcome. Wrong confidence then costs something real, unlike a score that gets ignored.
  Done when: closing a task prints the stated odds and the outcome, and the calibration curve over the last 50 tasks is viewable.

- **Wild: Draft the upstream issue when the bug is in a dependency** — FEATURE — value 3 — effort M — risk med — category: ecosystem
  Why: wild. Blocked items like T-0418 (installed foreman-ui) and T-1217 (Claude Code paints the pane background) are really upstream defects. A minimal repro and a drafted issue would turn a dead end into a move.
  Done when: a blocked task labelled upstream gets a stand-alone repro script and an issue draft file. Nothing is sent without an explicit command.

- **Wild: Rebuild a command clean-room from its docs and diff** — FIX — value 3 — effort L — risk low — category: docs
  Why: wild. A child that sees only the README and `--help` reimplements a small command. Where its behavior differs from the real one, the docs are ambiguous or the behavior is undocumented, which is the sibling-gap class this stream keeps fixing by hand.
  Done when: for three commands, a diff report lists each behavioral divergence as a doc fix or a bug task.

- **Wild: Quiz the guard with a bounty corpus** — SECURITY — value 3 — effort M — risk low — category: guard
  Why: wild. An attacker child gets a fixed budget to find a command the guard allows but shouldn't. Every success becomes a permanent test, and the budget is the score.
  Done when: a nightly run records bypasses found per dollar spent. Each bypass becomes a guard test within the same run.
