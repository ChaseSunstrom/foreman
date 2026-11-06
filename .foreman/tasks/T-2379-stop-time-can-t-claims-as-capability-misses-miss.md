---
id: T-2379
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T14:02:20Z
updated: 2026-11-01T22:44:18Z
group: Mission 6 inbox and installs
---
# Stop-time can't claims as capability misses (Mission 6 inbox, tier 2): a final reply…
## Raw request
> Stop-time can't claims as capability misses (Mission 6 inbox, tier 2): a final reply saying it can't or has no tool for something, while a task is active, logs one capability_miss. Kill-it-fast first: if the last 20 sessions' final replies hold fewer than 3 real tool gaps, drop it as noise
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
- 2026-10-31T14:02:20Z created
- 2026-11-01T22:44:18Z dropped: kill-it-fast check (its own criterion): the last 20 sessions' final replies (all projects) hold 1 can't sentence and 0 real tool gaps ('The registry refuses names container images can't use' describes a rule); under 3, so noise
## Follow-ups captured
