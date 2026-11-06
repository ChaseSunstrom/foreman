---
id: T-0794
type: FEATURE
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-14T15:55:21Z
updated: 2026-10-28T09:56:18Z
revisit: 2026-11-11
---
# Later from T-0760: Slim Foreman: Lite mode, retire adapters, freeze the mod, eject, fuses,
## Raw request
> Later from T-0760: Slim Foreman: Lite mode, retire adapters, freeze the mod, eject, fuses, dead code (19 ideas; brainstorm-20261014 cluster simplicity: a separate CLEAN milestone; not this run)
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
- 2026-10-28T09:56:18Z deferred: revisited 2026-10-28: the evidence its title waits on (real use, an incident, a Claude Code event) hasn't come; checked again in two weeks (revisit 2026-11-11)
## Follow-ups captured
## Context
Usage evidence (T-0818 round 2, 2026-10-14; state/events.jsonl Bash commands 2026-10-03..10-14, the log rotates so only 11 days): 4,944 fm calls by Claude, 92 of 108 registered verbs used. Never run by Claude in that window: adopt, agents, bisect, burden, canary, clauses, compact-output, data, docs, evals, explain, export, fail, init, instruments, landscape, lease, logs, machine, mcp, notify, oracle, orders, pause, pr, record, repeats, resume, rewrite, sensitive, session, share, smoke, spec, standing, suspects, sweep, sym, taste, trace, trust, uninstall-user, vetoes, whyred, wiring. Rare (1-2): bench, bus, conductor, deps, dream, drive, evolve, graph, install-user, outcomes, page, plugins, projects, relate, run, sentinel, serve, surprise, sync, tidy, tour, watch, why. Caveat: user-typed verbs, hook-internal calls, fm night and other sessions' logs aren't counted, so 'never used' is a list to check, not a verdict. Script: scratch verb_usage.py (read events.jsonl Bash targets, match fm <verb>).
