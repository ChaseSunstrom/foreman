---
id: T-3509
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:06:04Z
updated: 2026-11-06T19:14:51Z
lane: ~/.claude/foreman.lanes/T-3509
lane_branch: foreman/T-3509
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:09:12Z
plan0_scope: []
group: stats.json driven tower commits and ship tests
---
# The homepage's own-record numbers render from site/data/stats.json instead of static HTML frozen on 2 November
## Raw request
> The homepage's own-record numbers render from site/data/stats.json instead of static HTML frozen on 2 November
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] site build renders the own-record block (tasks, median check, Ward time, as-of date) from stats.json — verify with `python3 plugin/tests/run.py test_site_landing`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] render the block from stats.json, test-first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_site_landing test_site` → exit 0 · Ran 100 tests in 50.5s (35 jobs, 16 at a time; slowest: CardsPage 14s, Built 14s, Landing 12s) / OK [ran] [tree bcbf48e01d57] [world 2f1906870a] (2026-11-06T19:14:51Z)
## Log
- 2026-11-06T19:06:04Z created
- 2026-11-06T19:06:20Z lane: ~/.claude/foreman.lanes/T-3509 on foreman/T-3509
- 2026-11-06T19:09:11Z focused
- 2026-11-06T19:09:12Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2326 [FEATURE M, done, 3 steps] The website stays current: genesis publish refreshes the homepage stats daily, and the long-horizon card shows hidden checks passed — l…
- T-2957 [FEATURE M, done, 3 steps] Re-sync site/ to the converged illustrated forge (critique 7 converged: landing round 7, tower round 4): the redrawn eight stations as …
- T-2904 [CLEAN M, dropped, 1 steps] Keep 12's port scripts (port.py, annotate.py) in the repo under site/tools, writing…
- decision 2026-11-02: loop round 24: site/build.py, plugin.json, fmlib.py stay
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
