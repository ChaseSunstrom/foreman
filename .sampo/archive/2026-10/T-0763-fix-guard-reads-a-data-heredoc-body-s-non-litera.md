---
id: T-0763
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-14T15:36:32Z
updated: 2026-10-14T15:42:40Z
---
# FIX: guard reads a data heredoc body's non-literal args as $_ tree writes ('./$_ (a tree w
## Raw request
> FIX: guard reads a data heredoc body's non-literal args as $_ tree writes ('./$_ (a tree write over it)', 2x; fmguard.py:1360/2220/2096) when the same command runs an interpreter
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
- 2026-10-14T15:36:32Z created
- 2026-10-14T15:42:40Z dropped: by design: the heredoc's script is run by the same command, so its subprocess calls with computed arguments really run and can't be read before they do; relaxing it would let a written-and-run script write anywhere
## Follow-ups captured
