---
id: T-1583
type: FEATURE
tier: S
status: blocked
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-22T18:38:40Z
updated: 2026-10-23T08:44:04Z
---
# Catch it earlier: nothing runs or version-checks the SQL in playbooks; a reviewer with the
## Raw request
> T-1503 (Engineering playbooks: SQL, migrations, text/time/bytes, dependencies, characterisation, deprecation, decision memos) wasn't caught before it shipped: nothing runs or version-checks the SQL in playbooks; a reviewer with the docs caught it
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
- 2026-10-22T18:38:40Z created
- 2026-10-23T08:44:04Z blocked: the playbooks' SQL is Postgres (CREATE INDEX CONCURRENTLY, NOT VALID constraints, row-level security) written inline in prose; running or version-checking it needs a Postgres server, and none is installed here. With one: mark runnable statements in a sql block and run them in a scratch database from fm check playbooks
## Follow-ups captured
