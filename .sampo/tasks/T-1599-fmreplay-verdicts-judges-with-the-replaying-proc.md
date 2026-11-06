---
id: T-1599
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmreplay.py, plugin/tests/test_guard_cases.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T20:19:06Z
updated: 2026-10-22T20:33:45Z
base: 7426a2533ba8138245e95760fffb777f38662e0c
base_tree: eb3df44e6415367dbb0773e8ab02154443c90b71
plan0_at: 2026-10-22T20:31:34Z
plan0_scope: [plugin/lib/fmreplay.py, plugin/tests/test_guard_cases.py, CHANGELOG.md]
verified: strong
---
# Fmreplay.verdicts judges with the replaying process's PYTHONPATH: with PYTHONPATH set, the
## Raw request
> fmreplay.verdicts judges with the replaying process's PYTHONPATH: with PYTHONPATH set, the T-1194 python3 -c cases refuse and fm replay --cases goes red; replay should clear Python path variables for the guard as the hook sees them
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm replay judges the same with PYTHONPATH (and the other Python path variables) set in the replaying shell as without — verify with `python3 plugin/tests/run.py test_guard_cases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] verdicts clears the Python path variables while it judges
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus.test_an_inherited_pythonpath_doesnt_change_the_replay` → red as expected (exit 1) · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: AllowCorpus 0s) / FAILED (1 classes) [ran] [tree f6923f4e1b46] (2026-10-22T20:32:53Z)
- `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus.test_an_inherited_pythonpath_doesnt_change_the_replay` → ✗ exit 1 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: AllowCorpus 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 900f1a62635d] (2026-10-22T20:33:16Z)
- `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus.test_an_inherited_pythonpath_doesnt_change_the_replay` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: AllowCorpus 0s) / OK [ran] [tree 900f1a62635d] (2026-10-22T20:33:16Z)
- (step 2) `python3 plugin/tests/run.py test_guard_cases test_guard_mine test_safety_gate` → exit 0 · Ran 43 tests in 7.9s (5 classes, 16 at a time; slowest: SafetyGate 8s, ReleaseGate 5s, GuardCases 4s) / OK [ran] [tree 900f1a62635d] (2026-10-22T20:33:25Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 25 tests in 4.7s (2 classes, 16 at a time; slowest: GuardCases 4s, AllowCorpus 1s) / OK [ran] [tree 900f1a62635d] (2026-10-22T20:33:30Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 25 tests in 4.5s (2 classes, 16 at a time; slowest: GuardCases 4s, AllowCorpus 1s) / OK [ran] [tree 49abcd4592c4] (2026-10-22T20:33:36Z)
- (audit adversary) `self: intent: replay verdicts don't depend on the replaying shell's Python settings · adversary: only the replay's judging changes; the live hook still reads its own environment, where an inherited PYTHONPATH rightly makes python -c suspect · edge: variables restored in finally, even when the guard raises · operator: none · maintainer: subprocess test red first` → the guard rule is untouched; a hook with PYTHONPATH set still refuses those python -c cases [tree 49abcd4592c4] (2026-10-22T20:33:36Z)
- (audit self) `self: intent: replay verdicts don't depend on the replaying shell's Python settings · adversary: only the replay's judging changes; the live hook still reads its own environment, where an inherited PYTHONPATH rightly makes python -c suspect · edge: variables restored in finally, even when the guard raises · operator: none · maintainer: subprocess test red first` → no findings [tree 49abcd4592c4] (2026-10-22T20:33:36Z)
## Log
- 2026-10-22T20:19:06Z created
- 2026-10-22T20:31:27Z set scope=['plugin/lib/fmreplay.py', 'plugin/tests/test_guard_cases.py', 'CHANGELOG.md']
- 2026-10-22T20:31:34Z focused
- 2026-10-22T20:33:42Z done
- 2026-10-22T20:33:45Z committed dae2bc03 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1401-review: Verdict: approve with nits.** Both acceptance criteria are met and the stubbed-replay tests cover them. One MEDIUM finding is a silent way to pas…
- T-1401 [SECURITY M, done, 3 steps] Unattended fm code and fm release --push refuse on a stale or red safety replay — lesson: A gate fed by a self-reported ledger record …
- research T-1517-review: Verdict:** approve with nits. I found no bypass of the guard lock, no guard rule change, and nothing dangerous or secret in the allow-corpus. The…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_replay.py
## Why not caught
the unit tests popped the variables themselves; fm replay never did
## Lessons
- A replay must recreate the judge's environment, not inherit the runner's: env-dependent rules otherwise flip in CI
## Files touched
- plugin/tests/test_guard_cases.py
- plugin/lib/fmreplay.py
- CHANGELOG.md
