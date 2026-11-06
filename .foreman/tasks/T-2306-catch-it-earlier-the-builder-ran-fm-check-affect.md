---
id: T-2306
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-31T09:39:17Z
updated: 2026-10-31T09:41:55Z
---
# Catch it earlier: the builder ran fm check --affected, which picked test_hooks but not…
## Raw request
> T-2305 (Hooks import no glob: T-2297's leads-record prune lists the folder without a top-level import) wasn't caught before it shipped: the builder ran fm check --affected, which picked test_hooks but not test_core's LaterImports import-budget test; the full suite only runs at ship
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
- 2026-10-31T09:39:17Z created
- 2026-10-31T09:41:55Z dropped: duplicate of T-2307 (a builder is on it): fm check --affected pulls test_core's import-budget tests into hook-path module changes
## Follow-ups captured
