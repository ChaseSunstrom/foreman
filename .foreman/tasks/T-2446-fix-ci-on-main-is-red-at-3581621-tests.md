---
id: T-2446
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T22:59:40Z
updated: 2026-11-01T04:16:38Z
trigger: ci-red
trigger_key: 09aeed4b8bce88fb
base: 126d4ec84291d24b9152cbd6889f936c64d6d861
base_tree: a6f47af45d9057ea1944d53b64ab640068a7ff7e
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-01T04:09:22Z
plan0_scope: []
verified: strong
---
# FIX: CI on main is red at 3581621 (tests)
## Raw request
> FIX: CI on main is red at 3581621 (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/foreman/commit/3581621bceb8bd6c9a593aa90d8e4c3e21126c32
> CI-red: 3581621bceb8bd6c9a593aa90d8e4c3e21126c32
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the release proof's three setuptools-built cases skip with a reason where setuptools isn't installed and still run where it is — verify with `python3 plugin/tests/run.py test_prove -k release_proof`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] skip the setuptools-built ReleaseProof cases without setuptools; pin the skip with a test
## Resume here
## Docs impact
none: test-only change
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove -k without_setuptools` → ✗ exit 1 · run.py: no test matches test_prove with -k without_setuptools; did you mean -k ReleaseProofWithoutSetuptools? [ran] [tree dc99d1726061] (2026-11-01T04:10:00Z)
- (step 1) `python3 plugin/tests/run.py test_prove -k skip_without_setuptools` → ✗ exit 1 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: ReleaseProofWithoutSetuptools 1s) / FAILED (1 classes: test_prove.ReleaseProofWithoutSetuptools) [ran] [tree 4adbb1db391b] (2026-11-01T04:10:07Z)
- (step 1) `python3 plugin/tests/run.py test_prove -k skip_without_setuptools` → ✗ exit 1 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ReleaseProofWithoutSetuptools 1s) / FAILED (1 classes: test_prove.ReleaseProofWithoutSetuptools) [ran] [tree 0126a73b9ef7] (2026-11-01T04:10:18Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k release_proof` → ✗ exit 1 · Ran 8 tests in 3.6s (2 classes, 16 at a time; slowest: ReleaseProof 3s, ReleaseProofWithoutSetuptools 1s) / FAILED (1 classes: test_prove.ReleaseProofWithoutSetuptools) [ran] [tree 0126a73b9ef7] (2026-11-01T04:10:22Z)
- `python3 plugin/tests/run.py test_prove -k skip_without_setuptools` → ✗ exit 1 · Ran 3 tests in 1.8s (1 classes, 16 at a time; slowest: ReleaseProofWithoutSetuptools 1s) / FAILED (1 classes: test_prove.ReleaseProofWithoutSetuptools) (start tree + this task's tests) [ran] [tree 0126a73b9ef7] (2026-11-01T04:10:25Z)
- `python3 plugin/tests/run.py test_prove -k skip_without_setuptools` → ✗ exit 1 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ReleaseProofWithoutSetuptools 1s) / FAILED (1 classes: test_prove.ReleaseProofWithoutSetuptools) [ran] [tree 0126a73b9ef7] (2026-11-01T04:10:25Z)
- (step 1) `python3 plugin/tests/run.py test_prove -k skip_without_setuptools` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: ReleaseProofWithoutSetuptools 1s) / OK [ran] [tree 327f1951f40c] (2026-11-01T04:10:40Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k release_proof` → exit 0 · Ran 6 tests in 2.9s (2 classes, 16 at a time; slowest: ReleaseProof 3s, ReleaseProofWithoutSetuptools 1s) / OK [ran] [tree 327f1951f40c] (2026-11-01T04:10:43Z)
- `python3 plugin/tests/run.py test_prove -k skip_without_setuptools` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: ReleaseProofWithoutSetuptools 1s) / OK (start tree + this task's tests) [ran] [tree 327f1951f40c] (2026-11-01T04:10:46Z)
- `python3 plugin/tests/run.py test_prove -k skip_without_setuptools` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: ReleaseProofWithoutSetuptools 1s) / OK [ran] [tree 327f1951f40c] (2026-11-01T04:10:46Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k release_proof` → exit 0 · Ran 6 tests in 2.9s (2 classes, 16 at a time; slowest: ReleaseProof 3s, ReleaseProofWithoutSetuptools 1s) / OK [ran] [tree 327f1951f40c] (2026-11-01T04:16:13Z)
- (audit edge) `self-review; reproduced CI locally with a python3 -S wrapper (no setuptools): red before the skip, green after; full fm check green` → the skip asks the python3 fm prove will run (PATH), not the test process's interpreter, so a runner whose PATH python lacks setuptools skips and one that has it still builds; the download and refused cases never needed setuptools and still run [tree 327f1951f40c] (2026-11-01T04:16:13Z)
- (audit intent) `self-review; reproduced CI locally with a python3 -S wrapper (no setuptools): red before the skip, green after; full fm check green` → CI's ubuntu jobs went red on ReleaseProof only because their python3 has no setuptools; fm prove --release builds offline by design, so those three cases skip with a reason there, like the Postgres ones [tree 327f1951f40c] (2026-11-01T04:16:13Z)
- (audit self) `self-review; reproduced CI locally with a python3 -S wrapper (no setuptools): red before the skip, green after; full fm check green` → no findings [tree 327f1951f40c] (2026-11-01T04:16:13Z)
## Log
- 2026-10-31T22:59:40Z created
- 2026-11-01T04:09:20Z set tier=S
- 2026-11-01T04:09:21Z planned: it has criteria and steps
- 2026-11-01T04:09:21Z CI run 41245663820 (T-2445 has the log): test_prove.ReleaseProof fails on the ubuntu jobs because the runner's python has no setuptools; fm prove --release builds offline by design, so those cases read unproven there. The macOS InfraProof failure is T-2441's (non-blocking job).
- 2026-11-01T04:09:22Z focused
- 2026-11-01T04:09:22Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-01T04:10:25Z scope: plugin/tests/test_prove.py only (the release proof's tests); no product code changes
- 2026-11-01T04:16:09Z scope: plugin/tests/test_prove.py only
- 2026-11-01T04:16:35Z done
- 2026-11-01T04:16:38Z committed 99269500 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2014 [FIX M, dropped, 0 steps] FIX: CI on main is red at 104c441 (tests)
- T-1816 [FIX M, dropped, 0 steps] FIX: CI on main is red at eba6705 (tests)
- T-1842 [FIX S, done, 2 steps] FIX: CI tests time out: split the suite into 2 shards per job
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- the similar finished task took 2 steps
- start here (files T-1842 touched): plugin/tests/test_run.py, plugin/tests/run.py, .github/workflows/test.yml, CHANGELOG.md
## Why not caught
local python3 ships setuptools; CI's ubuntu python3 doesn't, and no local run removed it
## Lessons
- A test that builds with a site package must skip where the interpreter the product runs (PATH's python3) lacks it; python3 -S reproduces a bare runner locally
## Plan gaps
- failed first: step 1 skip the setuptools-built ReleaseProof cases without setuptools; pin the skip with a test
## Files touched
- plugin/tests/test_prove.py
