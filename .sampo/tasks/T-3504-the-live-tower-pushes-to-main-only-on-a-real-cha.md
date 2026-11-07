---
id: T-3504
type: PERFORMANCE
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:06:00Z
updated: 2026-11-06T19:10:54Z
lane: ~/.claude/foreman.lanes/T-3504
lane_branch: foreman/T-3504
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:08:41Z
plan0_scope: []
group: stats.json driven tower commits and ship tests
---
# The live tower pushes to main only on a real change and at most hourly: 738 tower-update commits so far, 103 of the last 228, each a Pages deploy
## Raw request
> The live tower pushes to main only on a real change and at most hourly: 738 tower-update commits so far, 103 of the last 228, each a Pages deploy
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the live tower's push to main skips a change that is only timestamps, commit ids or counters and pushes at most once an hour, and its commit message says sampo — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] real-change test and hourly floor in rune.py's push, test-first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 226 tests in 14.5s (25 jobs, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 14s, GenesisRead 8s) / OK [ran] [tree 2cdfc1d12dbe] [world 2f1906870a] (2026-11-06T19:10:54Z)
## Log
- 2026-11-06T19:06:00Z created
- 2026-11-06T19:06:17Z lane: ~/.claude/foreman.lanes/T-3504 on foreman/T-3504
- 2026-11-06T19:08:40Z focused
- 2026-11-06T19:08:41Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2555 [FEATURE S, done, 2 steps] fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries — lesson: a…
- T-2955 [FIX M, done, 2 steps] fm ship can't ship a branch that touched a file fm genesis live keeps publishing to main: the tower's commits make the replay fall back to …
- decision 2026-10-30: [outward] Turn on fm genesis live for the Foreman repo: tower changes push site/genesis data to origin main automatically
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- similar finished tasks took 2–2 steps
