---
id: T-2315
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T10:45:51Z
updated: 2026-10-31T11:39:27Z
done_in: T-2316
---
# fm-builder.md:26 forbids only 'cd DIR &&' chains, but builders hit 6 refusals on 'cd…
## Raw request
> fm-builder.md:26 forbids only 'cd DIR &&' chains, but builders hit 6 refusals on 'cd plugin/tests; for ...' and passed Grep a path missing foreman/: say never cd (not &&, not ;) and 'Grep/Glob: omit path, they search your worktree'; extend test_lanes.py:556's brief assertion
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
- 2026-10-31T10:45:51Z created
- 2026-10-31T10:46:05Z batched into T-2316
- 2026-10-31T10:57:29Z blocked: member of batch T-2316 (in a builder lane); closes done with it
- 2026-10-31T11:39:27Z done in T-2316 (batch)
## Follow-ups captured
