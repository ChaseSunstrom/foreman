---
id: T-3350
type: FIX
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-06T05:12:25Z
updated: 2026-11-06T05:12:25Z
---
# State writes give up after 5 s with 'lock busy' (core.py:1181 timeout, cli.py:8782-8786…
## Raw request
> State writes give up after 5 s with 'lock busy' (core.py:1181 timeout, cli.py:8782-8786 exit 3) and every caller retries by hand: tonight captures, audits, task evidence and sampo check --evidence each failed several times while a finish, ship or merge held the lock (builders report the same). Interactive mutate should wait with backoff up to ~60 s and say what holds the lock (pid, verb) while waiting; hooks keep their quick timeout but must not drop their state (hooks.py:3704-3725 sets save=False, so the drive's dedupe never persists); capture_promises/capture_friction (cli.py:4634, 4654) drop captures on a 1 s timeout
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:12:25Z created
## Follow-ups captured
