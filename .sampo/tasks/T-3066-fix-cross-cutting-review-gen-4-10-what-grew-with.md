---
id: T-3066
type: FIX
tier: L
status: deferred
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:12Z
updated: 2026-11-05T04:42:22Z
trigger: genesis-review
trigger_key: 97956892706598cc
---
# FIX: cross-cutting review gen-4 #10 (what grew without earning it): The CLI monolith…
## Raw request
> FIX: cross-cutting review gen-4 #10 (what grew without earning it): The CLI monolith moved and grew to 8,724 lines in the move; the rename was the chance to split it and instead added verbs users then reach for that don't exist ("fm models", "fm plan", "fm stop"). [plugin/lib/sampo/cli.py]
> genesis-review 4:10
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
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
- 2026-11-05T00:31:12Z created
- 2026-11-05T04:42:22Z deferred: splitting cli.py (8,724 lines) is a large refactor with no user-facing gain now; the missing-verb part ('fm models', 'fm plan') is T-3115's steer
## Follow-ups captured
