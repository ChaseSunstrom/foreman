---
id: T-1907
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_task_ergonomics.py, CHANGELOG.md]
depends_on: [T-1905]
source: discovered
created: 2026-10-29T03:46:38Z
updated: 2026-10-29T04:17:20Z
base: 139980e0d597c191defdd78fac002ec2943a4709
base_tree: b89e6e7e9b86dcb290668fa27183537fcca64c36
plan0_at: 2026-10-29T04:08:16Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_task_ergonomics.py, CHANGELOG.md]
verified: strong
---
# Fm task finish asks for the adversary lens before its checks run
## Raw request
> fm task finish asks for the adversary lens on security-sensitive files only after its checks run (fm task done's refusal); check it with the other gaps first, as T-1906 does for the red-to-green proof
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a close over a security-sensitive file with no adversary lens is refused before any check runs — verify with `python3 plugin/tests/run.py test_task_ergonomics -k adversary`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test (test_task_ergonomics)
2. [x] _task_files shared by done and finish; finish's gaps ask for the adversary lens
3. [x] CHANGELOG line
## Resume here
<!-- auto -->
- 2026-10-29T04:13:11Z steps 3/3 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_task_ergonomics.py
- touched since last checkpoint: plugin/tests/test_task_ergonomics.py, CHANGELOG.md, plugin/lib/fmcli.py
- failures met: assertionerror: ('test_guard.py', ' for where in (link, real): # no scratch to fall bac')
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics -k adversary` → red as expected (exit 1) · Ran 23 tests in 11.2s (6 classes, 16 at a time; slowest: TaskErgonomics 11s, ExpectFail 3s, DiffGates 3s) / FAILED (1 classes) [ran] [tree 3d17e0b2e4dd] (2026-10-29T04:08:37Z)
- (step 2) `python3 plugin/tests/run.py test_task_ergonomics -k adversary` → exit 0 · Ran 23 tests in 11.7s (6 classes, 16 at a time; slowest: TaskErgonomics 11s, ExpectFail 3s, DiffGates 3s) / OK [ran] [tree d0119cec50b2] (2026-10-29T04:08:50Z)
- (step 3) `grep -n 'T-1907' CHANGELOG.md` → exit 0 · 4:- fm task finish asks for the adversary lens on a security-sensitive change before any check runs, where fm task done asked for it only after the close's checks had run (T-1907). [ran] [tree d0119cec50b2] (2026-10-29T04:08:58Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                42.2    49.1     150  [0] / SessionEnd                  36.9    38.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree d0119cec50b2] (2026-10-29T04:16:04Z)
- (ac 1) `python3 plugin/tests/run.py test_task_ergonomics -k adversary` → exit 0 · Ran 23 tests in 9.4s (6 classes, 16 at a time; slowest: TaskErgonomics 9s, ExpectFail 2s, DiffGates 1s) / OK [ran] [tree d0119cec50b2] (2026-10-29T04:16:25Z)
- (audit intent) `self-review: the adversary gap joins finish's other pre-check refusals, reusing cmd_task_done's file test` → finish now refuses a risky-file task without the adversary lens before any check runs [tree d0119cec50b2] (2026-10-29T04:16:25Z)
- (audit edge) `self-review: the adversary gap joins finish's other pre-check refusals, reusing cmd_task_done's file test` → a task touching no risky file gets no new gap; done's own refusal still stands [tree d0119cec50b2] (2026-10-29T04:16:25Z)
- (audit adversary) `self-review: the adversary gap joins finish's other pre-check refusals, reusing cmd_task_done's file test` → the check reads the same touched-file list done uses, so finish can't be talked past it [tree d0119cec50b2] (2026-10-29T04:16:25Z)
- (audit self) `self-review: the adversary gap joins finish's other pre-check refusals, reusing cmd_task_done's file test` → no findings [tree d0119cec50b2] (2026-10-29T04:16:25Z)
## Log
- 2026-10-29T03:46:38Z created
- 2026-10-29T03:47:21Z planned from capture
- 2026-10-29T04:08:14Z focused
- 2026-10-29T04:17:18Z done
- 2026-10-29T04:17:20Z committed e60f9b34 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1906 [FIX S, done, 3 steps] Fm task finish checks a FIX's red-to-green proof before running its checks — lesson: A refusal known before the checks run must be said bef…
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-1893 [FIX S, done, 3 steps] fm task finish counts --expect-fail evidence as the red half of red-to-green proof — lesson: Red-to-green proof must read every way a red r…
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- A refusal done makes late should run where finish gathers its gaps, before the costly checks
## Files touched
- plugin/tests/test_task_ergonomics.py
- CHANGELOG.md
- plugin/lib/fmcli.py
