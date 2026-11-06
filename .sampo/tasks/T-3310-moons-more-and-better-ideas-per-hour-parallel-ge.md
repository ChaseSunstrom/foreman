---
id: T-3310
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T04:06:47Z
updated: 2026-11-06T04:10:59Z
---
# Moons: more and better ideas per hour: parallel generators on every endpoint (local GPU, Jarvis, Haiku), anti-repetition prompts, a kill judge that knows Sampo exists
## Raw request
> Moons: more and better ideas per hour: parallel generators on every endpoint (local GPU, Jarvis, Haiku), anti-repetition prompts, a kill judge that knows Sampo exists
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] moons grow runs generators on the local GPU model, Jarvis and Haiku at once (the store lock held only around writes, not the whole run), each endpoint at its own slot count — verify with `python3 plugin/tests/run.py test_moons_scale`
- [ ] each batch prompt carries the kept set's most over-used openers and phrases as things to avoid (learned from kept titles, never a fixed list) and 3 kept moons from distant cells as anchors to differ from; a test shows the avoid list comes from the data — verify with `python3 plugin/tests/run.py test_moons_scale`
- [ ] the kill judge's prompt says what Sampo is and already has, so a Sampo-subject moon is never killed as 'a hypothetical system that does not exist' (20+ such kills on 2026-11-06) — verify with `python3 plugin/tests/run.py test_moons_scale`
- [ ] sampo moons yield shows kept per hour and survival per generator model, and the run routes more batches to the model with the best kept-per-hour — verify with `python3 plugin/tests/run.py test_moons_scale`
- [ ] low and medium tier ideas are kept too when they are unique (embedding-distinct from every kept moon), in their own pool beside the wild ones, so the implementation queue can draw on them; the 10,000 count stays the wild tier unless the user says otherwise — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests for the four criteria  <- CURRENT
2. [ ] store lock around writes; endpoint pool with slots
3. [ ] avoid-list + anchors in the batch prompt; Sampo context in the kill judge
4. [ ] yield per model and routing
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:06:47Z created
## Follow-ups captured
