---
id: T-1190
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_verify_check.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T12:47:45Z
updated: 2026-10-16T13:16:12Z
base: 2937170ee4d8fdb2b29c9f6f3b2018cf71157084
base_tree: 58dd966dc41999ecdc3025cf7f04bcf01eb41b14
plan0_at: 2026-10-16T13:08:08Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_verify_check.py, CHANGELOG.md]
verified: strong
---
# The verify check (T-1145) reads the value of 'run.py -k NAME' as a test module and notes '
## Raw request
> The verify check (T-1145) reads the value of 'run.py -k NAME' as a test module and notes 'NAME.py doesn't exist yet': skip the word after -k (and other value-taking flags)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a verify with 'run.py -k NAME' or 'unittest -k NAME' gets no 'doesn't exist yet' note for NAME; a real missing module still does — verify with `python3 plugin/tests/run.py test_verify_check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test + skip flag values in _missing_target
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verify_check` → ✗ exit 1 · Ran 4 tests in 8.9s (1 classes, 16 at a time; slowest: VerifyCheck 9s) / FAILED (1 classes) [ran] [tree b73603dba3fe] (2026-10-16T13:08:23Z)
- (step 1) `python3 plugin/tests/run.py test_verify_check` → exit 0 · Ran 4 tests in 10.5s (1 classes, 16 at a time; slowest: VerifyCheck 10s) / OK [ran] [tree 7a8204c21457] (2026-10-16T13:08:43Z)
- `python3 plugin/tests/run.py test_verify_check` → ✗ exit 1 · Ran 4 tests in 24.3s (1 classes, 16 at a time; slowest: VerifyCheck 22s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7513b8425fea] (2026-10-16T13:09:42Z)
- `python3 plugin/tests/run.py test_verify_check` → exit 0 · Ran 4 tests in 23.6s (1 classes, 16 at a time; slowest: VerifyCheck 23s) / OK [ran] [tree 7513b8425fea] (2026-10-16T13:09:42Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_check` → exit 0 · Ran 4 tests in 27.4s (1 classes, 16 at a time; slowest: VerifyCheck 26s) / OK [ran] [tree 7513b8425fea] (2026-10-16T13:10:12Z)
- (audit edge) `self: one helper drops flags and the values of value-taking flags (-k, -p, -j, --pattern, -s/-t for unittest discovery) before module names are checked; both run.py and -m unittest paths use it` → an unknown value-taking flag's value would still be read as a module, giving only a note, never a refusal [tree 7513b8425fea] (2026-10-16T13:10:12Z)
- (audit self) `self: one helper drops flags and the values of value-taking flags (-k, -p, -j, --pattern, -s/-t for unittest discovery) before module names are checked; both run.py and -m unittest paths use it` → no findings [tree 7513b8425fea] (2026-10-16T13:10:12Z)
## Log
- 2026-10-16T12:47:45Z created
- 2026-10-16T13:08:06Z set scope=['plugin/lib/fmcore.py', 'plugin/tests/test_verify_check.py', 'CHANGELOG.md']
- 2026-10-16T13:08:07Z focused
- 2026-10-16T13:16:12Z done
- 2026-10-16T13:16:12Z committed a5e20f2e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0802 [FEATURE S, done, 2 steps] fm research list and fm research show NAME — lesson: when users and criteria keep reaching for a command that doesn't exist, add it
- T-1145 [FEATURE S, done, 2 steps] Check a verify command when it is added (fm task ac add/edit, --ac ':: cmd'): a python tes
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_core.py
## Plan gaps
- failed first: step 1 Failing test + skip flag values in _missing_target
## Files touched
- plugin/tests/test_verify_check.py
- plugin/lib/fmcore.py
- CHANGELOG.md
