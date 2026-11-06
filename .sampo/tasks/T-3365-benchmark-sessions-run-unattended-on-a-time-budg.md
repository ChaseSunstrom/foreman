---
id: T-3365
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/bench.py, plugin/tests/test_bench.py]
depends_on: []
source: followup
created: 2026-11-06T05:55:18Z
updated: 2026-11-06T05:55:19Z
---
# Benchmark sessions run unattended on a time budget: a session that stops early without claiming done gets a fixed 'I'm away, use your defaults' nudge at most 3 times (each counted), and each run records questions (AskUserQuestion plus replies ending in a question), stalls and interventions
## Raw request
> Benchmark sessions run unattended on a time budget: a session that stops early without claiming done gets a fixed 'I'm away, use your defaults' nudge at most 3 times (each counted), and each run records questions (AskUserQuestion plus replies ending in a question), stalls and interventions
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] with a fake claude that stops early twice, the session gets two nudges and the run records questions, stalls and interventions — verify with `python3 plugin/tests/run.py test_bench`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] fake-claude test, red  <- CURRENT
2. [ ] nudge loop and counts in _session
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:55:18Z created
## Follow-ups captured
