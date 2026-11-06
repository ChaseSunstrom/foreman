---
id: T-0888
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:29:55Z
updated: 2026-10-15T15:32:43Z
base: b078702f9f841a475d4d2a010e92dbfdf5cb3078
base_tree: fcbfbc88ad26ab13708d372e6f1def166da16965
verified: strong
---
# Fm night runs fm sentinel (closed tasks' checks against HEAD, bisect on a new failure) as
## Raw request
> FEATURE: fm night runs fm sentinel (closed tasks' checks against HEAD, bisect on a new failure) as a nightly job
> CONTEXT: round 5 #12. fmnight.py NAMES has no sentinel
## Interpretation
fm night gains a free 'sentinel' job (fm sentinel --bisect: closed tasks' checks against HEAD, a new failure bisected and captured as a FIX) once the project has finished tasks
## Assumptions (confidence)
## Acceptance criteria
- [x] a project with a finished task lists a free sentinel job in fm night --dry-run — verify with `python3 plugin/tests/run.py test_night`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_night, then the job in fmnight.jobs and NAMES
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night test_digest` → exit 0 · Ran 15 tests in 2.4s (7 classes, 16 at a time; slowest: Unattended 2s, NightGuards 2s, Night 1s) / OK [ran] [tree bd55992f8175] (2026-10-15T15:30:55Z)
- `python3 plugin/tests/run.py test_night` → ✗ exit 1 · Ran 12 tests in 2.0s (5 classes, 16 at a time; slowest: NightGuards 2s, Night 1s, PrePlan 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree bd55992f8175] (2026-10-15T15:30:59Z)
- `python3 plugin/tests/run.py test_night` → exit 0 · Ran 12 tests in 1.7s (5 classes, 16 at a time; slowest: NightGuards 2s, Night 1s, PrePlan 0s) / OK [ran] [tree bd55992f8175] (2026-10-15T15:30:59Z)
- (ac 1) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 12 tests in 1.7s (5 classes, 16 at a time; slowest: NightGuards 2s, Night 1s, PrePlan 0s) / OK [ran] [tree bd55992f8175] (2026-10-15T15:32:42Z)
- (audit self) `self review: one free job, listed only once the project has a finished task; sentinel's own --bisect captures FIX tasks that wait for the user like other night captures` → no findings [tree bd55992f8175] (2026-10-15T15:32:42Z)
## Log
- 2026-10-15T15:29:55Z created
- 2026-10-15T15:30:03Z set tier=S
- 2026-10-15T15:30:18Z focused
- 2026-10-15T15:32:42Z done
- 2026-10-15T15:32:43Z committed 48b0cde (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0671 [FEATURE M, done, 3 steps] Milestone: Features — Autonomy and the user — lesson: A guard-word filter on free text needs the verbs people actually use (push, delet…
- research brainstorm-round5-20261015: Probe: `fm ideas` with capability map + unspoken needs, 2 rounds, past every earlier ideas.md (brainstorm-20261015-101633): 54 new t…
- research T-0298-review-1: Findings
- decision 2026-10-15: Round 5 slate: 7 builds from 54 grounded ideas (snapshot before discarding commands, risk-ranked review, claims audit, keep-going stall count, night…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Files touched
- plugin/tests/test_night.py
- plugin/lib/fmnight.py
