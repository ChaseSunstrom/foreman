---
id: T-3134
type: FIX
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T04:42:23Z
updated: 2026-11-06T03:53:29Z
batch: [T-3064, T-3067, T-3073, T-3078]
---
# Batch: FIX: cross-cutting review gen-4 #8 (wha…; FIX: cross-cutting review gen-4 #11 (wh…; FIX: cross-cutting review ge…
## Raw request
> T-3064: FIX: cross-cutting review gen-4 #8 (what grew without earning it): 2,092 lines of bench output committed into the repo as data; every rerun will grow the diff and nothing reads it at runtime. [research/models/bench.jsonl]
> genesis-review 4:8
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
> T-3067: FIX: cross-cutting review gen-4 #11 (what is being measured wrong): Outcomes quote "49 of 50 held" style hold rates while 1769 of 1960 closes are still inside the 30-day window and 75 of those already lost; the track record is read on under 10% of closes. [191 finished the window]
> genesis-review 4:11
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
> T-3073: FIX: cross-cutting review gen-4 #17 (what is presented ahead of its proof): The close-holds verifier is wired into task finish on a held-out AUC of 0.55 pooled, one point above chance, with the 0.73 figure coming from one project; it is in shadow because it does not work. [AUC 0.55]
> genesis-review 4:17
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
> T-3078: FIX: cross-cutting review gen-4 #22 (what a demanding user would complain about first): SessionStart injected 142k characters over 95 sessions and one stack-card note fired 23 times; the user pays that context every session for notes the friction report itself flags as repeated 3+ times. [142,399 chars]
> genesis-review 4:22
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
## Interpretation
Reading 1: do T-3064, T-3067, T-3073, T-3078 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-3134. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670). Reading 2: each one alone; ruled out because one plan read and one gate run serve them all cheaper.
## Assumptions (confidence)
## Acceptance criteria
- [ ] T-3064: research/models/bench.jsonl lives in the project's state (not the repo); the site build and the bench read it from there; the repo copy is removed — verify with `! git -C ~/.claude/foreman ls-files --error-unmatch research/models/bench.jsonl 2>/dev/null && python3 plugin/tests/run.py test_louhi_models test_site_build`
- [ ] T-3067: a track-record line counts only closes past the 30-day window (and says how many are still in it); 'N of M held' never includes in-window closes — verify with `python3 plugin/tests/run.py test_outcomes`
- [ ] T-3073: the close-holds verifier stays shadow (advice only, never a refusal) until its held-out AUC over 3+ projects passes 0.65, and every line that names it states the pooled AUC (0.55 today) — verify with `python3 plugin/tests/run.py test_bookkeeping`
- [ ] T-3078: SessionStart injects each stack-card note or lesson at most once per session (a seen set), and the session's injected characters fall at least 30% on a replay of the last 95 sessions' starts — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] T-3064: FIX: cross-cutting review gen-4 #8 (what grew without earning it): 2,092 lines of bench…  <- CURRENT
2. [ ] T-3067: FIX: cross-cutting review gen-4 #11 (what is being measured wrong): Outcomes quote "49…
3. [ ] T-3073: FIX: cross-cutting review gen-4 #17 (what is presented ahead of its proof): The…
4. [ ] T-3078: FIX: cross-cutting review gen-4 #22 (what a demanding user would complain about first):…
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T04:42:23Z created
- 2026-11-05T04:42:30Z criterion 1 verify: `` → `! git -C ~/.claude/foreman ls-files --error-unmatch research/models/bench.jsonl 2>/dev/null && python3 plugin/tests/run.py test_louhi_models test_site_build`
- 2026-11-05T04:42:30Z criterion 1 text: T-3064: FIX: cross-cutting review gen-4 #8 (what grew without earning it): 2,092 lines of bench… works → T-3064: research/models/bench.jsonl lives in the project's state (not the repo); the site build and the bench read it from there; the repo copy is removed
- 2026-11-05T04:42:30Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_outcomes`
- 2026-11-05T04:42:30Z criterion 2 text: T-3067: FIX: cross-cutting review gen-4 #11 (what is being measured wrong): Outcomes quote "49… works → T-3067: a track-record line counts only closes past the 30-day window (and says how many are still in it); 'N of M held' never includes in-window closes
- 2026-11-05T04:42:31Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_bookkeeping`
- 2026-11-05T04:42:31Z criterion 3 text: T-3073: FIX: cross-cutting review gen-4 #17 (what is presented ahead of its proof): The… works → T-3073: the close-holds verifier stays shadow (advice only, never a refusal) until its held-out AUC over 3+ projects passes 0.65, and every line that names it states the pooled AUC (0.55 today)
- 2026-11-05T04:42:31Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_hooks`
- 2026-11-05T04:42:31Z criterion 4 text: T-3078: FIX: cross-cutting review gen-4 #22 (what a demanding user would complain about first):… works → T-3078: SessionStart injects each stack-card note or lesson at most once per session (a seen set), and the session's injected characters fall at least 30% on a replay of the last 95 sessions' starts
- 2026-11-05T04:42:31Z set tier=M
- 2026-11-05T04:42:32Z set approved=True
- 2026-11-05T04:42:32Z blocked: approved batch; waits for a builder slot
- 2026-11-06T03:53:29Z unblocked
## Follow-ups captured
