---
id: T-1906
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py, plugin/tests/test_task_ergonomics.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T03:36:15Z
updated: 2026-10-29T03:51:04Z
base: 8b4aeed457094060f6f4a76e03595b966fd6f793
base_tree: 80de8a99fed5e661d4d0fcadd96ee21a8e364a81
plan0_at: 2026-10-29T03:38:08Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py, CHANGELOG.md]
verified: strong
---
# Fm task finish checks a FIX's red-to-green proof before running its checks
## Raw request
> fm task finish runs the criterion checks (2+ min) before refusing for a missing red-to-green proof; check the proof with the other cheap preconditions first, so a refusal costs nothing (T-1902 close)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a FIX close with no red run is refused before any check runs; a red run of a command the close will run still counts — verify with `python3 plugin/tests/run.py test_diagnosis -k ProofFirst`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test (test_diagnosis ProofFirst)
2. [x] proof_gap on Brief, checked in finish's gaps with the commands about to run
3. [x] CHANGELOG line
## Resume here
<!-- auto -->
- 2026-10-29T03:48:08Z steps 3/3 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_diagnosis.py, plugin/tests/test_task_ergonomics.py
- touched since last checkpoint: plugin/tests/test_diagnosis.py, CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_task_ergonomics.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1907t.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1907i.txt
- failures met: assertionerror: '--lens "adversary:' not found in 'fm: t-0 not finished, nothing ran:\n -…
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_diagnosis -k ProofFirst` → red as expected (exit 1) · Ran 14 tests in 6.6s (8 classes, 16 at a time; slowest: Refuted 6s, WhyNotCaught 3s, NewWork 3s) / FAILED (1 classes) [ran] [tree fa1eb6dcef88] (2026-10-29T03:38:17Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis -k ProofFirst` → exit 0 · Ran 14 tests in 6.1s (8 classes, 16 at a time; slowest: Refuted 6s, WhyNotCaught 3s, NewWork 3s) / OK [ran] [tree add3be1562d2] (2026-10-29T03:38:28Z)
- (step 3) `grep -c T-1906 CHANGELOG.md` → exit 0 · 1 [ran] [tree add3be1562d2] (2026-10-29T03:38:29Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis test_bookkeeping` → exit 0 · Ran 31 tests in 13.5s (16 classes, 16 at a time; slowest: Refuted 12s, StepEvidence 12s, CommitOwnFiles 12s) / OK [ran] [tree 80ce7ee0867e] (2026-10-29T03:39:01Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4130 tests in 196.9s (991 classes, 16 at a time; slowest: Worker 102s, Stop 61s, Bench 50s) / FAILED (1 classes) [ran] [tree 80ce7ee0867e] (2026-10-29T03:45:35Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis test_bookkeeping test_task_ergonomics` → exit 0 · Ran 49 tests in 9.4s (19 classes, 16 at a time; slowest: TaskErgonomics 9s, Refuted 6s, CommitOwnFiles 6s) / OK [ran] [tree 27dda10862e2] (2026-10-29T03:46:21Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, ; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 03:45 UTC; claude plugin test [ran] [tree 27dda10862e2] (2026-10-29T03:50:17Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis -k ProofFirst` → exit 0 · Ran 14 tests in 3.6s (8 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 1s, NewWork 1s) / OK [ran] [tree 27dda10862e2] (2026-10-29T03:50:36Z)
- (audit intent) `self: S; read the diff, the gap is computed once with the commands the close is about to run` → a FIX with no proof is refused before any check runs, with how to give it [tree 27dda10862e2] (2026-10-29T03:50:36Z)
- (audit edge) `self: S; read the diff, the gap is computed once with the commands the close is about to run` → a red run of a command the close is about to run still counts; args.run None is filtered out of then; a Regression test line skips the gap [tree 27dda10862e2] (2026-10-29T03:50:36Z)
- (audit self) `self: S; read the diff, the gap is computed once with the commands the close is about to run` → no findings [tree 27dda10862e2] (2026-10-29T03:50:36Z)
## Log
- 2026-10-29T03:36:15Z created
- 2026-10-29T03:37:06Z planned from capture
- 2026-10-29T03:38:07Z focused
- 2026-10-29T03:46:11Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_diagnosis.py', 'plugin/tests/test_task_ergonomics.py', 'CHANGELOG.md']
- 2026-10-29T03:46:11Z scope: test_task_ergonomics' adversary-hint test now meets the proof gap first; it records none: fixture
- 2026-10-29T03:51:02Z done
- 2026-10-29T03:51:04Z committed 1ea8b8e1 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1893 [FIX S, done, 3 steps] fm task finish counts --expect-fail evidence as the red half of red-to-green proof — lesson: Red-to-green proof must read every way a red r…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-1844 [FIX S, done, 2 steps] FIX: fm task finish re-runs a red step's own failed command instead of refusing
- decision 2026-10-23: Gates behind volt's 2-hour cargo test lock: stop our own queued fm check runs and land the drafted tasks first, then one gate covers all of them bef…
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Lessons
- A refusal known before the checks run must be said before they run: order gap checks ahead of slow work
## Files touched
- plugin/tests/test_diagnosis.py
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/tests/test_task_ergonomics.py
