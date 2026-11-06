---
id: T-1482
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T17:09:44Z
updated: 2026-10-23T05:05:44Z
group: guard corpus and false blocks
done_in: T-1727
---
# Guard corpus: cover the obfuscated forms of the four bench SNAPSHOT commands (git reset --
## Raw request
> Guard corpus: cover the obfuscated forms of the four bench SNAPSHOT commands (git reset --hard HEAD~5, git checkout -- ., git clean, git stash drop…) from a disposable git folder, so a variant like \git reset --hard that skips the snapshot is caught; T-1263 left them out because their verdict depends on the tree
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
- 2026-10-22T17:09:44Z created
- 2026-10-23T03:33:02Z batched into T-1727
- 2026-10-23T05:05:44Z done in T-1727 (batch)
## Follow-ups captured
