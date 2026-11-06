---
id: T-1843
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T16:34:41Z
updated: 2026-10-28T17:02:07Z
---
# Fm drill` has no scheduled or CI run, so the detectors it exercises could regress unseen;
## Raw request
> fm drill` has no scheduled or CI run, so the detectors it exercises could regress unseen; consider a task to run it from `fm check
> (noticed by an agent; research T-1669-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-28T16:34:41Z created
- 2026-10-28T17:02:07Z dropped: already covered: test_drill runs fm drill --seed 11 --faults 6 (every fault kind) and --seed 5 in the suite, which CI runs on every push; a regressed detector reads 'missed' and fails it
## Follow-ups captured
