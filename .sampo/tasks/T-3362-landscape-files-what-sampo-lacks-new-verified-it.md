---
id: T-3362
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/outside.py, plugin/tests/test_outside.py, plugin/lib/sampo/night.py, plugin/tests/test_night.py]
depends_on: [T-3339]
source: followup
created: 2026-11-06T05:54:24Z
updated: 2026-11-06T05:54:25Z
group: landscape scan and model tracking
---
# Landscape files what Sampo lacks: new verified items recall.covered misses are clustered locally (moonscale _reps/_bar) and filed once per cluster through eco.capture_once with their sources, one trigger per track so each track's precision is judged on its own; the scan runs in Sampo's home project once a week per machine
## Raw request
> Landscape files what Sampo lacks: new verified items recall.covered misses are clustered locally (moonscale _reps/_bar) and filed once per cluster through eco.capture_once with their sources, one trigger per track so each track's precision is judged on its own; the scan runs in Sampo's home project once a week per machine
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the stub's 4x3 claims become 3 captures with sources; a rerun files 0; a muted trigger files 0 — verify with `MOONS_EMBED= python3 plugin/tests/run.py test_outside`
- [ ] due at 7 days and not before; another project's night doesn't list it — verify with `python3 plugin/tests/run.py test_night test_outside`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] cluster and file  <- CURRENT
2. [ ] home-project night job
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:54:24Z created
## Follow-ups captured
