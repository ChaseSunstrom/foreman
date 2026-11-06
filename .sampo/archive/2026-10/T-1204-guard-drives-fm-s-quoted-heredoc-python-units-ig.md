---
id: T-1204
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T14:48:42Z
updated: 2026-10-16T14:59:11Z
base: 7f00f694eba2ef07f6b44454c7837f6c5e936fa4
base_tree: 072598071f740578cf1b655360ad08cb339fce03
plan0_at: 2026-10-16T14:55:45Z
plan0_scope: []
verified: strong
---
# Guard: heredoc python gets the PYTHONPATH and earlier-cd checks -c code has
## Raw request
> Guard: _drives_fm's quoted-heredoc python units ignore an inherited or exported PYTHONPATH and a cd on an earlier line (the -c path from T-1194 refuses both); give heredoc units the same checks
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a quoted python heredoc whose fm text is only in strings is still refused when PYTHON* settings are inherited or set in the command, or a cd outside its own cd chain moves the folder it imports from; the existing heredoc allow cases still pass — verify with `python3 plugin/tests/run.py test_guard test_guard_cases test_replay`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing cases: exported PYTHONPATH then heredoc; inherited PYTHONPATH; cd on an earlier line then heredoc importing json beside a json.py
2. [x] In _drives_fm, apply the PYTHON* check and the moved-folder rule to heredoc units too
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay` → exit 0 · Ran 186 tests in 18.2s (59 classes, 16 at a time; slowest: GuardAgainstBash 17s, GuardCases 7s, Hook 5s) / OK [ran] [tree 2be248c194c0] (2026-10-16T14:57:16Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay` → exit 0 · Ran 186 tests in 19.8s (59 classes, 16 at a time; slowest: GuardAgainstBash 19s, GuardCases 6s, Hook 5s) / OK [ran] [tree 2be248c194c0] (2026-10-16T14:57:36Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay` → exit 0 · Ran 186 tests in 15.9s (59 classes, 16 at a time; slowest: GuardAgainstBash 15s, GuardCases 8s, Hook 6s) / OK [ran] [tree 2be248c194c0] (2026-10-16T14:57:53Z)
- (audit adversary) `self: tightening only (two new refusal conditions, both already applied to -c units); fm replay of the real-command corpus: 0 newly blocked, 0 newly allowed; 24 labelled cases, 0 drifted` → PYTHON* text anywhere outside the heredoc bodies or inherited PYTHON* env refuses when any python unit names fm modules (sitecustomize from PYTHONPATH runs without an import); a cd/pushd/popd outside every unit's own chain makes every run folder unknown, so an import there refuses [tree 2be248c194c0] (2026-10-16T14:57:53Z)
- (audit self) `self: tightening only (two new refusal conditions, both already applied to -c units); fm replay of the real-command corpus: 0 newly blocked, 0 newly allowed; 24 labelled cases, 0 drifted` → no findings [tree 2be248c194c0] (2026-10-16T14:57:53Z)
## Log
- 2026-10-16T14:48:42Z created
- 2026-10-16T14:55:44Z planned from capture
- 2026-10-16T14:55:45Z focused
- 2026-10-16T14:57:37Z scope: CHANGELOG line
- 2026-10-16T14:59:09Z done
- 2026-10-16T14:59:11Z committed 8c9c6d87 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- T-1194 [FIX M, done, 2 steps] Guard parses python -c code like quoted heredoc bodies before calling it Foreman-driving — lesson: Loosening a guard rule needs the mined r…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- the similar finished task took 2 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
