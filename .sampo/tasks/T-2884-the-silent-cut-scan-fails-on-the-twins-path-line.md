---
id: T-2884
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T03:49:49Z
updated: 2026-11-04T03:50:49Z
base: af995fe77da0e1b816d6b931792538866f97d1c0
base_tree: 66ebf8775f347322d55bd66d2ba65b4e359417b0
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T03:49:50Z
plan0_scope: []
verified: strong
---
# The silent-cut scan fails on the twins' path:line join in lanes.py (a pair, not a cut list)
## Raw request
> The silent-cut scan fails on the twins' path:line join in lanes.py (a pair, not a cut list)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the silent-cut scan passes — verify with `python3 plugin/tests/run.py test_left_out`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] mark the pair join as not a list
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_left_out` → exit 0 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: LeftOut 0s) / OK [ran] [tree b11e62a7f510] [world 2f1906870a] (2026-11-04T03:49:56Z)
- (ac 1) `python3 plugin/tests/run.py test_left_out` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T03:49:56Z [ran] [tree b11e62a7f510] [world 2f1906870a] (2026-11-04T03:50:06Z)
- (audit edge) `test_left_out red at the start tree (lanes.py:1870), green after` → the comment only exempts this one line; any real cut list elsewhere still fails the scan [tree b11e62a7f510] (2026-11-04T03:50:06Z)
- (audit intent) `test_left_out red at the start tree (lanes.py:1870), green after` → the baseline scan is green again [tree b11e62a7f510] (2026-11-04T03:50:06Z)
- (audit self) `test_left_out red at the start tree (lanes.py:1870), green after` → no findings [tree b11e62a7f510] (2026-11-04T03:50:06Z)
## Log
- 2026-11-04T03:49:49Z created
- 2026-11-04T03:49:49Z focused
- 2026-11-04T03:49:50Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T03:50:46Z done
- 2026-11-04T03:50:49Z committed b48f5ec1 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2250 [FIX S, done, 1 steps] fm find --capture keys twin leads in scan order like rank and fm prove — lesson: Numbering that depends on iteration order must fix its own…
- T-2629 [FIX M, done, 3 steps] The guard reads a redirect's fd number as the fd, not a write target (cp a b 2>/dev/null was a write to ./2), and a parsed python heredoc's…
- research T-2123-review: Verdict: changes needed (2 HIGH, 6 MEDIUM, 5 LOW); fixed or skipped with reason. Reviewer: one foreman:fm-reviewer, five lenses, read-only.
- decision 2026-11-02: Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary…
- similar finished tasks took 1–3 steps
## Regression test
none: the existing scan test_left_out is the regression test; it was red at the start tree (lanes.py:1870, seen in this session's run) and is green now
## Why not caught
T-2861's lane merged without running test_left_out; its affected set didn't include the scan
## Files touched
- plugin/lib/sampo/lanes.py
