---
id: T-0741
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T19:57:21Z
updated: 2026-10-09T19:57:38Z
base: 4baa0ff30b2188b331e7cc60072d2ba1ac907dd8
base_tree: cd21e3cc7bcab3d3f2b2c35814a45775366e55b0
verified: strong
---
# MASTER.md names fm bisect (T-0686 left it out; fm doctor's self-docs check fails)
## Raw request
> MASTER.md names fm bisect (T-0686 left it out; fm doctor's self-docs check fails)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the self-docs check passes — verify with `python3 plugin/tests/run.py -p test_doctor.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] name it
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -p test_doctor.py` → ✗ exit 1 · Ran 24 tests in 4.4s (6 classes, 16 at a time; slowest: Command 4s, RestoreState 0s, Checks 0s) / FAILED (1 classes) [ran] [tree cd21e3cc7bca] (2026-10-09T19:57:30Z)
- (ac 1) `python3 plugin/tests/run.py -p test_doctor.py` → exit 0 · Ran 24 tests in 6.4s (6 classes, 16 at a time; slowest: Command 6s, RestoreState 0s, Checks 0s) / OK [ran] [tree 09c9dbb99935] (2026-10-09T19:57:37Z)
- (step 1) `python3 plugin/tests/run.py -p test_doctor.py` → exit 0 · Ran 24 tests in 6.4s (6 classes, 16 at a time; slowest: Command 6s, RestoreState 0s, Checks 0s) / OK [ran] [tree 09c9dbb99935] (2026-10-09T19:57:37Z)
- (audit self) `self: one doc line; the self-docs check passes` → no findings [tree 09c9dbb99935] (2026-10-09T19:57:37Z)
## Log
- 2026-10-09T19:57:21Z created
- 2026-10-09T19:57:21Z focused
- 2026-10-09T19:57:37Z done
- 2026-10-09T19:57:38Z committed 7f0683d (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- research T-0296-review-1: Verdict:** approve with nits. I found no HIGH findings. I read the diff and `fmcore`'s `find_project`/`routing` but did not run any tests. [sta…
- T-0268 [FEATURE M, done, 3 steps] Repo integrity in fm doctor: empty git objects and truncated state, fm doctor --repair — lesson: A health check that is also a gate mus…
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- similar past tasks were M: consider --tier M
## Files touched
- MASTER.md
