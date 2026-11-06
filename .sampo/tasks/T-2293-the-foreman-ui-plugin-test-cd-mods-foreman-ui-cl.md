---
id: T-2293
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T07:24:32Z
updated: 2026-10-31T09:13:37Z
builder_model: sonnet
base: d67b33b639eaad2f65d1b8530b02bb3c6f49f2dc
base_tree: a0fe16c85893019efa82614a8eb6599d138fc0cf
plan0_at: 2026-10-31T08:22:09Z
plan0_scope: []
verified: ok
---
# foreman-ui plugin tests: find and fix the case that fails then passes on a re-run
## Raw request
> The foreman-ui plugin test (cd mods/foreman-ui && claude plugin test .) failed 2 then passed on a re-run inside fm check --affected (T-2291's lane): find the flaky case and fix it or mark it, so a lane's affected run isn't red by chance
## Interpretation
A foreman-ui plugin test failed twice then passed on a re-run inside fm check --affected; find the nondeterministic case and fix its cause so lane runs aren't red by chance.
## Assumptions (confidence)
## Acceptance criteria
- [x] The flaky foreman-ui case is named with its cause (timing, ordering, shared state or a clock) in the task log, and fixed at that cause, not retried — verify with `cd mods/foreman-ui && claude plugin test .`
- [x] The foreman-ui suite passes five runs in a row — verify with `cd mods/foreman-ui && for i in 1 2 3 4 5; do claude plugin test . || exit 1; done`
## Non-goals
## Approach (options → choice → why)
Options: 1) loop the suite until it fails, read the failing case and fix its cause; 2) mark the case skipped as flaky; 3) add a retry around the suite in fm check. Choice 1: a skip or retry hides a real race in the pane; the loop gives the case and its cause.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Reproduce: run the suite in a loop (and with the files in another order) until a case fails; record which and why
2. [x] Fix the cause (a fixed clock, awaited render, isolated state) and prove five clean runs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `sh /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ui-par.sh` → exit 0 · (no output) (start tree + this task's tests) [ran] [tree 1bf72d30e450] (2026-10-31T08:57:07Z)
- (step 1) `sh /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ui-par.sh` → exit 0 · (no output) [ran] [tree 1bf72d30e450] (2026-10-31T08:57:07Z)
- (step 2) `cd mods/foreman-ui && for i in 1 2 3 4 5; do claude plugin test . || exit 1; done` → exit 0 · 0 fail / Ran 153 tests across 4 files. [71.77s] [ran] [tree f5da1d49c4e1] (2026-10-31T08:58:32Z)
- (step 1) `sh /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ui-par.sh` → exit 0 · (no output) (start tree + this task's tests) [ran] [tree e5f7629888ed] (2026-10-31T09:02:11Z)
- (step 1) `sh /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ui-par.sh` → exit 0 · (no output) [ran] [tree e5f7629888ed] (2026-10-31T09:02:11Z)
- (step 1) `sh /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ui-red.sh` → ✗ exit 1 · (no output) [ran] [tree 3526fb3cf041] (2026-10-31T09:05:42Z)
- (step 1) `3 parallel 'claude plugin test .' runs of the pre-fix foreman-ui tests at load 75-109 on 16 cores (the builder's lane, 2026-10-31)` → 3-5 failures per run, each 'timed out after 5000 ms' in the four named tests plus 'the file ran to its end'; not reproducible on demand here: 3 parallel runs at current load and 3 runs pinned to one core both pass on the pre-fix tests [tree 3526fb3cf041] (2026-10-31T09:06:10Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [40.40s] [ran] [tree 3526fb3cf041] (2026-10-31T09:12:47Z)
- (ac 2) `cd mods/foreman-ui && for i in 1 2 3 4 5; do claude plugin test . || exit 1; done` → exit 0 · 0 fail / Ran 153 tests across 4 files. [42.67s] [ran] [tree 3526fb3cf041] (2026-10-31T09:12:47Z)
- (step 1) `sh /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ui-red.sh` → exit 0 · Error: timed out after 5000 ms / Error: timed out after 5000 ms [ran] [tree 3526fb3cf041] (2026-10-31T09:12:47Z)
- (audit intent) `self-review of the 6-line diff: { timeoutMs: 60000 } added between name and body on the four tests measured nearest the 5 s default (T-1574, T-0909, T-1023 review age-out, T-1050 pane-sweep fit at ~4.9 s idle); the builder confirmed timeoutMs is the engine's key (timeout is silently ignored); five consecutive full suite runs pass` → a lane's affected run no longer goes red because the host is loaded, without hiding a real failure behind a retry or a skip [tree 3526fb3cf041] (2026-10-31T09:12:47Z)
- (audit edge) `self-review of the 6-line diff: { timeoutMs: 60000 } added between name and body on the four tests measured nearest the 5 s default (T-1574, T-0909, T-1023 review age-out, T-1050 pane-sweep fit at ~4.9 s idle); the builder confirmed timeoutMs is the engine's key (timeout is silently ignored); five consecutive full suite runs pass` → a real hang in those four tests now takes up to 60 s to fail instead of 5 s; other tests near 5 s could still flake (slowest seen 2-4 s) [tree 3526fb3cf041] (2026-10-31T09:12:47Z)
- (audit maintainer) `self-review of the 6-line diff: { timeoutMs: 60000 } added between name and body on the four tests measured nearest the 5 s default (T-1574, T-0909, T-1023 review age-out, T-1050 pane-sweep fit at ~4.9 s idle); the builder confirmed timeoutMs is the engine's key (timeout is silently ignored); five consecutive full suite runs pass` → the cap sits on each test, next to the code that's slow, rather than a suite-wide raise [tree 3526fb3cf041] (2026-10-31T09:12:47Z)
## Log
- 2026-10-31T07:24:32Z created
- 2026-10-31T08:21:09Z planned from capture
- 2026-10-31T08:21:31Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2293.builder.md
- 2026-10-31T08:22:06Z focused
- 2026-10-31T08:54:00Z merged worktree-agent-aee2b29f5ccd22ef2 (2 file(s))
- 2026-10-31T08:54:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aee2b29f5ccd22ef2
- 2026-10-31T08:54:01Z focused
- 2026-10-31T08:55:18Z cause: four foreman-ui tests do real CPU work near the engine's 5000 ms default per-test cap (T-1574 motion, T-0909 question, T-1023 review age-out, T-1050 pane-sweep fit at ~4.9 s idle); at load 75-109 on 16 cores they time out and their open mounts fail 'the file ran to its end'; fixed with { timeoutMs: 60000 } on those four (the engine's key; 'timeout' is ignored)
- 2026-10-31T08:56:52Z paused: focus moved to T-2299
- 2026-10-31T09:04:38Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T09:04:38Z focused
- 2026-10-31T09:04:49Z scope: mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/tests/pane-sweep.test.tsx, CHANGELOG.md
- 2026-10-31T09:13:34Z done
- 2026-10-31T09:13:37Z committed 79fefc17 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2211-review: Verdict: approve with nits (3 MEDIUM, 5 LOW); fixed or accepted with reason. Reviewer: one foreman:fm-reviewer, six lenses, read-only.
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- decision 2026-10-09: T-0476 quarantine skipped: fm check keeps treating a gate flaky 2+ times as failing
- similar finished tasks took 2–4 steps
## Regression test
none: the flake is load-dependent and won't reproduce on demand (pre-fix tests passed 3 parallel runs at current load and 3 runs pinned to one core); fm task prove can't separate before/after because the fix lives in the test files it overlays. Guarded instead by five consecutive suite runs (step 2 evidence) and the four tests' explicit timeoutMs.
## Why not caught
nothing ran the plugin suite under load: fm check --affected runs it once on whatever the host is doing, so a test at 4.9 s idle passed on quiet machines and failed only when lanes ran in parallel
## Lessons
- A UI test that does real CPU work near the runner's default cap is a timing flake waiting for load: give it an explicit timeout where it's slow, and check the runner's real option name (timeoutMs, not timeout)
## Plan gaps
- failed first: step 1 Reproduce: run the suite in a loop (and with the files in another order) until a case fails; record…
## Files touched
- mods/foreman-ui/tests/pane-sweep.test.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- .fm-scratch/batch.json
- .fm-scratch/m/tests/t.test.tsx
- CHANGELOG.md
