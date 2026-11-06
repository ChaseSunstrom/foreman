---
id: T-2088
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T03:15:13Z
updated: 2026-10-30T13:29:10Z
done_in: T-2090
---
# Genesis keeps the site live on its own: every fm genesis put/init (and exam results)…
## Raw request
> Genesis keeps the site live on its own: every fm genesis put/init (and exam results) re-exports site/genesis and ships it to main (standing grant), debounced so a burst of puts is one push
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
- 2026-10-30T03:15:13Z created
- 2026-10-30T13:29:10Z done in T-2090: already built: fm genesis live (on since 03:31Z) re-exports site/genesis and pushes a data-only commit to main on every tower change, debounced, last push 4a5580eb
## Follow-ups captured
