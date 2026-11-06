---
id: T-1919
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T04:57:31Z
updated: 2026-10-29T05:42:33Z
base: b58a867318b182facebb0f11899e05b4510bb9b6
base_tree: 6911a75f9eb48b362c1392deddfc30881781ea27
plan0_at: 2026-10-29T05:35:43Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py, CHANGELOG.md]
verified: strong
---
# Prove keeps a changed tests-folder file the start tree has at its start version
## Raw request
> FIX: fm task prove copies every TESTISH file to the start tree, so code under test that lives in a tests folder (plugin/tests/run.py) is carried too and the red run passes; carry only test-named files and helpers the new tests import
## Interpretation
A runner or helper the start tree has, changed by the task, is code under change; a brand-new helper is test scaffolding
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task prove leaves a changed, non-test-named tests-folder file that exists at the start commit (run.py) at its start version and names it; new helpers and test-named files still come over — verify with `python3 plugin/tests/run.py test_diagnosis`
## Non-goals
## Approach (options → choice → why)
rejected: keep T-1845's after-the-fact hint only (still costs a manual red run per runner fix)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test: changed runner + new helper; prove proves and names the kept runner (red on today's prove)
2. [x] Skip copying non-test-named files the start tree has; report them as kept
## Resume here
<!-- auto -->
- 2026-10-29T05:36:07Z step 2/2: Skip copying non-test-named files the start tree has; report them as kept
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py
- touched since last checkpoint: CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_diagnosis` → ✗ exit 1 · Ran 14 tests in 4.5s (8 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 2s, NewWork 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a5b5cafe8093] (2026-10-29T05:35:56Z)
- `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 14 tests in 3.7s (8 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 2s, NewWork 1s) / OK [ran] [tree a5b5cafe8093] (2026-10-29T05:35:56Z)
- (step 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 14 tests in 3.6s (8 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 2s, NewWork 1s) / OK [ran] [tree a5b5cafe8093] (2026-10-29T05:36:06Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis test_cli test_lifecycle` → ✗ exit 1 · run.py: no test matches test_lifecycle [ran] [tree a5b5cafe8093] (2026-10-29T05:36:07Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis test_cli` → exit 0 · Ran 143 tests in 23.8s (45 classes, 16 at a time; slowest: TaskLifecycle 24s, CaptureAndIntake 9s, StateViews 9s) / OK [ran] [tree a5b5cafe8093] (2026-10-29T05:37:41Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis 2>&1 | grep -E "^(FAIL|AssertionError|.*Error:)" | head -5` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree 363ba75b5751] (2026-10-29T05:40:30Z)
- (step 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 14 tests in 3.7s (8 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 2s, NewWork 1s) / OK [ran] [tree 41ed8fb053df] (2026-10-29T05:41:31Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis test_cli` → exit 0 · Ran 143 tests in 23.8s (45 classes, 16 at a time; slowest: TaskLifecycle 24s, CaptureAndIntake 9s, StateViews 9s) / OK [ran] [tree 41ed8fb053df] (2026-10-29T05:41:55Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 14 tests in 3.7s (8 classes, 16 at a time; slowest: Refuted 3s, WhyNotCaught 2s, NewWork 1s) / OK [ran] [tree 41ed8fb053df] (2026-10-29T05:42:06Z)
- (audit intent) `fm-reviewer (approve with nits): 3 findings fixed test-first` → ok — runner kept and named; new and imported helpers carried [tree 41ed8fb053df] (2026-10-29T05:42:06Z)
- (audit edge) `fm-reviewer (approve with nits): 3 findings fixed test-first` → a test named for the file keeps it though imported (test_run.py ↔ run.py); conftest always carried [tree 41ed8fb053df] (2026-10-29T05:42:06Z)
- (audit adversary) `fm-reviewer (approve with nits): 3 findings fixed test-first` → ok — paths only from git diff, no shell [tree 41ed8fb053df] (2026-10-29T05:42:06Z)
- (audit maintainer) `fm-reviewer (approve with nits): 3 findings fixed test-first` → helper-carry half now tested; ledger event lists carried and kept [tree 41ed8fb053df] (2026-10-29T05:42:06Z)
## Log
- 2026-10-29T04:57:31Z created
- 2026-10-29T05:09:10Z planned from capture
- 2026-10-29T05:35:42Z focused
- 2026-10-29T05:42:31Z done
- 2026-10-29T05:42:33Z committed 962230ac (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0809 [FIX S, dropped, 2 steps] fm task prove treats only test files as tests, not every file in a tests folder
- T-1845 [FIX S, done, 2 steps] FIX: fm task prove names the changed non-test files it copied onto the start tree when the check passes there
- T-1652 [FEATURE M, done, 4 steps] Brand assets, Figma-as-data import, inferred tokens, a token x-ray, a foreman-design plugin entry — lesson: a tokens importer must coun…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
- similar finished tasks took 2–4 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
T-1845's test changed run.py and a new helper together; nothing covered a runner the start tree already had
## Lessons
- A prove fix that keeps files must test the carried half too, or deleting the copy stays green
## Plan gaps
- failed first: step 2 Skip copying non-test-named files the start tree has; report them as kept
## Files touched
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/tests/test_diagnosis.py
