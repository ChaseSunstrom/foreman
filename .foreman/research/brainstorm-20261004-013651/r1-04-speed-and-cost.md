# Brainstorm — lens: speed and cost

- **Keep the drive alive across background waits** — FIX — value 4 — effort M — risk med — category: drive latency
  Why: friction shows 18 turn-ends only to wait on a background reviewer, each resuming later. Earlier ideas include a "background wait" drive state, but not the fix: have the drive do independent queue work (next task's plan read, gate pre-warm) while the reviewer runs, and end the turn only when nothing independent is left.
  Done when: a replayed drive with a pending reviewer and a second queued task starts the second task's plan before the reviewer reports, and `events.jsonl` shows zero wait-only turn-ends.

- **Cache gate results by input hash** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: the 704-test gate (~30 s) reruns on every `fm check`. Key each gate on hashes of the files it covers (plus the test files). Skip when unchanged and record "cached from run X" as evidence. Risk: a stale cache gives false green evidence, so the cache is invalidated by any dependency-file change and `--fresh` forces a real run.
  Done when: a second `fm check` with no file changes returns in under 1 s and labels itself cached, and touching an imported file forces a real run.

- **Select affected tests from the impact map** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: fmmap already computes impact. Run only impacted tests at step gates and the full suite at close. This cuts mid-task latency without lowering the final bar. Assumption: the test-to-module map can be built by imports.
  Done when: editing one leaf module at a step gate runs fewer tests than the full suite, and the close gate still runs all of them.

- **Make the flaky-test detector quarantine, not retry** — FIX — value 3 — effort S — risk low — category: gates
  Why: one test class failed once under machine load and passed on rerun. Rerunning blindly is slow and hides the problem. On a failure, rerun only the failed tests once, record "flaky-suspect" with the load average, and count it toward a quarantine list. A pass is evidence only when labelled as a rerun.
  Done when: a synthetic test that fails once then passes is reported as flaky-suspect (not clean green) and appears in `fm friction`.

- **Verify repo integrity in `fm doctor`** — FIX — value 4 — effort S — risk low — category: reliability
  Why: a crash left four zero-byte loose git objects that broke `git diff`, and `fm doctor` passed. Add a cheap check (find empty files in `.git/objects`, plus `git fsck --connectivity-only` when that's quick) and print the exact move-aside recovery.
  Done when: with an empty loose object planted in a fixture repo, `fm doctor` fails and names the file.

- **Stop the guard false positives with a read-only classifier** — FIX — value 4 — effort M — risk med — category: guard precision
  Why: `git stash list`, read-only python reading state files, and a heredoc that edits plugin source text are all blocked wrongly. Parse subcommands against a read-only allowlist (`stash list`, `stash show`) and treat python as read-only when the code has no write calls on Foreman paths. The guard is never weakened: each new allow is a fixture pair (allowed read and blocked write).
  Done when: all three friction commands pass, and a write variant of each is still blocked in the test suite.

- **Tier the reviewer by diff risk** — PERFORMANCE — value 4 — effort M — risk med — category: review cost
  Why: reviews find 3–7 real issues every time, so they must stay. But a reviewer reading a doc-only or test-only diff doesn't need all five lenses. Pick lenses from the touched paths (parsers → edge/adversary, exports → privacy), and run the cheap model for mechanical lenses. Quality is checked by bench replay: no lost finding on past reviews.
  Done when: a docs-only diff runs one lens, and replaying past review diffs finds the same real issues as the full pass.

- **Pre-warm the next step's context while the model works** — PERFORMANCE — value 3 — effort M — risk low — category: latency
  Why: hook p95 is 35 ms, so the hooks are not the bottleneck. Model turns are. A background `fm` job assembles recall, the impact map and the playbook excerpt for the next step into one file, so `fm next` is a single read instead of several commands.
  Done when: `fm next` after a step closes does one file read, and the file's contents match a cold build.

- **Wild: Spend leftover quota on speculative gates** — FEATURE — value 3 — effort L — risk med — category: speculation
  Why: assumption: the user's budget has idle headroom (the $15/day cap is rarely reached). While the model is thinking, speculatively run the likely next verify commands in a scratch worktree, so by the time it asks, the result is already there. Capped by `fm budget`, and the result is used only if the file hashes still match.
  Done when: a verify command speculated beforehand returns instantly in the next step with a "speculated, hashes match" label, and a mismatch discards it.

- **Wild: Add a token X-ray for each task** — FEATURE — value 3 — effort M — risk low — category: cost visibility
  Why: the user wants subagents not to "eat up a crap ton of tokens" without being restricted. `fm cost` shows totals, but a per-task flame breakdown (reads, subagents, retries, always-on rules) shows which stage is wasteful. Each line carries a "would have been saved by: <existing feature>" pointer.
  Done when: `fm cost ID --xray` prints stage-level token shares that sum to the task total within 2%.

- **Wild: Add a "fast lane" auto-detector for trivial briefs** — FEATURE — value 3 — effort S — risk med — category: ceremony cost
  Why: assumption: S-tier tasks (typo, rename) pay the same intake and plan overhead as L tasks. Learn from closed S tasks which steps produced no findings, and offer a collapsed flow (one criterion, one gate, no separate review) with a yes/no. An escalation rule promotes it to the full flow if the diff exceeds a threshold.
  Done when: a one-line doc fix completes in at most three fm commands, and a 200-line change refuses the fast lane.
