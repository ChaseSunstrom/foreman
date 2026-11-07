---
id: T-3123
type: FEATURE
tier: L
status: blocked
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:15:19Z
updated: 2026-11-05T03:20:51Z
---
# Self-awareness: Sampo notices what the user would otherwise point out: a miss ledger from the user's pointing-out messages, turn-end self-checks per miss class, and a next-ask review at each task boundary
## Raw request
> Self-awareness: Sampo notices what the user would otherwise point out: a miss ledger from the user's pointing-out messages, turn-end self-checks per miss class, and a next-ask review at each task boundary
## Interpretation
The user (2026-11-05): 'think about how to make yourself more self aware and capture things like that in the future so I don't need to point them out, and fo everything thing', after one evening of pointing out a stalled page, unfiled Sampo bugs, an unmeasured merge queue, local models never used on real work and 5,000 cards with no view. Reading 1 (chosen): every user message that points something out is a miss, logged with its class; each class gets a cheap turn-end check that fires before the user would (stalled user asks, unfiled workarounds, long waits with no measured cause, outputs at scale with no view, goals unreachable at the current rate, capabilities unused on real work, dead or silent background jobs); at each task boundary the next-request predictor's top guesses that nothing covers become captures; the measure is user-pointed misses per day, trending down. Reading 2: a reminder in the rules only; rejected, a rule without a check is what failed tonight.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a user message that points something out (why is X not done, are you also, have you tried, how come, can we improve) is logged as a miss with its class and the turn it came; sampo misses shows them by class and per day — verify with `python3 plugin/tests/run.py test_self_aware`
- [ ] the turn-end checks fire for each class with numbers: a user-sourced task unmoved for an hour, a refusal routed around with no capture that turn, a merge or slot waiting over 30 min, a store over 500 items with no page listing it, a target unreachable at the measured rate, a capability with zero real-work uses, a background job silent for 30 min — verify with `python3 plugin/tests/run.py test_self_aware`
- [ ] at each task boundary the predictor's top three next asks that no open task covers are captured with source 'predicted'; a predicted capture the user later asks for counts as a catch — verify with `python3 plugin/tests/run.py test_self_aware`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the Stop hook's reply gates, the friction digest, the ledger's events, the next-request predictor and the blind-spots lens; add a miss ledger and one check per class; likely outcome: the drive surfaces each class's hit with its numbers before the user asks. 2. Do less: a weekly report of misses; fails if: tonight's misses each cost hours before the user noticed. 3. A model reads every turn for misses; fails if: models advise and proof decides, and most classes are measurable without a model. Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] part 1: the miss ledger and classes (test-first)  <- CURRENT
2. [ ] part 2: the turn-end checks per class
3. [ ] part 3: the boundary review from the predictor
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:15:19Z created
- 2026-11-05T03:15:24Z set approved=True
- 2026-11-05T03:20:51Z blocked: umbrella: parts T-3126 to T-3128 wait for builder slots
## Follow-ups captured
## Build vs reuse
Reuses the Stop hook's reply gates (hooks.py: _claims_gate, the clause check), the friction digest (friction.py), the ledger and global events, the next-request predictor (the self-running line reports it), the blind-spots lens and standing-intent; new: a misses store, one check function per class, and the boundary review.
