---
id: T-0891
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T16:40:21Z
updated: 2026-10-15T16:40:33Z
done_in: T-0883
---
# Catch it earlier: local runs always had ~/.cache or XDG_RUNTIME_DIR; CI's fresh HOME is th
## Raw request
> T-0883 (Guard tests keep their temp folder outside /tmp when ~/.cache doesn't exist, and ~user is checked against the passwd entry) wasn't caught before it shipped: local runs always had ~/.cache or XDG_RUNTIME_DIR; CI's fresh HOME is the first place without either
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
- 2026-10-15T16:40:21Z created
- 2026-10-15T16:40:33Z done in T-0883: the CI workflow (T-0882) and the fixed harness (T-0883) are that catch
## Follow-ups captured
