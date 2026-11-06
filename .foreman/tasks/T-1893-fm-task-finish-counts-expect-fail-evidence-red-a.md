---
id: T-1893
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_task_ergonomics.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T01:58:16Z
updated: 2026-10-29T02:14:59Z
base: 0979983cfb1815ae7453bb17d8f9c83da286f529
base_tree: e77eb5e20c86a9bd178864b6b45ea6f3c11b98c1
plan0_at: 2026-10-29T02:07:54Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_task_ergonomics.py, CHANGELOG.md]
verified: strong
---
# fm task finish counts --expect-fail evidence as the red half of red-to-green proof
## Raw request
> fm task finish counts --expect-fail evidence (red as expected) as the red half of red-to-green proof: red_green_cmd only matched a plain failure, so every test-first FIX recorded with --expect-fail was refused
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an --expect-fail red run then a pass of the same command is red-green proof — verify with `python3 plugin/tests/run.py test_task_ergonomics`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: ExpectFail red then pass
2. [x] red_green_cmd counts red as expected
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics` → ✗ exit 1 · Ran 18 tests in 10.8s (3 classes, 16 at a time; slowest: TaskErgonomics 10s, ExpectFail 3s, ScopeWords 1s) / FAILED (1 classes) [ran] [tree f248bf291b46] (2026-10-29T02:08:06Z)
- (step 2) `python3 plugin/tests/run.py test_task_ergonomics` → exit 0 · Ran 18 tests in 10.1s (3 classes, 16 at a time; slowest: TaskErgonomics 10s, ExpectFail 3s, ScopeWords 0s) / OK [ran] [tree 9c94a54c1f6a] (2026-10-29T02:08:26Z)
- (step 3) `grep -c T-1893 CHANGELOG.md` → exit 0 · 1 [ran] [tree 9c94a54c1f6a] (2026-10-29T02:08:26Z)
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics.ExpectFail` → exit 0 · Ran 4 tests in 3.1s (1 classes, 16 at a time; slowest: ExpectFail 3s) / OK [ran] [tree 9c94a54c1f6a] (2026-10-29T02:08:36Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.8    44.1     150  [0] / SessionEnd                  35.1    37.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree 9c94a54c1f6a] (2026-10-29T02:14:38Z)
- (ac 1) `python3 plugin/tests/run.py test_task_ergonomics` → exit 0 · Ran 18 tests in 5.9s (3 classes, 16 at a time; slowest: TaskErgonomics 6s, ExpectFail 2s, ScopeWords 0s) / OK [ran] [tree 9c94a54c1f6a] (2026-10-29T02:14:50Z)
- (audit intent) `self-review of the one-line diff plus the lenses below; gates exit 0` → an --expect-fail red run followed by a pass of the same command now satisfies red-to-green, so finish no longer refuses test-first FIXes [tree 9c94a54c1f6a] (2026-10-29T02:14:50Z)
- (audit adversary) `self-review of the one-line diff plus the lenses below; gates exit 0` → a pass recorded before the red run still isn't proof (order is kept by the existing scan); a red with a different command doesn't count [tree 9c94a54c1f6a] (2026-10-29T02:14:50Z)
- (audit edge) `self-review of the one-line diff plus the lenses below; gates exit 0` → no pass yet returns None (tested); a plain ✗ exit still counts as before [tree 9c94a54c1f6a] (2026-10-29T02:14:50Z)
- (audit self) `self-review of the one-line diff plus the lenses below; gates exit 0` → no findings [tree 9c94a54c1f6a] (2026-10-29T02:14:50Z)
## Log
- 2026-10-29T01:58:16Z created
- 2026-10-29T01:59:50Z planned from capture
- 2026-10-29T02:07:53Z focused
- 2026-10-29T02:14:58Z done
- 2026-10-29T02:14:59Z committed c36e8b06 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0165 [FEATURE S, done, 3 steps] A step whose newest run failed closes when the same command passed later (the red run of red→green) — lesson: Evidence rules should fol…
- research T-1518-review: Verdict:** approve with nits. I found nothing in `--repeat` that forges or weakens evidence. The canary has two real weaknesses. I had no shell, …
- T-1486 [FEATURE S, done, 2 steps] Fm task evidence --expect-fail: record a run that must fail (non-zero exit required, recor — lesson: Give each evidence kind its own wo…
- decision 2026-10-14: Block T-0760 rather than edit its failing AC, since the AC already has evidence
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_core.py
## Lessons
- Red-to-green proof must read every way a red run is recorded, including --expect-fail's 'red as expected'
## Plan gaps
- failed first: step 1 Failing test: ExpectFail red then pass
## Files touched
- plugin/tests/test_task_ergonomics.py
- CHANGELOG.md
- plugin/lib/fmcore.py
