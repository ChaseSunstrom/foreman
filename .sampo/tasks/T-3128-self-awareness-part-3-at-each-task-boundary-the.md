---
id: T-3128
type: FEATURE
tier: S
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:20:45Z
updated: 2026-11-06T03:53:38Z
inferred_deps: [T-3123]
inferred_why: T-3123: named in its request
group: self-awareness and miss ledger
---
# Self-awareness part 3: at each task boundary, the predicted next asks no open task covers become captures, and a predicted capture the user later asks for counts as a catch (T-3123)
## Raw request
> Self-awareness part 3: at each task boundary, the predicted next asks no open task covers become captures, and a predicted capture the user later asks for counts as a catch (T-3123)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] at a task boundary the predictor's top three next asks that no open task's title or criteria cover are captured with source 'predicted'; when a later user message matches a predicted capture, it is marked caught and sampo misses counts catches beside misses — verify with `python3 plugin/tests/run.py test_self_aware`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests with a fake predictor  <- CURRENT
2. [ ] the boundary capture and the catch match
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:20:45Z created
- 2026-11-05T03:20:51Z set approved=True
- 2026-11-05T03:20:51Z blocked: approved; waits for a builder slot
- 2026-11-06T03:53:38Z unblocked
## Follow-ups captured
