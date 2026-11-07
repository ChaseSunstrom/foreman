---
id: T-3517
type: CLEAN
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:11:46Z
updated: 2026-11-06T19:22:03Z
lane: ~/.claude/foreman.lanes/T-3517
lane_branch: foreman/T-3517
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T19:13:24Z
plan0_scope: []
group: builder regression tests before lane review
---
# 32 inbox tasks are titled 'Catch it earlier: the builder's own failing test before the…
## Raw request
> CLEAN: 32 inbox tasks are titled 'Catch it earlier: the builder's own failing test before the fix, then the lane review;…' (16 open, 5 from today) and 23 'Feature anticipation gap 3…' look alike: the source task id goes in the title and repeats of one rule merge into one task
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] an auto-captured task's title carries its source task id, and a capture repeating an open task of the same rule and source logs onto it instead of a new task — verify with `python3 plugin/tests/run.py test_inbox_more`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] source id in the title and merge repeats, test-first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_inbox_more` → exit 0 · Ran 38 tests in 116.1s (14 jobs, 16 at a time; slowest: Served.test_revive_from_the_page 5s, App 3s, Ticket 3s) / OK [ran] [tree dd731e550c2d] [world 2f1906870a] (2026-11-06T19:22:03Z)
## Log
- 2026-11-06T19:11:46Z created
- 2026-11-06T19:12:37Z set tier=S
- 2026-11-06T19:12:38Z planned: it has criteria and steps
- 2026-11-06T19:12:42Z lane: ~/.claude/foreman.lanes/T-3517 on foreman/T-3517
- 2026-11-06T19:13:23Z focused
- 2026-11-06T19:13:24Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2774 [CLEAN M, done, 3 steps] Rune's anticipation gaps are consumed, not dropped: the next generation's predict action lists the last generation's missed steers, and s…
- T-2773 [FEATURE M, dropped, 0 steps] FEATURE: anticipation gap (#3): the user's steer wasn't among gen-4's sealed…
- T-2827 [FEATURE M, deferred, 0 steps] FEATURE: anticipation gap (#3): the user's steer wasn't among gen-4's sealed…
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
