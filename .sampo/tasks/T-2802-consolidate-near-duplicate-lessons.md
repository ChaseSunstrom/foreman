---
id: T-2802
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: night
created: 2026-11-03T08:38:52Z
updated: 2026-11-03T21:11:06Z
done_in: T-2742
---
# Consolidate near-duplicate lessons
## Raw request
> - T-1929.1 + T-1936.1: keep T-1936.1 "Match guard refusals by their exact text or a constant, never a substring of free text that can hold user paths"; retire the others with fm recall --lessons --retire ID --why merged
> - T-0421.1 + T-0422.1: keep T-0421.1 "Check the property (a download reaches a shell; a word may expand) rather than the shape of one line."; retire the others with fm recall --lessons --retire ID --why merged
> - T-0840.1 + T-0842.1: keep T-0840.1 "none: bookkeeping"; retire the others with fm recall --lessons --retire ID --why merged
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
- 2026-11-03T08:38:52Z created
- 2026-11-03T21:11:06Z done in T-2742: done inline: retired T-1929.1 (into T-1936.1), T-0422.1 (into T-0421.1), T-0842.1 and T-0840.1 ('none: bookkeeping' is a no-lesson marker) with fm recall --lessons --retire
## Follow-ups captured
