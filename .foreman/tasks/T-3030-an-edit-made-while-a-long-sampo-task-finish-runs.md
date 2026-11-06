---
id: T-3030
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-04T22:15:19Z
updated: 2026-11-06T03:53:43Z
---
# An edit made while sampo task finish runs is warned and never attributed to the task being closed
## Raw request
> An edit made while a long sampo task finish runs is attributed to the task being closed (finish focuses it), which stales that close's own audits and pulls the file into its commit; T-2995's close failed this way when T-3028's test edit landed mid-check. Either finish shouldn't need the focus, or the hook should warn that a close is running and attribute nothing to it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] while sampo task finish ID runs (a closing marker in meta with its pid, read through c.gates_live's key form), an edit in the project gets the note 'a close of ID is running: this edit isn't part of it' and is not journalled to ID, so ID's audits stay fresh and its commit leaves the file out; with no close running, attribution is as today; a stale marker (dead pid) counts as none — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests in test_hooks: an edit under a live closing marker is not journalled to the closing task and gets the note; a dead pid's marker is ignored  <- CURRENT
2. [ ] finish writes and clears the closing marker; the edit hook reads it (gates_live key='closing') beside _gates_note
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T22:15:19Z created
- 2026-11-05T02:56:53Z planned from capture
- 2026-11-05T02:56:54Z set approved=True
- 2026-11-05T02:56:54Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-11-05T02:56:54Z blocked: planned and approved; waits for a builder slot, and after T-3087's merge (cli.py)
- 2026-11-06T03:53:43Z unblocked
## Follow-ups captured
