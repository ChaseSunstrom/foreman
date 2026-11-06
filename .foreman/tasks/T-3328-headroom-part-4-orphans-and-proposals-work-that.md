---
id: T-3328
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/headroom.py, plugin/tests/test_headroom.py, plugin/lib/sampo/night.py, plugin/lib/sampo/cli.py]
depends_on: [T-3316]
source: followup
created: 2026-11-06T04:31:29Z
updated: 2026-11-06T04:31:30Z
---
# Headroom part 4: orphans and proposals: work that fits no member of a set, a local-model 'what does a complete version lack' pass on the top 5 sets a night, filed through find.capture; sampo headroom and a night job
## Raw request
> Headroom part 4: orphans and proposals: work that fits no member of a set, a local-model 'what does a complete version lack' pass on the top 5 sets a night, filed through find.capture; sampo headroom and a night job
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] orphans(p, set) reads briefs, steer rules, miss events, failures and ideas; 3 fixture steers about a sixth lens are orphans of LENSES — verify with `python3 plugin/tests/run.py test_headroom`
- [ ] with a fake model, a set with no evidence (not raised, no orphans, no cap hit) is never asked, answers are cached by set hash, a repeat run files nothing new, filings go through find.capture(finder='headroom') so OPEN_CAP and precision muting apply; night.jobs lists headroom at idle priority — verify with `python3 plugin/tests/run.py test_headroom test_night`
## Non-goals
## Approach (options → choice → why)
1) local model only on sets with evidence, rotating, cached: cheap per result. 2) ask about every set nightly: noise and cost. 3) never ask, only measure: misses what's absent from all data. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] orphans by ideas.misses-style overlap  <- CURRENT
2. [ ] rank + ask + cache + capture
3. [ ] sampo headroom [--capture] and the night job
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:31:29Z created
## Follow-ups captured
