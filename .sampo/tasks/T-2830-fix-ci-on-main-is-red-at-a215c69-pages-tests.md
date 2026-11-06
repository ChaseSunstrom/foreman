---
id: T-2830
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T18:58:29Z
updated: 2026-11-03T21:07:32Z
trigger: ci-red
trigger_key: 86eef8eb2ba79d37
done_in: T-2822
---
# FIX: CI on main is red at a215c69 (pages, tests)
## Raw request
> FIX: CI on main is red at a215c69 (pages, tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/sampo/commit/a215c69987be3fdcf55933495fd6194fa97fd43f
> CI-red: a215c69987be3fdcf55933495fd6194fa97fd43f
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
- 2026-11-03T18:58:29Z created
- 2026-11-03T21:07:32Z done in T-2822: CI red at a215c69 (pages, tests) predates the green CI at 55ee23fd (pages and tests both green), a descendant carrying T-2822's fix
## Follow-ups captured
