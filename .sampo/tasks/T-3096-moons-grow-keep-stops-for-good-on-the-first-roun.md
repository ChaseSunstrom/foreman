---
id: T-3096
type: FIX
tier: S
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T02:11:39Z
updated: 2026-11-06T03:52:58Z
---
# moons grow --keep waits and retries a local model that stops answering, stopping only after a sustained outage
## Raw request
> moons grow --keep stops for good on the first round whose local calls all fail ('stopped: local'), as when Jarvis is busy with other runs; a long fill should wait and retry a busy or slow local model with backoff (a few minutes, a bounded number of times) and stop only after a sustained outage
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a --keep run whose round ends 'stopped: local' waits (backoff from 60 s doubling, capped at 10 min) and starts the next round, up to a bounded number of waits; a model that answers again resumes the fill; only the last wait ending without an answer stops the run, saying how long it waited — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: a fake local model that fails one round then answers; --keep resumes and adds rows; one that never answers stops after the bounded waits  <- CURRENT
2. [ ] the wait-and-retry in grow --keep's round loop (sleep injectable for the test)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T02:11:39Z created
- 2026-11-05T02:37:34Z planned from capture
- 2026-11-05T02:37:35Z set approved=True
- 2026-11-05T02:37:35Z blocked: after T-3047 merges (both change moonscale.py's grow); the fill runs under a shell retry until then
- 2026-11-05T02:37:42Z criterion 1 verify: `python3 plugin/tests/run.py test_moonscale` → `python3 plugin/tests/run.py test_moons_scale`
- 2026-11-06T03:52:58Z unblocked
## Follow-ups captured
