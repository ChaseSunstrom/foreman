---
id: T-0792
type: FEATURE
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-14T15:55:21Z
updated: 2026-10-28T09:56:17Z
revisit: 2026-11-11
---
# Later from T-0760: Lanes and fleet: fork from planner session, ListAgents registry, fill w
## Raw request
> Later from T-0760: Lanes and fleet: fork from planner session, ListAgents registry, fill wait time (16 ideas; brainstorm-20261014 cluster lanes-fleet: liveness slice comes first)
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
- 2026-10-14T15:55:21Z created
- 2026-10-14T19:45:48Z deferred: a 'later' brainstorm cluster: it waits on the evidence its title names (real use, an incident, a Claude Code event), not on ideas; the 2026-10-14 loop stopped dry (revisit 2026-10-28)
- 2026-10-16T11:47:17Z set status=captured
- 2026-10-16T11:47:17Z steer: re-queued by the deferred triage (T-1168): not built, nothing blocks it
- 2026-10-16T12:10:10Z set status=deferred
- 2026-10-16T12:10:10Z deferred again after grounding (T-1168 triage): built since: hollow returns rejected at SubagentStop (hollow_return), apply-back gated (fm lane merge passes every file through the guard), lane scope pre-claims (T-1068/T-1138), stalled builders flagged (T-1156), conflict-prone files warned (T-1161). Left: SendMessage mesh across machines, agent teams, ListAgents as registry, haiku repo oracle (L or need Claude Code features); fork lanes (runs on the main model: costlier than sonnet builders); per-lane --settings overlay, idle-time patch proposals, next-brief precompute (M, each its own task when a round grounds them)
- 2026-10-28T09:56:17Z deferred: revisited 2026-10-28: the evidence its title waits on (real use, an incident, a Claude Code event) hasn't come; checked again in two weeks (revisit 2026-11-11)
## Follow-ups captured
