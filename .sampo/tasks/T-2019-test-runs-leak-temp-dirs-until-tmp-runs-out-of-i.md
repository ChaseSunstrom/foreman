---
id: T-2019
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T17:19:44Z
updated: 2026-10-29T17:35:32Z
base: fadef9478419589fb846aae16eade243a189973f
base_tree: 8963f9cb49b05da51b0ff1baaf0759725edc5174
plan0_at: 2026-10-29T17:19:45Z
plan0_scope: []
verified: strong
---
# Test runs leak temp dirs until /tmp runs out of inodes: each class gets its own TMPDIR, removed after it, and a dead run's are swept
## Raw request
> Test runs leak temp dirs until /tmp runs out of inodes: each class gets its own TMPDIR, removed after it, and a dead run's are swept
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a class's temp files are removed after it runs, and a dead run's temp dir is swept at the next start — verify with `python3 plugin/tests/run.py test_run -k tmp`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] free the 43.9k stale /tmp test dirs
2. [x] run.py: per-class TMPDIR, rmtree after, sweep dead pids' dirs; test
## Resume here
<!-- auto -->
- 2026-10-29T17:31:05Z steps 2/2 done
- git: foreman/build; 3 uncommitted: plugin/tests/run.py, plugin/tests/test_bench_family.py, plugin/tests/test_run.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/sweep_tmp.py, plugin/tests/test_bench_family.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/reuse.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/genlazy.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/imp_fm.py, plugin/tests/run.py, plugin/tests/test_run.py, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/lazy_test.txt
- failures met: assertionerror: [{'project': none, 'kind': 'child_shells', 'severity': 'action', 'detail'…
## Docs impact
## Verification evidence
- (step 1) `df -i /tmp` → exit 0 · Filesystem      Inodes IUsed   IFree IUse% Mounted on / tmpfs          1048576 30479 1018097    3% /tmp [ran] [tree 8963f9cb49b0] (2026-10-29T17:20:04Z)
- (ac 1) `python3 plugin/tests/run.py test_run -k tmp 2>&1 | grep -E "Error|assert|FAILED|OK" | head -6` → ✗ exit 1 · FAILED (failures=1, errors=1) / FAILED (1 classes) [ran] [tree f15743807abf] (2026-10-29T17:20:29Z)
- (step 2) `python3 plugin/tests/run.py test_run 2>&1 | tail -3` → exit 0 · Ran 59 tests in 5.4s (33 classes, 16 at a time; slowest: Ship 5s, Ambient 5s, Hang 4s) / OK [ran] [tree 68ca7786788f] (2026-10-29T17:20:53Z)
- (step 2) `python3 plugin/tests/run.py test_ci_annotations test_run test_bench_family` → exit 0 · Ran 87 tests in 20.5s (46 classes, 16 at a time; slowest: Judged 20s, Duel 15s, Marathon 15s) / OK [ran] [tree 5a888e5ed5f1] (2026-10-29T17:21:26Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4223 tests in 183.1s (996 classes, 16 at a time; slowest: Worker 98s, Stop 53s, Fakes 44s) / FAILED (1 classes) (pre-existing: it also failed before this task) [ran] [tree ecdfbce04eaa] (2026-10-29T17:25:21Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py, plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 17:14 UTC; claude plugin test [ran] [tree e1f8a6534e1a] (2026-10-29T17:30:02Z)
- (ac 1) `python3 plugin/tests/run.py test_run -k tmp` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Tmp 0s) / OK [ran] [tree e1f8a6534e1a] (2026-10-29T17:32:20Z)
- (audit intent) `self-review (budget spent: no subagents): per-class TMPDIR removed in a finally; sweep removes only fmtest- dirs whose pid is dead and skips other users' (PermissionError); gates green, 4223 tests` → test runs stop filling /tmp; a killed run's leftovers go on the next start [tree e1f8a6534e1a] (2026-10-29T17:32:20Z)
- (audit edge) `self-review (budget spent: no subagents): per-class TMPDIR removed in a finally; sweep removes only fmtest- dirs whose pid is dead and skips other users' (PermissionError); gates green, 4223 tests` → killed run swept next start; a live concurrent run's dirs kept; prefix fmtest- avoids tidy's -tmp-fm- child-shell regex [tree e1f8a6534e1a] (2026-10-29T17:32:20Z)
- (audit self) `self-review (budget spent: no subagents): per-class TMPDIR removed in a finally; sweep removes only fmtest- dirs whose pid is dead and skips other users' (PermissionError); gates green, 4223 tests` → no findings [tree e1f8a6534e1a] (2026-10-29T17:32:20Z)
## Log
- 2026-10-29T17:19:44Z created
- 2026-10-29T17:19:45Z focused
- 2026-10-29T17:26:19Z steer: gates caught tidy's child_shells regex (-tmp-fm-) matching the per-class fm-run- temp paths; prefix is now fmtest-
- 2026-10-29T17:32:37Z done
- 2026-10-29T17:32:39Z committed 67768c6b (3 files)
- 2026-10-29T17:32:43Z guard authorization added: publish
- 2026-10-29T17:35:32Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- research T-1284-review: Verdict:** approve with nits. I found no way to make the guard treat an outside write as inside a project, or a project or state write as outside…
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- decision 2026-10-23: Usage pace: subagents paused at 75% weekly usage with 27% of the week gone; work continues in the main thread, security items first (T-1751, T-1749)…
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
- plugin/tests/test_bench_family.py
- CHANGELOG.md
