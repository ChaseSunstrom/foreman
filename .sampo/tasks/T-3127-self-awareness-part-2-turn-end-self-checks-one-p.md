---
id: T-3127
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:20:44Z
updated: 2026-11-06T03:52:28Z
inferred_deps: [T-3123]
inferred_why: T-3123: named in its request
group: self-awareness and miss ledger
---
# Self-awareness part 2: turn-end self-checks, one per miss class, that fire with numbers before the user would ask (T-3123)
## Raw request
> Self-awareness part 2: turn-end self-checks, one per miss class, that fire with numbers before the user would ask (T-3123)
## Interpretation
Reading 1 (chosen): the Stop hook runs cheap checks (no model) and names each hit with its numbers: a user-sourced task unmoved for 60 min; a refusal or failure this turn routed around with no capture; a merge or builder slot waiting over 30 min; a store over 500 items with no page that lists it; a target its measured rate can't reach in 30 days; a capability with zero real-work uses in 7 days; a background job whose log or store hasn't changed in 30 min. Each hit is held once per turn like the clause check. Reading 2: a daily report; rejected, tonight's misses cost hours each.
## Assumptions (confidence)
## Acceptance criteria
- [ ] each class fires on a fixture of tonight's case (the T-3055 merge waiting 3 h behind closes; the 27B never tried on a real task; cards with no page; moons at 3.2% yield against 10,000; the card writer stopped) and stays quiet when the case is resolved; a hit is held once per turn and names its numbers — verify with `python3 plugin/tests/run.py test_self_aware`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the Stop hook's held-once gates, the ledger and events, task sources, lane and merge state, store counts; likely outcome: each class fires on tonight's cases in tests. 2. Do less: three classes; fails if: the user still points out the rest. 3. A model reviews the turn; fails if: models advise, proof decides, and these are countable. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests per class with fixtures  <- CURRENT
2. [ ] the checks in the Stop hook, held once
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:20:44Z created
- 2026-11-05T03:20:50Z set approved=True
- 2026-11-05T03:20:50Z blocked: approved; waits for a builder slot
- 2026-11-05T03:49:26Z add a class: CI red on main (2026-11-05: the tests workflow red for 14 h, two pushes, unnoticed until the drive offered T-2969)
- 2026-11-05T04:43:24Z stalled-ask check: before flagging a user ask as stalled, test whether it is already built (T-2082/T-1792 sat blocked 6 days on a confirm for pages T-1220 had shipped)
- 2026-11-06T03:52:28Z unblocked
## Follow-ups captured
