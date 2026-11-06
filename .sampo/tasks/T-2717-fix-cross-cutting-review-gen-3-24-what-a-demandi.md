---
id: T-2717
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T23:14:50Z
updated: 2026-11-02T23:15:45Z
trigger: genesis-review
trigger_key: 480fd8e3f2847d93
---
# FIX: cross-cutting review gen-3 #24 (what a demanding user would complain about first):…
## Raw request
> FIX: cross-cutting review gen-3 #24 (what a demanding user would complain about first): the guard refused the agent writing its own new test file through a Python heredoc, and the hint tells it to use the Edit tool; a harness that blocks the agent from authoring tests for the feature it is building costs a rewrite per file. [plugin/tests/test_steer.py]
> genesis-review 3:24
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
- 2026-11-02T23:14:50Z created
- 2026-11-02T23:15:45Z dropped: by design: the guard refuses interpreter code that writes Foreman's own files (heredocs included) because it can't read what the code writes; the Write and Edit tools author a test file in one call, and the hint says so
## Follow-ups captured
