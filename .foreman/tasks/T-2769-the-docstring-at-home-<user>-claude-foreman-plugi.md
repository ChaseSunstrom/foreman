---
id: T-2769
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T04:39:09Z
updated: 2026-11-03T04:39:14Z
---
# The docstring at ~/.claude/foreman/plugin/lib/sampo/design.py:11-12 promises a…
## Raw request
> the docstring at ~/.claude/foreman/plugin/lib/sampo/design.py:11-12 promises a standalone CI copy that the new import breaks. It is worth a small task to check the claim and reword or fix it
> (noticed by an agent; research T-2748-review)
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
- 2026-11-03T04:39:09Z created
- 2026-11-03T04:39:14Z dropped: not a regression: before the move fmdesign.py imported fmcore too (git show <merge>^1:plugin/lib/fmdesign.py:27), and 'runs without fm' means the script runs from the lib dir without the fm CLI, which it still does (python3 plugin/lib/sampo/design.py contrast … runs; the __main__ block keeps lib on the path)
## Follow-ups captured
