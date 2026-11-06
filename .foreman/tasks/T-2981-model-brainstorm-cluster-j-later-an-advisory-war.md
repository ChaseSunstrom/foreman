---
id: T-2981
type: SECURITY
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-04T14:20:36Z
updated: 2026-11-06T03:53:21Z
---
# Ward risk head: an advisory model that may only turn an allow into an ask, labelled by guard outcomes, probed by a local attacker
## Raw request
> Model brainstorm cluster J (later): an advisory Ward risk head trained on guard refusals that may only tighten the rule-based guard (ask, never allow), probed by a trained attacker over the shared text channel (research brainstorm-20261104-model)
## Interpretation
Reading 1 (chosen): a shadow-first advisory scorer over tool calls the rules allow; it may only raise an ask (allow to ask), never allow or block; labels come only from outcomes (991 logged guard blocks, blocks later granted, blocks today's guard allows, allowed calls later reverted or that a later rule would block); scored on held-out projects; a local attacker writes evasions of the rule set to probe rules and head. Reading 2: let a model replace parts of the rule guard; rejected, the decision of 2026-11-04 keeps the guard rule-based and a model may only ask.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo exam models --ward DIR writes Ward Examples labelled only by outcomes (block kept, block granted, block today's rules allow, allowed then reverted or later ruled), split by whole projects, with no agent-authored text — verify with `python3 plugin/tests/run.py test_ward_head`
- [ ] the head can only tighten: with the ward_head setting on, a high score turns an allow into an ask and never turns a block into an allow or an ask into an allow; with it off (the default) no guard decision changes and scores go to shadow only — verify with `python3 plugin/tests/run.py test_ward_head test_guard`
- [ ] an attacker run: a local model given the rule names and the guard tests' blocked examples writes evasion attempts; each is run through the rules and the head; rules-alone and rules-plus-head catch rates and the false-ask rate on held-out normal calls are in research, and each rule miss is captured as a task — verify with `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/T-2981-ward-head.md`
- [ ] the head goes live only when it adds catches on the held-out attack set with false asks at most 1% of held-out normal calls; otherwise it stays shadow, with a decision row citing the run — verify with `python3 plugin/tests/run.py test_ward_head`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the T-2975 bge-m3 k-NN baseline and a logistic head as the scorer, guard_block events plus outcomes as data, offline shadow scoring first; likely outcome: a measured shadow head, live only if it clears the bar. 2. Do less: only the attacker probe of the rule guard, each miss captured as a rule task; fails if: the request's model never exists, though the misses are the highest-value output and are kept in 1. 3. A model inline in the hook from the start; fails if: a model call on every tool call costs latency thousands of times a day and puts a model in the guard's path. Choice 1 (70%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: outcome-only labels and project split; the head only tightens (allow to ask), never loosens; off by default changes nothing  <- CURRENT
2. [ ] export and label; count each label; fewer than 50 missed-risk labels keeps the head shadow-only, recorded
3. [ ] head: bge-m3 embedding and a logistic head, the k-NN baseline as rival, shadow scores on held-out projects
4. [ ] attacker: a local model writes evasions from the rule names and test examples; rules and head scored; misses captured as rule tasks
5. [ ] numbers in research; the live bar and decision row
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T14:20:36Z created
- 2026-11-05T02:33:55Z planned from capture
- 2026-11-05T02:34:02Z criterion 3 verify: `test -f state/projects/foreman-4a056f/research/T-2981-ward-head.md` → `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/T-2981-ward-head.md`
- 2026-11-05T02:34:03Z set approved=True
- 2026-11-05T02:34:03Z blocked: planned and approved; waits for a builder slot (6 lanes open until the merge chain lands them)
- 2026-11-06T03:53:21Z unblocked
## Follow-ups captured
