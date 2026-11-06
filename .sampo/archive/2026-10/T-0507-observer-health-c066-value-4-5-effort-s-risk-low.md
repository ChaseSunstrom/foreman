---
id: T-0507
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:33Z
---
# Observer health (C066, value 4/5, effort S, risk low)
## Raw request
> FEATURE: Observer health (C066, value 4/5, effort S, risk low)
>   first version: First version: count swallowed exceptions in hooks into a log, doctor and fm friction read it, plus a canary fixture the Stop hook checks per session so a blind observer is flagged. Skip randomized drills and witness sessions.
>   what it is: Prove the hooks and observers are alive with heartbeats, canaries, witnesses and swallowed-error counts.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 10 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:18Z created
- 2026-10-09T14:30:33Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
