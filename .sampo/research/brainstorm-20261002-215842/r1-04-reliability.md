# Brainstorm — lens: reliability

- **Run gates on a content-hash cache so unchanged code never re-tests** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: gates take 18.8 of 125 hours, and one project's `cargo test` runs ~8 min about once per task. Many runs probably repeat on a tree that hasn't changed (assumption: a share of runs re-verify identical code).
  Done when: a second `fm check` on an unchanged tree (hash of tracked files plus the gate command) returns the recorded result in under 1 s and says "cached @<hash>"; any edit invalidates it.

- **Run gates in the background while the next step starts, with a fail-back** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: an 8 min blocking test run stalls the whole session; the verify step only needs the result before `done`. Assumption: later steps can start safely while the gate runs.
  Done when: `fm task done` waits on or refuses without the pending gate result, and a failing background gate raises a toast and reopens the task.

- **Select affected tests only from the task's own diff** — PERFORMANCE — value 4 — effort L — risk med — category: gates
  Why: the full suite runs once per task regardless of change size. This pairs with T-0078/T-0079 diff-scoping. Assumption: the test layout allows a path-to-test mapping, with the full suite as a periodic safety net.
  Done when: a one-file change runs a subset in under 25% of the full-suite time, and the full suite still runs at queue end.

- **Add a stuck-step detector that classifies why a task is slow** — FEATURE — value 4 — effort M — risk low — category: diagnosis
  Why: "takes hours" was reported, and the measurements give totals but not per-task causes. Assumption: the ledger has the timestamps to attribute time.
  Done when: for any task over 1 h, `fm why-slow T-xxxx` prints a breakdown (gate, review, ceremony, model thinking, waiting on user) that sums to within 5% of wall time.

- **Add a stale-fact tripwire that re-verifies recorded claims before they're reused** — FIX — value 4 — effort M — risk med — category: context freshness
  Why: the user asked for long sessions without "out of date information". Assumption: briefs and notes cite files, symbols and commands that change under them.
  Done when: a resumed task whose brief cites a path or symbol that no longer exists gets a "stale: <ref>" warning listing the refs, tested with a deleted file.

- **Add a regression-proof hook budget that fails CI when a hook gets slower** — PERFORMANCE — value 3 — effort S — risk low — category: perf guard
  Why: hooks are ~30 ms each and run on 13 events, so a slow hook multiplies. Nothing in the pack guards that.
  Done when: a test measures p95 latency per hook event and fails above a stated budget (e.g. 60 ms).

- **Add a self-healing `fm doctor --fix` for record, hooks and mod mismatches** — FEATURE — value 4 — effort M — risk med — category: self-repair
  Why: there are many moving parts (record, 13 hooks, the mod, plugin version, the 2.1.287 early-access API), and the user wants no commands handed to them. Assumption: drift is currently found only by failure.
  Done when: a corrupted stage, a missing hook entry or a mod/plugin version skew is detected and repaired in one call, each covered by a fixture test.

- **Fuzz the guard with a corpus of real commands and wrapped forms (wild)** — SECURITY — value 3 — effort M — risk low — category: guard
  Why: the guard is a regex "speed bump" over shell text. Assumption: encoded, quoted or `bash -c`-wrapped variants slip through. Replaying the user's own historical commands would also expose false positives that cost them "yes" prompts.
  Done when: a replay of the ledger's recorded commands reports false-positive and false-negative counts, and a seeded set of obfuscated dangerous forms is all caught or listed as known gaps.

- **Run a nightly chaos drill that kills the session mid-step and checks resume (wild)** — FIX — value 4 — effort M — risk low — category: resilience
  Why: drive mode already stopped early once, and resume-after-compact is a headline feature, but nothing exercises SIGKILL mid-write, a full disk or a frozen hook. Assumption: no such test exists today.
  Done when: a script kills `fm` at random points across 100 runs and the record always loads and resumes at the right step, with zero corrupt files.

- **Keep a "black box" flight recorder that makes any stall explainable after the fact (wild)** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the failure reports (drive stopped on "Next:", hours-long tasks) were reconstructed by hand. A rolling log of the last N hook decisions, gate outcomes and drive wake-ups would make each report self-diagnosing.
  Done when: after a drive stop, `fm blackbox` prints the last 50 decisions and the exact reason the loop ended.

- **Make drive mode auto-file its own bug when it detects it stopped wrongly (wild)** — FEATURE — value 3 — effort S — risk med — category: self-reporting
  Why: the "ended its turn on Next: T-0176" failure was found by the user. Assumption: the Stop hook can detect "queue non-empty but turn ended with no tool call" and capture it.
  Done when: a simulated early stop creates one deduplicated inbox item carrying the transcript tail and queue state.
